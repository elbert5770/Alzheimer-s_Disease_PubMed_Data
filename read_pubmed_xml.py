import xml.etree.ElementTree as ET
import os
import glob
from typing import List, Dict, Optional

def get_xml_files() -> List[str]:
    """
    Get all XML files matching the pattern pubmed_*_to_*.xml
    
    Returns:
        List[str]: List of XML file paths
    """
    pattern = "pubmed_*_to_*.xml"
    xml_files = glob.glob(pattern)
    return sorted(xml_files)

def parse_pubmed_xml(xml_file: str) -> Optional[Dict]:
    """
    Parse a PubMed XML file and extract key information
    
    Args:
        xml_file (str): Path to the XML file
        
    Returns:
        Dict: Dictionary containing parsed data, or None if parsing fails
    """
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Define the namespace for PubMed XML
        namespace = {'pubmed': 'https://dtd.nlm.nih.gov/ncbi/pubmed/out/pubmed_250101.dtd'}
        
        articles = []
        
        # Find all PubmedArticle elements
        for article in root.findall('.//PubmedArticle'):
            article_data = {}
            
            # Extract PMID
            pmid_elem = article.find('.//PMID')
            if pmid_elem is not None:
                article_data['pmid'] = pmid_elem.text
            
            # Extract Article Title
            title_elem = article.find('.//ArticleTitle')
            if title_elem is not None:
                article_data['title'] = title_elem.text
            
            # Extract Journal Title
            journal_elem = article.find('.//Journal/Title')
            if journal_elem is not None:
                article_data['journal'] = journal_elem.text
            
            # Extract Publication Date
            pub_date = article.find('.//PubDate')
            if pub_date is not None:
                year_elem = pub_date.find('Year')
                month_elem = pub_date.find('Month')
                day_elem = pub_date.find('Day')
                
                date_parts = []
                if year_elem is not None:
                    date_parts.append(year_elem.text)
                if month_elem is not None:
                    date_parts.append(month_elem.text)
                if day_elem is not None:
                    date_parts.append(day_elem.text)
                
                article_data['publication_date'] = '-'.join(date_parts) if date_parts else None
            
            # Extract Abstract
            abstract_elem = article.find('.//Abstract/AbstractText')
            if abstract_elem is not None:
                article_data['abstract'] = abstract_elem.text
            
            # Extract Authors
            authors = []
            author_list = article.find('.//AuthorList')
            if author_list is not None:
                for author in author_list.findall('Author'):
                    last_name_elem = author.find('LastName')
                    fore_name_elem = author.find('ForeName')
                    
                    author_name = ""
                    if last_name_elem is not None:
                        author_name += last_name_elem.text
                    if fore_name_elem is not None:
                        author_name += f", {fore_name_elem.text}"
                    
                    if author_name:
                        authors.append(author_name)
            
            article_data['authors'] = authors
            
            # Extract DOI
            doi_elem = article.find('.//ELocationID[@EIdType="doi"]')
            if doi_elem is not None:
                article_data['doi'] = doi_elem.text
            
            articles.append(article_data)
        
        return {
            'file': xml_file,
            'article_count': len(articles),
            'articles': articles
        }
        
    except ET.ParseError as e:
        print(f"Error parsing XML file {xml_file}: {e}")
        return None
    except Exception as e:
        print(f"Error processing file {xml_file}: {e}")
        return None

def process_all_xml_files() -> List[Dict]:
    """
    Process all XML files in the current directory
    
    Returns:
        List[Dict]: List of parsed data from all XML files
    """
    xml_files = get_xml_files()
    print(f"Found {len(xml_files)} XML files to process")
    
    results = []
    for xml_file in xml_files:
        print(f"Processing: {xml_file}")
        result = parse_pubmed_xml(xml_file)
        if result:
            results.append(result)
            print(f"  - Found {result['article_count']} articles")
        else:
            print(f"  - Failed to parse {xml_file}")
    
    return results

