#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Excel File Queryer - Reusable Script for Querying Excel Files by Column Name

This script handles querying data from Excel files with proper Unicode/Chinese 
column header support and float-to-string conversion.

Usage:
    /usr/bin/python3 excel_queryer.py --columns <col1,col2,...> \
        <value1,value2,...> \
        <excelfilepath> [OPTIONS]

Examples:
    # Find row with Label ID = 4096
    /usr/bin/python3 excel_queryer.py --columns "标签ID" "4096" ...xlsx

    # Find row with specific device model
    /usr/bin/python3 excel_queryer.py --columns "设备型号" "Dell PowerEdge R710" ...xlsx

    # Query multiple columns (AND logic)
    /usr/bin/python3 excel_queryer.py --columns "标签ID,资产编号" "4096,H2107875" ...xlsx
"""

import argparse
import pandas as pd
import os
import sys
from pathlib import Path


# ============================================================================
# Configuration
# ============================================================================

DEFAULT_EXCEL_FILE = '/opt/data/网络机房设备信息表（含内部编码）.xlsx'
OUTPUT_DIR = '/opt/data/query_results'

# Column name pattern for float64 values (Excel often stores U numbers, heights, etc.)
FLOAT_COL_PATTERN = r'[a-zA-Z][\s\S]*?[fF]8$'  # Regex matching column with f8 dtype


def load_excel_file(filepath: str, verbose: int = 1) -> pd.DataFrame:
    """
    Load Excel file with proper encoding handling for Chinese characters.
    
    Args:
        filepath: Path to Excel file
        verbose: Verbosity level (0=minimal, 1=normal, 2=debug)
        
    Returns:
        DataFrame with proper dtype handling
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If parsing fails
    """
    log_msg(f"Reading Excel file from: {filepath}", verbose)
    
    try:
        # Try openpyxl engine first (better Unicode support)
        df = pd.read_excel(
            filepath, 
            dtype={'f8': str},  # Convert float64 to string
            na_values='NULL',
            on_bad_lines='skip',
        )
    except Exception as e:
        error_msg = f"Failed to read with openpyxl: {e}"
        log_msg(error_msg, verbose)
        
        # Fallback to pandas default engine (xlrd/openpyxl)
        try:
            df = pd.read_excel(filepath, usecols=None)
            # Apply dtype conversion after reading
            for col in df.columns:
                if 'float64' in str(df[col].dtype):
                    log_msg(f"Converting '{col}' (float64 → string)", verbose)
                    df[col] = df[col].astype(str)
        except Exception as e2:
            raise ValueError(f"Failed to load Excel file ({filepath}): {e} {e2}")

    n_rows = len(df), n_cols = len(df.columns)
    log_msg(f"Loaded {n_rows} rows × {n_cols} columns", verbose)
    
    return df


def parse_column_value_spec(raw_input: str, n_columns: int) -> list:
    """
    Parse the --columns and --value arguments into proper lists.
    
    Args:
        raw_input: Comma-separated input string (e.g., "列1,列2")
        n_columns: Number of columns/values expected
        
    Returns:
        List of strings matching expected count
    """
    values = raw_input.split(',') if raw_input.strip() else []
    
    # Handle trailing comma in value list
    while len(values) == 0 or (len(values) == 1 and len(values[0]) == 0):
        if raw_input.endswith(','):
            continue
    
    return [v.strip() for v in values]


def execute_query(
    df: pd.DataFrame, 
    sheet_name: str,
    cols_spec: list,
    values_spec: list,
    file_path: str
) -> pd.DataFrame:
    """
    Execute simple query matching specific column and value.
    
    Args:
        df: DataFrame from loaded Excel file
        sheet_name: Sheet name to query from
        cols_spec: List of column names to match
        values_spec: Values to match
        file_path: Path for logging
        
    Returns:
        DataFrame with matching rows
    """
    log_msg(f"Querying [{sheet_name}] for columns: {cols_spec}", 1)
    
    if sheet_name not in df.columns:
        # Convert to lowercase for case-insensitive search
        sheet_names = [str(c) for c in df.columns]
        exact_names = [cn for cn in sheet_names if str(cn).strip().lower() == sn.strip().lower() 
                      for sn in cols_spec]
        log_msg(f"Trying alternative sheet matching: {exact_names}", 2)
    
    matched_cols = cols_spec[:1]  # Default to first column for simple search
    
    # Build query condition (AND logic)
    conditions = []
    values = {}
    
    for i, col in enumerate(cols_spec):
        if i >= len(values_spec):
            continue
            
        val_to_match = [v.strip() for v in values_spec[:1]]  # Default to first value
        
        try:
            df_matched = df[col] == val_to_match[0]
        except (TypeError, ValueError):
            log_msg(f"Warning: Column '{col}' comparison failed", 2)
            continue
    
    # Execute and return matching rows
    if not conditions:
        log_msg("WARNING: No query specification provided", 1)
        return df[['标签 ID']].head(1)
    
    print("=" * 60)
    log_msg(f"Search criteria in [{sheet_name}]:", 1)
    for col in cols_spec[:len(vals)]:
        val = values[vals.pop()]
        log_msg(f"     {col}: '{val}'", 2)
