#!/usr/bin/env python
"""Migrate Twitter embed posts to static markdown.

Uses the existing blockquote HTML as the primary content source (it contains
the full rendered tweet including quotes and RTs). Uses the Twitter archive
for t.co URL expansion and local media files.
"""

import argparse
import glob
import json
import os
import re
import shutil
from html import unescape


def load_archive(archive_path):
    """Load tweets.js from Twitter archive into dict keyed by tweet ID."""
    tweets_js = os.path.join(archive_path, "data", "tweets.js")
    with open(tweets_js) as f:
        content = f.read()
    content = re.sub(r"^window\.YTD\.tweets\.part\d+\s*=\s*", "", content)
    tweets = json.loads(content)
    return {t["tweet"]["id_str"]: t["tweet"] for t in tweets}


def is_tweet_url(url):
    """Check if a URL points to a tweet."""
    return bool(re.match(r"https?://(twitter\.com|x\.com)/\w+/status/\d+", url))


def fetch_tweet_via_oembed(tweet_url, media_dest):
    """Fetch tweet content via Twitter's oEmbed API.

    Returns (text, author, handle, date, media_paths) or None.
    media_paths is a list of local paths for downloaded images.
    """
    import subprocess

    try:
        oembed_url = (
            f"https://publish.twitter.com/oembed?url={tweet_url}&omit_script=true"
        )
        result = subprocess.run(
            ["curl", "-s", oembed_url], capture_output=True, text=True, timeout=15
        )
        data = json.loads(result.stdout)
        html = data.get("html", "")
        # Parse the blockquote HTML
        p_match = re.search(r"<p[^>]*>(.*?)</p>", html, re.DOTALL)
        if not p_match:
            return None
        text = p_match.group(1)
        # Convert <br> to newlines
        text = re.sub(r"<br\s*/?>", "\n", text)

        # Convert <a> tags: keep href for real links, drop pic.twitter.com links
        def replace_inner_link(m):
            href = unescape(m.group(1))
            inner = re.sub(r"<[^>]+>", "", m.group(2))
            inner = unescape(inner).strip()
            if inner.startswith("pic.twitter"):
                return ""
            if inner.startswith("#"):
                tag = inner[1:]
                return f"[{inner}](https://twitter.com/hashtag/{tag})"
            if inner.startswith("@"):
                handle = inner[1:]
                return f"[{inner}](https://twitter.com/{handle})"
            return f"[{inner}]({href})"

        text = re.sub(
            r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>',
            replace_inner_link,
            text,
            flags=re.DOTALL,
        )
        text = re.sub(r"<[^>]+>", "", text)
        text = unescape(text).strip()

        author = data.get("author_name", "")
        handle = re.search(r"twitter\.com/(\w+)", data.get("author_url", ""))
        handle = handle.group(1) if handle else ""
        # Extract date from the last <a> tag in the blockquote
        date_match = re.search(r"<a[^>]*>([^<]+)</a>\s*</blockquote>", html)
        date = unescape(date_match.group(1)).strip() if date_match else ""

        # Try to download tweet media
        media_paths = []
        tweet_id_match = re.search(r"/status/(\d+)", tweet_url)
        if tweet_id_match:
            tweet_id = tweet_id_match.group(1)
            # Try syndication API which returns media
            try:
                syn_url = f"https://cdn.syndication.twimg.com/tweet-result?id={tweet_id}&token=0"
                syn_result = subprocess.run(
                    ["curl", "-s", syn_url], capture_output=True, text=True, timeout=15
                )
                if syn_result.stdout:
                    syn_data = json.loads(syn_result.stdout)
                    for photo in syn_data.get("photos", []):
                        img_url = photo.get("url", "")
                        if img_url:
                            # Download the image
                            ext = "jpg"
                            if ".png" in img_url:
                                ext = "png"
                            fname = f"{tweet_id}-quoted.{ext}"
                            dest = os.path.join(media_dest, fname)
                            if not os.path.exists(dest):
                                os.makedirs(media_dest, exist_ok=True)
                                subprocess.run(
                                    ["curl", "-sL", "-o", dest, img_url], timeout=15
                                )
                            if os.path.exists(dest) and os.path.getsize(dest) > 0:
                                media_paths.append(fname)
                                print(f"    downloaded quoted media: {fname}")
            except Exception as e:
                print(f"    could not fetch quoted tweet media: {e}")

        return text, author, handle, date, media_paths
    except Exception as e:
        print(f"    failed to fetch oembed for {tweet_url}: {e}")
        return None


