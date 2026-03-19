import sqlite3
import pandas as pd
import os

def export_to_csv():
    print("--- Exporting Database for Looker Studio ---")
    
    if not os.path.exists('animals.db'):
        print("Error: animals.db not found!")
        return
        
    conn = sqlite3.connect('animals.db')
    
    # Load into DataFrame
    query = "SELECT * FROM species"
    df = pd.read_sql_query(query, conn)
    
    import re
    
    def extract_speed(s):
        if not s: return None
        # Find first number (usually mph)
        nums = re.findall(r"(\d+(?:\.\d+)?)", str(s))
        return float(nums[0]) if nums else None

    def extract_weight(s):
        if not s: return None
        s_low = str(s).lower()
        nums = re.findall(r"(\d+(?:\.\d+)?)", s_low)
        if not nums: return None
        val = float(nums[0].replace(',', ''))
        
        # Simple unit detection
        if 'kg' in s_low: return val
        if 'lb' in s_low: return val * 0.453592
        if 'oz' in s_low or ' g ' in s_low or s_low.endswith('g'): return val / 1000.0
        return val

    print("Cleaning numerical data...")
    df['weight_kg'] = df['weight'].apply(extract_weight)
    df['top_speed_mph'] = df['top_speed'].apply(extract_speed)
    
    # Add a lowercase version for case-insensitive searching in Looker Studio
    df['name_lower'] = df['name'].str.lower()
    
    # Export to CSV
    output_file = 'species_export.csv'
    df.to_csv(output_file, index=False)
    
    print(f"Success! Exported {len(df)} records to '{output_file}'.")
    print("You can now upload this file to Google Sheets for Looker Studio.")
    
    conn.close()

if __name__ == "__main__":
    export_to_csv()
