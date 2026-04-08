#!/usr/bin/env python
"""Merge two NBIB/medline files, deduplicating by PMID.

For duplicate PMIDs, the record from the second (newer) file is preferred.
Output preserves raw NBIB format by reading files as text blocks.
"""

import argparse
import re
import sys


def parse_nbib_blocks(filepath):
    """Parse an NBIB file into a dict of PMID -> raw text block."""
    records = {}
    with open(filepath) as f:
        content = f.read()
    # Split on blank lines between records
    blocks = re.split(r'\n\n+', content.strip())
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        match = re.search(r'^PMID-\s*(\d+)', block, re.MULTILINE)
        if match:
            pmid = match.group(1)
            records[pmid] = block
        else:
            print('warning: skipping block without PMID', file=sys.stderr)
    return records


def main():
    parser = argparse.ArgumentParser(description='Merge two NBIB files by PMID')
    parser.add_argument('base', help='Base NBIB file (existing)')
    parser.add_argument('new', help='New NBIB file to merge in')
    parser.add_argument('-o', '--output', required=True, help='Output NBIB file')
    args = parser.parse_args()

    base = parse_nbib_blocks(args.base)
    new = parse_nbib_blocks(args.new)

    print(f'base: {len(base)} records')
    print(f'new: {len(new)} records')

    only_base = set(base) - set(new)
    only_new = set(new) - set(base)
    both = set(base) & set(new)

    print(f'only in base: {len(only_base)}')
    print(f'only in new: {len(only_new)}')
    print(f'in both (preferring new): {len(both)}')

    # Merge: start with new, add base-only
    merged = dict(new)
    for pmid in only_base:
        merged[pmid] = base[pmid]

    print(f'merged: {len(merged)} records')

    # Sort by PMID descending (newer first)
    sorted_pmids = sorted(merged.keys(), key=int, reverse=True)

    with open(args.output, 'w') as f:
        for i, pmid in enumerate(sorted_pmids):
            if i > 0:
                f.write('\n')
            f.write(merged[pmid])
            f.write('\n')

    print(f'wrote {len(sorted_pmids)} records to {args.output}')


if __name__ == '__main__':
    main()