def print_summary(results: List[Dict]):
    """
    Print a summary of the processed XML files
    
    Args:
        results (List[Dict]): List of parsed results
    """
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    total_files = len(results)
    total_articles = sum(result['article_count'] for result in results)
    
    print(f"Total XML files processed: {total_files}")
    print(f"Total articles found: {total_articles}")
    
    if results:
        print(f"\nFiles processed:")
        for result in results:
            print(f"  - {result['file']}: {result['article_count']} articles")

def print_sample_articles(results: List[Dict], max_articles: int = 5):
    """
    Print sample articles from the processed results
    
    Args:
        results (List[Dict]): List of parsed results
        max_articles (int): Maximum number of articles to display
    """
    print(f"\n" + "="*60)
    print(f"SAMPLE ARTICLES (showing up to {max_articles} per file)")
    print("="*60)
    
    for result in results:
        print(f"\nFile: {result['file']}")
        print("-" * 40)
        
        for i, article in enumerate(result['articles'][:max_articles]):
            print(f"\nArticle {i+1}:")
            print(f"  PMID: {article.get('pmid', 'N/A')}")
            print(f"  Title: {article.get('title', 'N/A')}")
            print(f"  Journal: {article.get('journal', 'N/A')}")
            print(f"  Date: {article.get('publication_date', 'N/A')}")
            print(f"  DOI: {article.get('doi', 'N/A')}")
            
            authors = article.get('authors', [])
            if authors:
                print(f"  Authors: {', '.join(authors[:3])}{'...' if len(authors) > 3 else ''}")
            
            abstract = article.get('abstract', '')
            if abstract:
                print(f"  Abstract: {abstract[:200]}{'...' if len(abstract) > 200 else ''}")

def main():
    """
    Main function to process all XML files
    """
    print("PubMed XML File Processor")
    print("="*40)
    
    # Process all XML files
    results = process_all_xml_files()
    
    if not results:
        print("No XML files were successfully processed.")
        return
    
    # Print summary
    print_summary(results)
    
    # Print sample articles
    print_sample_articles(results)
    
    # Save results to a summary file
    save_summary_to_file(results)

def save_summary_to_file(results: List[Dict], output_file: str = "pubmed_summary.txt"):
    """
    Save a summary of the results to a text file
    
    Args:
        results (List[Dict]): List of parsed results
        output_file (str): Output file name
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("PubMed XML Processing Summary\n")
            f.write("="*40 + "\n\n")
            
            total_files = len(results)
            total_articles = sum(result['article_count'] for result in results)
            
            f.write(f"Total XML files processed: {total_files}\n")
            f.write(f"Total articles found: {total_articles}\n\n")
            
            for result in results:
                f.write(f"File: {result['file']}\n")
                f.write(f"Articles: {result['article_count']}\n")
                f.write("-" * 30 + "\n")
                
                for i, article in enumerate(result['articles']):
                    f.write(f"\nArticle {i+1}:\n")
                    f.write(f"  PMID: {article.get('pmid', 'N/A')}\n")
                    f.write(f"  Title: {article.get('title', 'N/A')}\n")
                    f.write(f"  Journal: {article.get('journal', 'N/A')}\n")
                    f.write(f"  Date: {article.get('publication_date', 'N/A')}\n")
                    f.write(f"  DOI: {article.get('doi', 'N/A')}\n")
                    
                    authors = article.get('authors', [])
                    if authors:
                        f.write(f"  Authors: {', '.join(authors)}\n")
                    
                    abstract = article.get('abstract', '')
                    if abstract:
                        f.write(f"  Abstract: {abstract}\n")
                
                f.write("\n" + "="*50 + "\n\n")
        
        print(f"\nSummary saved to: {output_file}")
        
    except Exception as e:
        print(f"Error saving summary to file: {e}")

if __name__ == "__main__":
    main() 