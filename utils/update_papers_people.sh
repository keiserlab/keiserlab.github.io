#!/usr/bin/env bash
#
# KEISER 2018-06-15
# KEISER 2024-11-05
#
# to check/update dependencies
# `uv lock --upgrade`

echo '# 1 Update papers'
uv run papers/merge_myncbi.py papers/input/mybib.nbib papers/input/preprints.csv -o ../_pages/publications.md -d ../_data/papers.csv -m papers/input/manual.nbib

echo '# 2 Update people'
uv run people/authors2people.py ../_data/authors.yml -o ../collections/_people/ -p ../_data/papers.csv