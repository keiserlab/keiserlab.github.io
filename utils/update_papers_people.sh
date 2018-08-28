#!/bin/bash
#
# KEISER 2018-06-15

echo '=== 1 Update papers ==='
papers/merge_myncbi.py papers/input/mybib.nbib papers/input/preprints.csv -o ../_pages/publications.md -d ../_data/papers.csv

echo '=== 2 Update people ==='
people/authors2people.py ../_data/authors.yml -o ../collections/_people/ -p ../_data/papers.csv
