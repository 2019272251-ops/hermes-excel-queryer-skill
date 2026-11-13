#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Find the row where 标签 ID (Label ID) equals 4096
"""

import pandas as pd
import re

csv_file = '/opt/data/network_equipment_网络机房.csv'

print("=" * 60)
print("FINDING ROW WHERE 标签 ID = 4096")
print("=" * 60 + "\n")

try:
    print(f"Reading CSV file: {csv_file}")
    df = pd.read_csv(csv_file, encoding='utf-8')

    # Display column names with indices
    col_names = [str(col) for col in df.columns]
    
    # Show column info
    print("\nAll columns:")
    for idx, col in enumerate(df.columns):
        print(f"  {idx}: '{col}'")

    # Find '标签 ID' or similar ID columns
    tag_id_cols = []
    for i, col in enumerate(col_names):
        if 'ID' in col:
            tag_id_cols.append((i, col))
    
    print("\n" + "=" * 60)
    if tag_id_cols:
        print(f"FINDING ROWS WHERE '{tag_id_cols[0][1]}' = 4096")
        for idx, col in tag_id_cols:
            print(f"Column index {idx}: '{col}'")
        
        # Try to find rows where the ID column equals 4096
        try:
            # Convert all columns with 'ID' to numeric if needed
            for col_idx, col_name in tag_id_cols:
                df[col_names[col_idx]] = pd.to_numeric(df[col_names[col_idx]], errors='coerce')
            
            df_filtered = df[df[tag_id_cols[0][1]].astype(float) == 4096]
            
            print(f"\n{'='*60}")
            print(f"Found {len(df_filtered)} row(s) where '{tag_id_cols[0][1]}' == 4096")
            print(f"{'='*60}")
            
            if len(df_filtered) > 0:
                for idx, row in df_filtered.iterrows():
                    print(f"\nRow {idx + 1} Data:")
                    
                    # Print all values with column names
                    for col_name in df.columns:
                        value = row[col_name]
                        if isinstance(value, float) and pd.isna(value):
                            print(f"    {col_name}: (null)")
                        else:
                            print(f"    {col_name}: {value}")
            else:
                print("\nNo rows found with 标签 ID = 4096")
                
        except Exception as e:
            print(f"\nConversion error: {e}")
            # Try without conversion - search strings
            for idx, row in df.iterrows():
                for col_idx, col_name in tag_id_cols:
                    if str(row[col_names[col_idx]]).strip() == '4096':
                        print(f"\nRow {idx + 1} found with string match:")
                        for col_name in df.columns:
                            val = row[col_name]
                            if pd.isna(val):
                                val_str = "(null)"
                            else:
                                val_str = str(val)
                            print(f"    {col_name}: {val_str}")
                        
    else:
        print("\nERROR: No column found with 'ID' in name")

except Exception as e:
    print(f"\nError reading file: {e}")