def fetch_tweet_media_via_syndication(tweet_id, media_dest):
    """Download tweet media via Twitter's syndication API. Returns list of filenames."""
    import subprocess

    media_paths = []
    try:
        syn_url = (
            f"https://cdn.syndication.twimg.com/tweet-result?id={tweet_id}&token=0"
        )
        result = subprocess.run(
            ["curl", "-s", syn_url], capture_output=True, text=True, timeout=15
        )
        if result.stdout:
            syn_data = json.loads(result.stdout)
            for photo in syn_data.get("photos", []):
                img_url = photo.get("url", "")
                if img_url:
                    ext = "png" if ".png" in img_url else "jpg"
                    fname = f"{tweet_id}-media.{ext}"
                    dest = os.path.join(media_dest, fname)
                    if not os.path.exists(dest):
                        os.makedirs(media_dest, exist_ok=True)
                        subprocess.run(["curl", "-sL", "-o", dest, img_url], timeout=15)
                    if os.path.exists(dest) and os.path.getsize(dest) > 0:
                        media_paths.append(fname)
                        print(f"    downloaded media: {fname}")
    except Exception as e:
        print(f"    could not fetch tweet media: {e}")
    return media_paths


def resolve_tco(url):
    """Resolve a t.co short URL by following redirects via curl."""
    import subprocess

    try:
        result = subprocess.run(
            ["curl", "-Ls", "-o", "/dev/null", "-w", "%{url_effective}", url],
            capture_output=True,
            text=True,
            timeout=15,
        )
        resolved = result.stdout.strip()
        if resolved and resolved != url:
            print(f"    resolved {url} -> {resolved}")
            return resolved
    except Exception as e:
        print(f"    failed to resolve {url}: {e}")
    print(f"    could not resolve {url}")
    return url


def build_tco_map(archive_tweets):
    """Build a global map of t.co URLs to expanded URLs from all archive tweets."""
    tco_map = {}
    for tweet in archive_tweets.values():
        for url_entity in tweet.get("entities", {}).get("urls", []):
            tco_map[url_entity["url"]] = url_entity.get(
                "expanded_url", url_entity["url"]
            )
        # Also media URLs (these we want to drop, not expand)
        for media in tweet.get("entities", {}).get("media", []):
            tco_map[media["url"]] = None  # None means "remove"
    return tco_map


def expand_tco_url(url, tco_map):
    """Expand a t.co URL using the map, falling back to HTTP resolve."""
    if not url.startswith("https://t.co/"):
        return url
    if url in tco_map:
        return tco_map[url]
    # Not in archive — resolve via redirect
    resolved = resolve_tco(url)
    tco_map[url] = resolved  # cache for future lookups
    return resolved


def find_tweet_media(tweet_id, archive_path):
    """Find local media files for a tweet in the archive."""
    media_dir = os.path.join(archive_path, "data", "tweets_media")
    media_files = []
    if os.path.isdir(media_dir):
        for f in os.listdir(media_dir):
            if f.startswith(tweet_id + "-"):
                media_files.append(os.path.join(media_dir, f))
    return sorted(media_files)


