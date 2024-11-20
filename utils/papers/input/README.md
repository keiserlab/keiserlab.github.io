# papers raw data sources

## published
- `mybib.nbib` from pubmed.gov bibliography, Export File (MEDLINE) -> `medline.txt`, rename
  - manually exclude preprints/biorxiv entries because pubmed.gov only indexes preprints with federal funding
- `manual.nbib` is for any papers not indexed by pubmed (e.g., nature machine intelligence for a while, when it came out)

## preprints
- `preprints.csv` manually populated
- add NCBI LID (usually published DOI) once paper published, to link pre/paper records
- `git mv` preprint `journal.DOI.jpg` -> `LID.jpg` in `assets/images/papers`