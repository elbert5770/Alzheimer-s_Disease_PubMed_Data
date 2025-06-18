import xml.etree.ElementTree as ET
import os
import csv
from typing import List, Dict, Optional

def generate_file_names() -> List[str]:
    """
    Generate file names based on the pattern pubmed_x0_to_x1.xml
    where x0 ranges from 0 to 3600 in steps of 100
    
    Returns:
        List[str]: List of expected file names
    """
    file_names = []
    for x0 in range(0, 3700, 100):
        x1 = x0 + 99  # Each file contains 100 articles (0-99, 100-199, etc.)
        file_name = f"pubmed_{x0}_to_{x1}.xml"
        file_names.append(file_name)
    return file_names

def check_file_exists(file_name: str) -> bool:
    """
    Check if a file exists in the current directory
    
    Args:
        file_name (str): Name of the file to check
        
    Returns:
        bool: True if file exists, False otherwise
    """
    return os.path.exists(file_name)

def extract_article_ids_from_xml(file_name: str) -> List[Dict]:
    """
    Extract ArticleIdList information from a single XML file
    
    Args:
        file_name (str): Name of the XML file to read
        
    Returns:
        List[Dict]: List of dictionaries containing ArticleIdList data
    """
    if not check_file_exists(file_name):
        print(f"File not found: {file_name}")
        return []
    
    try:
        tree = ET.parse(file_name)
        root = tree.getroot()
        
        article_id_lists = []
        
        # Find all PubmedArticle elements
        for article in root.findall('.//PubmedArticle'):
            # Find ArticleIdList within each article
            article_id_list = article.find('.//ArticleIdList')
            if article_id_list is not None:
                # Extract PMID from the article (for reference)
                pmid_elem = article.find('.//PMID')
                pmid = pmid_elem.text if pmid_elem is not None else "N/A"
                
                # Initialize dictionary for this ArticleIdList
                id_data = {
                    'pmid': pmid,
                    'file_source': file_name,
                    'pubmed': None,
                    'mid': None,
                    'pmc': None,
                    'doi': None,
                    'pii': None,
                    'pmcid': None,
                    'other_ids': {}
                }
                
                # Extract all ArticleId elements
                for article_id in article_id_list.findall('ArticleId'):
                    id_type = article_id.get('IdType')
                    id_value = article_id.text
                    
                    if id_type in ['pubmed', 'mid', 'pmc', 'doi', 'pii', 'pmcid']:
                        id_data[id_type] = id_value
                    else:
                        # Store other ID types in the other_ids dictionary
                        id_data['other_ids'][id_type] = id_value
                
                article_id_lists.append(id_data)
        
        return article_id_lists
        
    except ET.ParseError as e:
        print(f"Error parsing XML file {file_name}: {e}")
        return []
    except Exception as e:
        print(f"Error reading file {file_name}: {e}")
        return []

def process_all_xml_files() -> List[Dict]:
    """
    Process all XML files and extract ArticleIdList information
    
    Returns:
        List[Dict]: List of all ArticleIdList data from all files
    """
    file_names = generate_file_names()
    print(f"Generated {len(file_names)} file names to check")
    
    all_article_ids = []
    total_files_processed = 0
    
    for file_name in file_names:
        if check_file_exists(file_name):
            print(f"Processing: {file_name}")
            article_ids = extract_article_ids_from_xml(file_name)
            all_article_ids.extend(article_ids)
            print(f"  - Found {len(article_ids)} ArticleIdList entries")
            total_files_processed += 1
        else:
            print(f"File not found: {file_name}")
    
    print(f"\nTotal files processed: {total_files_processed}")
    print(f"Total ArticleIdList entries found: {len(all_article_ids)}")
    
    return all_article_ids