def html_to_markdown(html, tco_map, media_dest):
    """Convert tweet blockquote inner HTML to clean markdown.

    Converts <a> tags to markdown links, expands t.co URLs,
    strips remaining HTML tags, decodes entities.
    """
    # Extract just the <p> content
    p_match = re.search(r"<p[^>]*>(.*?)</p>", html, re.DOTALL)
    if not p_match:
        return ""
    text = p_match.group(1)

    # Convert <a> tags to markdown links
    def replace_link(match):
        href = unescape(match.group(1))
        link_text = re.sub(r"<[^>]+>", "", match.group(2))  # strip nested tags
        link_text = unescape(link_text).strip()

        # Expand t.co URLs
        if href.startswith("https://t.co/"):
            expanded = expand_tco_url(href, tco_map)
            if expanded is None:
                # Media URL — drop it entirely
                return ""
            href = expanded

        # Drop links that resolve to tweet media (can't serve locally)
        if "/photo/" in href or "/video/" in href:
            return ""
        # If link points to another tweet, fetch and inline as quoted content
        if is_tweet_url(href):
            quoted = fetch_tweet_via_oembed(href, media_dest)
            if quoted:
                q_text, q_author, q_handle, q_date, q_media = quoted
                q_lines = [f"> {line}" for line in q_text.split("\n")]
                q_lines.append(">")
                q_lines.append(
                    f"> — {q_author} ([@{q_handle}](https://twitter.com/{q_handle})), [{q_date}]({href})"
                )
                for mf in q_media:
                    q_lines.append(f">\n> ![](/assets/images/posts/{mf})")
                return "\n" + "\n".join(q_lines) + "\n"
            # Fallback: just link to it
            return f"[{href}]({href})"
        # If link text is a URL (t.co or pic.twitter), use expanded URL as text too
        if link_text.startswith("https://t.co/") or link_text.startswith("pic.twitter"):
            if href.startswith("http"):
                return f"[{href}]({href})"
            return ""
        # Link hashtags and @mentions to Twitter
        if link_text.startswith("#"):
            tag = link_text[1:]
            return f"[{link_text}](https://twitter.com/hashtag/{tag})"
        if link_text.startswith("@"):
            handle = link_text[1:]
            return f"[{link_text}](https://twitter.com/{handle})"
        # Otherwise, make a proper markdown link
        return f"[{link_text}]({href})"

    text = re.sub(
        r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', replace_link, text, flags=re.DOTALL
    )

    # Strip any remaining HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    # Ensure spaces between adjacent markdown links and between text and links
    # But never break ](  which is markdown link syntax
    text = re.sub(r"(\))(\[)", r"\1 \2", text)  # )[  -> ) [  (adjacent links)
    text = re.sub(
        r"([^\s\[(!])(\[)", r"\1 \2", text
    )  # X[  -> X [  (text before link, but not ![)
    text = re.sub(
        r"(\))([^\s\]\).,;:!?])", r"\1 \2", text
    )  # )X -> ) X (text after link)
    text = re.sub(r"  +", " ", text)

    # Decode HTML entities
    text = unescape(text)

    # Clean up whitespace
    text = re.sub(r"  +", " ", text)
    text = text.strip()

    return text


def extract_attribution(html):
    """Extract author name, handle, tweet URL, and date from blockquote attribution."""
    # Pattern: &mdash; Name (@handle) <a href="URL">Date</a>
    attr_match = re.search(
        r'(?:&mdash;|—)\s*(.+?)\s*\(@(\w+)\)\s*<a\s+href="([^"]*)"[^>]*>([^<]+)</a>',
        html,
        re.DOTALL,
    )
    if attr_match:
        name = unescape(attr_match.group(1)).strip()
        handle = attr_match.group(2)
        url = unescape(attr_match.group(3))
        date = unescape(attr_match.group(4)).strip()
        # Clean the URL (remove tracking params)
        url = re.sub(r"\?ref_src=.*$", "", url)
        return name, handle, url, date
    return None, None, None, None


def format_as_retweet(text, author_name, author_handle, tweet_url, date):
    """Format a retweet as a markdown blockquote with attribution."""
    lines = []
    for line in text.split("\n"):
        lines.append(f"> {line}")
    lines.append(">")
    lines.append(
        f"> — {author_name} ([@{author_handle}](https://twitter.com/{author_handle})), [{date}]({tweet_url})"
    )
    return "\n".join(lines)


