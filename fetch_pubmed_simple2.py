import requests
import csv

def read_pubmed_ids_from_csv(csv_file, start_row, end_row):
    """
    Read PubMed IDs from CSV file from start_row to end_row (inclusive)
    
    Args:
        csv_file (str): Path to the CSV file
        start_row (int): Starting row number (0-indexed)
        end_row (int): Ending row number (inclusive, 0-indexed)
        
    Returns:
        str: Comma-separated string of PubMed IDs
    """
    pubmed_ids = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            
            # Skip header row
            next(csv_reader)
            
            # Read rows from start_row to end_row
            for i, row in enumerate(csv_reader):
                if start_row <= i <= end_row:
                    if row and row[0].strip():  # Check if first column has data
                        pubmed_ids.append(row[0].strip())
                elif i > end_row:
                    break
                    
        return ','.join(pubmed_ids)
        
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file}' not found")
        return None
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

def fetch_pubmed_xml_simple(pubmed_id):
    """
    Simple function to fetch XML data for a PubMed ID
    
    Args:
        pubmed_id (str): The PubMed ID to fetch
        
    Returns:
        str: XML content as string
    """
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        'db': 'pubmed',
        'id': pubmed_id,
        'retmode': 'xml'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# for x0_start in range(0, 3700,100):
    # Configuration
csv_file = "alzforum_recommends_pmid_list_20250617.csv"
x0 = 3700  # Starting row (0-indexed, excluding header)
x1 = 3703  # Ending row (inclusive, 0-indexed, excluding header)

# Read PubMed IDs from CSV
pubmed_id = read_pubmed_ids_from_csv(csv_file, x0, x1)

if pubmed_id:
    print(f"Fetching XML for PubMed IDs: {pubmed_id}")
    xml_content = fetch_pubmed_xml_simple(pubmed_id)

    if xml_content:
        print("Success! XML content:")
        print("-" * 50)
        print(xml_content)
        
        # Save to file
        filename = f"pubmed_{x0}_to_{x1}.xml"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        print(f"\nXML saved to: {filename}")
    else:
        print("Failed to fetch XML")
else:
    print("Failed to read PubMed IDs from CSV") 