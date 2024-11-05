source 'https://rubygems.org'

# Use GitHub Pages versions for compatibility
# Can check current versions at: https://pages.github.com/versions/
# http://jekyllrb.com/docs/github-pages/
# https://mmistakes.github.io/minimal-mistakes/docs/quick-start-guide/
gem 'github-pages', group: :jekyll_plugins

# https://mmistakes.github.io/minimal-mistakes/docs/installation/
gem 'jekyll-include-cache'
gem "webrick", "~> 1.7"

# :jekyll_plugins group - these gems are automatically loaded by Jekyll as plugins
group :jekyll_plugins do
  gem "jekyll-feed"        # Generates Atom feed for your posts
  gem "jekyll-seo-tag"     # Adds meta tags for search engines
  gem "jekyll-sitemap"     # Creates sitemap.xml for search engines
  gem "jekyll-redirect-from"  # Create redirects, useful when changing URLs
end

# :development group - these gems are only installed when running in development
# They won't be installed when deploying to GitHub Pages
group :development do
  gem "ruby-lsp"          # Language server (e.g., for vscode extensions)
  gem "html-proofer"      # Test your rendered HTML files
  gem "jekyll-compose"    # Jekyll commands to create posts/drafts
  gem "solargraph"
end