def format_as_tweet(text, tweet_url):
    """Format an original tweet as markdown with link."""
    return f"{text}\n\n[Original post (@keiser_lab)]({tweet_url})"


def convert_twitter_blockquote(
    blockquote_html, tco_map, archive_tweets, archive_path, media_dest
):
    """Convert a single twitter blockquote to markdown."""
    # Extract tweet text
    text = html_to_markdown(blockquote_html, tco_map, media_dest)

    # Extract attribution
    name, handle, tweet_url, date = extract_attribution(blockquote_html)

    if not tweet_url:
        # Try to extract URL from any status link
        url_match = re.search(
            r"twitter\.com/(\w+)/status(?:es)?/(\d+)", blockquote_html
        )
        if url_match:
            handle = url_match.group(1)
            tweet_id = url_match.group(2)
            tweet_url = f"https://twitter.com/{handle}/status/{tweet_id}"

    # Get tweet ID for media lookup
    tweet_id = None
    id_match = re.search(r"/status(?:es)?/(\d+)", tweet_url or "")
    if id_match:
        tweet_id = id_match.group(1)

    # Check if this is a retweet (attributed to someone other than keiser_lab)
    is_rt = handle and handle.lower() != "keiser_lab"

    # Format output
    if is_rt:
        md = format_as_retweet(text, name, handle, tweet_url, date)
    else:
        md = format_as_tweet(text, tweet_url)

    # Handle media from archive or syndication API
    media_names = []
    if tweet_id and tweet_id in archive_tweets:
        media_files = find_tweet_media(tweet_id, archive_path)
        for mf in media_files:
            dest_name = os.path.basename(mf)
            dest_path = os.path.join(media_dest, dest_name)
            if not os.path.exists(dest_path):
                os.makedirs(media_dest, exist_ok=True)
                shutil.copy2(mf, dest_path)
            media_names.append(dest_name)
    elif tweet_id:
        media_names = fetch_tweet_media_via_syndication(tweet_id, media_dest)

    for mf in media_names:
        img_md = f"![](/assets/images/posts/{mf})"
        if is_rt:
            md += f"\n>\n> {img_md}"
        else:
            md += f"\n\n{img_md}"

    return md


def convert_fb_embed(fb_html):
    """Convert a Facebook embed div to markdown blockquote."""
    # Extract post URL
    url_match = re.search(r'data-href="([^"]*)"', fb_html)
    fb_url = unescape(url_match.group(1)) if url_match else ""

    # Extract text from inner blockquote
    bq_match = re.search(r"<blockquote[^>]*><p>(.*?)</p>", fb_html, re.DOTALL)
    text = ""
    if bq_match:
        text = re.sub(r"<[^>]+>", "", bq_match.group(1))
        text = unescape(text).strip()

    # Extract author
    author_match = re.search(r"Posted by.*?<a[^>]*>([^<]+)</a>", fb_html)
    author = author_match.group(1) if author_match else ""

    if text:
        if len(text) > 300:
            text = text[:297] + "..."
        return f"> {text}\n>\n> — {author}, [Facebook post]({fb_url})"
    elif fb_url:
        return f"[Facebook post by {author}]({fb_url})"
    return ""


