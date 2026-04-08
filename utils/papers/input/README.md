# papers raw data sources

## published
- `mybib.nbib` from pubmed.gov bibliography, Export File (MEDLINE) -> `medline.txt`
  - bioRxiv/chemRxiv medline entries are automatically filtered by the merge script (preprints.csv is SSOT for preprints)
  - to merge a new medline export with the existing file: `uv run papers/merge_nbib.py papers/input/mybib.nbib ~/Downloads/medline.txt -o papers/input/mybib.nbib`
- `manual.nbib` is for any papers not indexed by pubmed (e.g., nature machine intelligence for a while, when it came out)
- `skip.csv` lists DOIs to omit from the publications page

## preprints
- `preprints.csv` manually populated (SSOT for preprints)
- add NCBI LID (usually published DOI) once paper published, to link pre/paper records
- `git mv` preprint `journal.DOI.jpg` -> `LID.jpg` in `assets/images/papers`