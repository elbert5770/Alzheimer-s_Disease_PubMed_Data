import xml.etree.ElementTree as ET
import os
from typing import List, Dict, Optional

def generate_file_names() -> List[str]:
    """
    Generate file names based on the pattern pubmed_x0_to_x1.xml
    where x0 ranges from 0 to 3600 in steps of 100
    
    Returns:
        List[str]: List of expected file names
    """
    file_names = []
    for x0 in range(0, 3600, 100):
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

def read_xml_file(file_name: str) -> Optional[Dict]:
    """
    Read and parse a single XML file
    
    Args:
        file_name (str): Name of the XML file to read
        
    Returns:
        Dict: Dictionary containing file info and article count, or None if file doesn't exist
    """
    if not check_file_exists(file_name):
        print(f"File not found: {file_name}")
        return None
    
    try:
        tree = ET.parse(file_name)
        root = tree.getroot()
        
        # Count the number of PubmedArticle elements
        articles = root.findall('.//PubmedArticle')
        article_count = len(articles)
        
        return {
            'file_name': file_name,
            'article_count': article_count,
            'exists': True
        }
        
    except ET.ParseError as e:
        print(f"Error parsing XML file {file_name}: {e}")
        return {
            'file_name': file_name,
            'article_count': 0,
            'exists': True,
            'error': str(e)
        }
    except Exception as e:
        print(f"Error reading file {file_name}: {e}")
        return {
            'file_name': file_name,
            'article_count': 0,
            'exists': True,
            'error': str(e)
        }

def process_xml_files() -> List[Dict]:
    """
    Process all XML files based on the range pattern
    
    Returns:
        List[Dict]: List of file information
    """
    file_names = generate_file_names()
    print(f"Generated {len(file_names)} file names to check")
    
    results = []
    for file_name in file_names:
        result = read_xml_file(file_name)
        if result:
            results.append(result)
    
    return results

def print_results(results: List[Dict]):
    """
    Print the results of processing the XML files
    
    Args:
        results (List[Dict]): List of file processing results
    """
    print("\n" + "="*80)
    print("XML FILE PROCESSING RESULTS")
    print("="*80)
    
    existing_files = [r for r in results if r['exists']]
    missing_files = [r for r in results if not r['exists']]
    
    print(f"\nFiles found: {len(existing_files)}")
    print(f"Files missing: {len(missing_files)}")
    
    total_articles = sum(r['article_count'] for r in existing_files)
    print(f"Total articles across all files: {total_articles}")
    
    if existing_files:
        print(f"\nExisting files:")
        for result in existing_files:
            status = f"({result['error']})" if 'error' in result else ""
            print(f"  ✓ {result['file_name']}: {result['article_count']} articles {status}")
    
    if missing_files:
        print(f"\nMissing files:")
        for result in missing_files:
            print(f"  ✗ {result['file_name']}")

def save_results_to_file(results: List[Dict], output_file: str = "xml_file_summary.txt"):
    """
    Save the results to a text file
    
    Args:
        results (List[Dict]): List of file processing results
        output_file (str): Output file name
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("PubMed XML File Summary\n")
            f.write("="*30 + "\n\n")
            
            existing_files = [r for r in results if r['exists']]
            missing_files = [r for r in results if not r['exists']]
            
            f.write(f"Files found: {len(existing_files)}\n")
            f.write(f"Files missing: {len(missing_files)}\n")
            
            total_articles = sum(r['article_count'] for r in existing_files)
            f.write(f"Total articles: {total_articles}\n\n")
            
            f.write("Existing files:\n")
            f.write("-" * 20 + "\n")
            for result in existing_files:
                status = f" (ERROR: {result['error']})" if 'error' in result else ""
                f.write(f"{result['file_name']}: {result['article_count']} articles{status}\n")
            
            if missing_files:
                f.write(f"\nMissing files:\n")
                f.write("-" * 15 + "\n")
                for result in missing_files:
                    f.write(f"{result['file_name']}\n")
        
        print(f"\nResults saved to: {output_file}")
        
    except Exception as e:
        print(f"Error saving results to file: {e}")

def main():
    """
    Main function to process XML files
    """
    print("PubMed XML File Reader")
    print("="*30)
    print("Checking files with pattern: pubmed_x0_to_x1.xml")
    print("where x0 ranges from 0 to 3600 in steps of 100")
    
    # Process all XML files
    results = process_xml_files()
    
    # Print results
    print_results(results)
    
    # Save results to file
    save_results_to_file(results)

if __name__ == "__main__":
    main() 