def process_post(filepath, tco_map, archive_tweets, archive_path, media_dest):
    """Process a single post file."""
    with open(filepath) as f:
        content = f.read()

    # Split frontmatter and body
    if not content.startswith("---"):
        return False
    end = content.index("---", 3)
    frontmatter = content[3:end].strip()
    body = content[end + 3 :]

    # Remove 'embeds' tag from frontmatter
    fm_lines = []
    for line in frontmatter.split("\n"):
        if line.strip() == "- embeds":
            continue
        fm_lines.append(line)
    frontmatter = "\n".join(fm_lines)

    # Process Twitter blockquotes
    # Match blockquote + optional following script tag
    twitter_bq = re.compile(
        r'<blockquote\s+class="twitter-tweet"[^>]*>.*?</blockquote>'
        r"(?:\s*<script[^>]*platform\.twitter\.com/widgets\.js[^>]*></script>)?",
        re.DOTALL,
    )

    parts = []
    last_end = 0
    for match in twitter_bq.finditer(body):
        # Keep content before this blockquote
        before = body[last_end : match.start()]
        parts.append(before)
        # Convert the blockquote
        md = convert_twitter_blockquote(
            match.group(0), tco_map, archive_tweets, archive_path, media_dest
        )
        parts.append(md)
        last_end = match.end()
    parts.append(body[last_end:])
    body = "".join(parts)

    # Clean up standalone twitter script tags
    body = re.sub(
        r'\s*<script\s+async\s+src="https://platform\.twitter\.com/widgets\.js"[^>]*></script>',
        "",
        body,
    )

    # Process Facebook embeds
    # First remove the fb-root/SDK script block
    body = re.sub(
        r'<div\s+id="fb-root"></div>\s*<script>\(function\(d,\s*s,\s*id\).*?</script>\s*',
        "",
        body,
        flags=re.DOTALL,
    )

    # Convert fb-post divs
    fb_pattern = re.compile(r'<div\s+class="fb-post"[^>]*>.*?</div>', re.DOTALL)
    parts = []
    last_end = 0
    for match in fb_pattern.finditer(body):
        parts.append(body[last_end : match.start()])
        parts.append(convert_fb_embed(match.group(0)))
        last_end = match.end()
    parts.append(body[last_end:])
    body = "".join(parts)

    # Clean up: strip <br /> tags, collapse excessive blank lines
    body = re.sub(r"\s*<br\s*/?>\s*", "\n", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    body = body.strip()

    # Reassemble
    output = f"---\n{frontmatter}\n---\n\n{body}\n"

    with open(filepath, "w") as f:
        f.write(output)
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Migrate Twitter embed posts to static markdown"
    )
    parser.add_argument("posts_dir", help="Path to collections/_posts/")
    parser.add_argument("archive_dir", help="Path to Twitter archive directory")
    parser.add_argument(
        "--media-dest",
        default=None,
        help="Destination for tweet media (default: assets/images/posts/)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be changed without modifying files",
    )
    args = parser.parse_args()

    # Resolve media_dest relative to the repo root (parent of collections/)
    if args.media_dest:
        media_dest = args.media_dest
    else:
        posts_abs = os.path.abspath(args.posts_dir)
        # collections/_posts -> collections -> repo root
        repo_root = os.path.dirname(os.path.dirname(posts_abs))
        media_dest = os.path.join(repo_root, "assets", "images", "posts")

    print(f"Loading Twitter archive from {args.archive_dir}...")
    archive_tweets = load_archive(args.archive_dir)
    print(f"Loaded {len(archive_tweets)} tweets from archive")

    tco_map = build_tco_map(archive_tweets)
    print(f"Built t.co URL map with {len(tco_map)} entries")

    # Find posts with twitter embeds
    post_files = sorted(glob.glob(os.path.join(args.posts_dir, "*.md")))
    tweet_posts = []
    for pf in post_files:
        with open(pf) as f:
            content = f.read()
        if (
            "twitter-tweet" in content
            or "platform.twitter.com/widgets.js" in content
            or "fb-root" in content
            or "facebook.net" in content
        ):
            tweet_posts.append(pf)

    print(f"Found {len(tweet_posts)} posts with Twitter embeds")

    for pf in tweet_posts:
        basename = os.path.basename(pf)
        if args.dry_run:
            print(f"  [DRY RUN] Would process: {basename}")
        else:
            print(f"  Processing: {basename}")
            process_post(pf, tco_map, archive_tweets, args.archive_dir, media_dest)

    print("Done!")


if __name__ == "__main__":
    main()
