#!/usr/bin/env python3
"""
Script to sort article_ids.csv by the first column (pmid) and remove duplicate entries.
"""

import pandas as pd
import sys

def sort_and_deduplicate_csv(input_file, output_file=None):
    """
    Sort CSV file by first column and remove duplicates based on first column.
    
    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to output CSV file (optional, defaults to input_file)
    """
    try:
        # Read the CSV file
        print(f"Reading {input_file}...")
        df = pd.read_csv(input_file)
        
        # Get original row count
        original_count = len(df)
        print(f"Original row count: {original_count}")
        
        # Sort by first column (pmid)
        print("Sorting by first column (pmid)...")
        df_sorted = df.sort_values(by=df.columns[0])
        
        # Remove duplicates based on first column, keeping the first occurrence
        print("Removing duplicates based on first column...")
        df_deduplicated = df_sorted.drop_duplicates(subset=[df.columns[0]], keep='first')
        
        # Get final row count
        final_count = len(df_deduplicated)
        removed_count = original_count - final_count
        
        print(f"Final row count: {final_count}")
        print(f"Removed {removed_count} duplicate rows")
        
        # Determine output file
        if output_file is None:
            output_file = input_file
        
        # Write the result back to file
        print(f"Writing sorted and deduplicated data to {output_file}...")
        df_deduplicated.to_csv(output_file, index=False)
        
        print("Successfully completed sorting and deduplication!")
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    """Main function to handle command line arguments and execute the script."""
    if len(sys.argv) < 2:
        print("Usage: python sort_and_deduplicate_csv.py <input_file> [output_file]")
        print("Example: python sort_and_deduplicate_csv.py article_ids.csv")
        print("Example: python sort_and_deduplicate_csv.py article_ids.csv sorted_article_ids.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    sort_and_deduplicate_csv(input_file, output_file)

if __name__ == "__main__":
    main() 