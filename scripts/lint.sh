#!/usr/bin/env bash
#
# Run all project linters. Exits non-zero on the first failure.
#
# Source-level (runs against the repo as checked in):
#   ruff      — python (utils/)
#   yamllint  — yaml (_config.yml, _data/)
#   biome     — scss, json (assets/)
#
# Built-site level (requires `bundle exec jekyll build` or docker compose):
#   htmlproofer — html validation + internal link checking (_site/)

set -euo pipefail

echo '# python'
uvx ruff check utils/

echo '# yaml'
uvx yamllint -d relaxed _config.yml _data/

echo '# scss + json'
npx @biomejs/biome check .

echo '# html (built site)'
if [ -d _site ]; then
    docker compose exec keiserlab bundle exec htmlproofer ./_site \
        --disable-external \
        --allow-hash-href \
        --no-enforce-https \
        --ignore-urls '/tags/,/tbproxy/'
else
    echo 'skipped: _site/ not found (start the container first)'
fi