def save_to_csv(article_ids: List[Dict], output_file: str = "article_ids.csv"):
    """
    Save ArticleIdList data to a CSV file
    
    Args:
        article_ids (List[Dict]): List of ArticleIdList data
        output_file (str): Output CSV file name
    """
    if not article_ids:
        print("No ArticleIdList data to save")
        return
    
    # Get all unique ID types from other_ids
    all_id_types = set()
    for entry in article_ids:
        all_id_types.update(entry['other_ids'].keys())
    
    # Define the CSV columns
    columns = ['pmid', 'file_source', 'pubmed', 'mid', 'pmc', 'doi', 'pii', 'pmcid']
    # Add other ID types as columns
    for id_type in sorted(all_id_types):
        columns.append(f'other_{id_type}')
    
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
            
            for entry in article_ids:
                # Create a row with the standard columns
                row = {
                    'pmid': entry['pmid'],
                    'file_source': entry['file_source'],
                    'pubmed': entry['pubmed'],
                    'mid': entry['mid'],
                    'pmc': entry['pmc'],
                    'doi': entry['doi'],
                    'pii': entry['pii'],
                    'pmcid': entry['pmcid']
                }
                
                # Add other ID types
                for id_type in sorted(all_id_types):
                    row[f'other_{id_type}'] = entry['other_ids'].get(id_type)
                
                writer.writerow(row)
        
        print(f"ArticleIdList data saved to: {output_file}")
        print(f"CSV contains {len(article_ids)} rows and {len(columns)} columns")
        
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def print_summary(article_ids: List[Dict]):
    """
    Print a summary of the extracted ArticleIdList data
    
    Args:
        article_ids (List[Dict]): List of ArticleIdList data
    """
    if not article_ids:
        print("No ArticleIdList data found")
        return
    
    print("\n" + "="*80)
    print("ARTICLE ID LIST SUMMARY")
    print("="*80)
    
    # Count occurrences of each ID type
    id_type_counts = {
        'pubmed': 0,
        'mid': 0,
        'pmc': 0,
        'doi': 0,
        'pii': 0,
        'pmcid': 0,
        'other': 0
    }
    
    other_id_types = set()
    
    for entry in article_ids:
        if entry['pubmed']:
            id_type_counts['pubmed'] += 1
        if entry['mid']:
            id_type_counts['mid'] += 1
        if entry['pmc']:
            id_type_counts['pmc'] += 1
        if entry['doi']:
            id_type_counts['doi'] += 1
        if entry['pii']:
            id_type_counts['pii'] += 1
        if entry['pmcid']:
            id_type_counts['pmcid'] += 1
        if entry['other_ids']:
            id_type_counts['other'] += 1
            other_id_types.update(entry['other_ids'].keys())
    
    print(f"\nTotal ArticleIdList entries: {len(article_ids)}")
    print(f"\nID Type Distribution:")
    for id_type, count in id_type_counts.items():
        if count > 0:
            print(f"  {id_type.upper()}: {count}")
    
    if other_id_types:
        print(f"\nOther ID types found:")
        for id_type in sorted(other_id_types):
            count = sum(1 for entry in article_ids if id_type in entry['other_ids'])
            print(f"  {id_type}: {count}")
    
    # Show sample entries
    print(f"\nSample entries (first 5):")
    for i, entry in enumerate(article_ids[:5]):
        print(f"\nEntry {i+1}:")
        print(f"  PMID: {entry['pmid']}")
        print(f"  File: {entry['file_source']}")
        for id_type in ['pubmed', 'mid', 'pmc', 'doi', 'pii', 'pmcid']:
            if entry[id_type]:
                print(f"  {id_type.upper()}: {entry[id_type]}")
        if entry['other_ids']:
            print(f"  Other IDs: {entry['other_ids']}")

def main():
    """
    Main function to extract ArticleIdList data from XML files
    """
    print("PubMed ArticleIdList Extractor")
    print("="*40)
    print("Extracting ArticleIdList information from XML files")
    print("with pattern: pubmed_x0_to_x1.xml")
    print("where x0 ranges from 0 to 3600 in steps of 100")
    
    # Process all XML files
    article_ids = process_all_xml_files()
    
    if not article_ids:
        print("No ArticleIdList data found in any XML files.")
        return
    
    # Print summary
    print_summary(article_ids)
    
    # Save to CSV
    save_to_csv(article_ids)

if __name__ == "__main__":
    main() 