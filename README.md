# PubMed XML File Processor

This repository contains programs to process PubMed XML files with the naming pattern `pubmed_x0_to_x1.xml`, where x0 and x1 are generated from the range `range(0, 3600, 100)`.

## Files

### 1. `read_pubmed_xml_simple.py` (Basic file checking)
A simple program that:
- Generates file names based on the pattern `pubmed_x0_to_x1.xml` where x0 ranges from 0 to 3600 in steps of 100
- Checks which files exist in the current directory
- Counts the number of articles in each XML file
- Provides a summary of all files and total article count
- Saves results to `xml_file_summary.txt`

### 2. `extract_article_ids.py` (ArticleIdList extraction - **NEW**)
A program that extracts ArticleIdList information from XML files:
- Processes all XML files with the pattern `pubmed_x0_to_x1.xml`
- Extracts ArticleIdList blocks from each article
- Creates a CSV file with one row per ArticleIdList entry
- Columns include: pmid, file_source, pubmed, mid, pmc, doi, pii, pmcid, and other ID types
- Saves results to `article_ids.csv`

### 3. `read_pubmed_xml.py` (Comprehensive version)
A more comprehensive program that:
- Finds all XML files matching the pattern `pubmed_*_to_*.xml`
- Parses each XML file and extracts detailed article information including:
  - PMID (PubMed ID)
  - Article title
  - Journal name
  - Publication date
  - Authors
  - DOI
  - Abstract
- Provides detailed summaries and sample articles
- Saves comprehensive results to `pubmed_summary.txt`

## Usage

### Basic Usage (File checking)
```bash
python3 read_pubmed_xml_simple.py
```

This will:
- Check for 36 files: `pubmed_0_to_99.xml` through `pubmed_3500_to_3599.xml`
- Display which files exist and how many articles each contains
- Save a summary to `xml_file_summary.txt`

### ArticleIdList Extraction (Recommended for ID analysis)
```bash
python3 extract_article_ids.py
```

This will:
- Process all 36 XML files
- Extract ArticleIdList information from each article
- Create a CSV file with 3,590 rows (one per ArticleIdList)
- Columns include all ID types found: pubmed, mid, pmc, doi, pii, pmcid, etc.
- Save results to `article_ids.csv`

### Comprehensive Usage
```bash
python3 read_pubmed_xml.py
```

This will:
- Process all XML files in the directory
- Extract detailed article information
- Display sample articles
- Save comprehensive results to `pubmed_summary.txt`

## Expected File Pattern

The programs expect XML files with the following naming pattern:
- `pubmed_0_to_99.xml` (articles 0-99)
- `pubmed_100_to_199.xml` (articles 100-199)
- `pubmed_200_to_299.xml` (articles 200-299)
- ...
- `pubmed_3500_to_3599.xml` (articles 3500-3599)

## Output Files

### `xml_file_summary.txt` (from simple version)
Contains:
- Number of files found vs missing
- Total article count
- List of existing files with article counts

### `article_ids.csv` (from extract_article_ids.py) - **NEW**
Contains:
- One row per ArticleIdList entry (3,590 total rows)
- Columns: pmid, file_source, pubmed, mid, pmc, doi, pii, pmcid, other_medline, other_sici
- All ID types found in the ArticleIdList blocks
- File size: ~333KB

### `pubmed_summary.txt` (from comprehensive version)
Contains:
- Detailed information about each article
- PMID, title, journal, authors, abstract, etc.
- Complete article data for analysis

## ArticleIdList CSV Structure

The `article_ids.csv` file contains the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| pmid | PubMed ID from the article | 19622817 |
| file_source | Source XML file | pubmed_0_to_99.xml |
| pubmed | PubMed ID from ArticleIdList | 19622817 |
| mid | Manuscript ID | NIHMS146886 |
| pmc | PubMed Central ID | PMC2763631 |
| doi | Digital Object Identifier | 10.1001/jama.2009.1064 |
| pii | Publisher Item Identifier | 302/4/385 |
| pmcid | PubMed Central ID (alternative) | PMC123456 |
| other_medline | Other MEDLINE IDs | (if present) |
| other_sici | SICI identifiers | (if present) |

## ID Type Distribution (from actual data)

- **PUBMED**: 3,590 entries (100%)
- **DOI**: 3,565 entries (99.3%)
- **PII**: 3,024 entries (84.2%)
- **PMC**: 2,199 entries (61.2%)
- **MID**: 945 entries (26.3%)
- **Other types**: 10 entries (0.3%)

## Requirements

- Python 3.x
- Standard library modules: `xml.etree.ElementTree`, `os`, `csv`, `typing`

## Example Output

```
PubMed ArticleIdList Extractor
========================================
Extracting ArticleIdList information from XML files
with pattern: pubmed_x0_to_x1.xml
where x0 ranges from 0 to 3600 in steps of 100
Generated 36 file names to check
Processing: pubmed_0_to_99.xml
  - Found 91 ArticleIdList entries
...

Total files processed: 36
Total ArticleIdList entries found: 3590

================================================================================
ARTICLE ID LIST SUMMARY
================================================================================

Total ArticleIdList entries: 3590

ID Type Distribution:
  PUBMED: 3590
  MID: 945
  PMC: 2199
  DOI: 3565
  PII: 3024
  OTHER: 10

ArticleIdList data saved to: article_ids.csv
CSV contains 3590 rows and 10 columns
```

## Notes

- The first file (`pubmed_0_to_99.xml`) contains 91 articles instead of 100, which is normal
- One file (`pubmed_2300_to_2399.xml`) contains 99 articles instead of 100
- All other files contain exactly 100 articles each
- Total articles across all files: 3,590
- The ArticleIdList CSV contains exactly 3,590 rows (one per article)
- Most articles have multiple ID types (PubMed ID, DOI, PII, etc.) 