---
name: excel-file-queryer
description: "Query data from Excel files by column name, particularly for Chinese character headers with float64 conversion handling."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Excel, Data Querying, Pandas, Unicode Handling]
    related_skills: [powerpoint, ocr-and-documents, data-science]
---

# Excel File Queryer Skill

## Overview

This skill enables querying data from Excel files using column names. It handles:
- Chinese/Unicode character column headers
- Float64-to-string conversion (common in Excel when storing values like "3.5" or U numbers)
- Multiple sheet processing
- Robust error handling for encoding issues

## Problem Statement

Excel files often store values as float64 in pandas, which can lead to issues displaying values like "3.5" vs "." or causing comparison failures. Additionally, Chinese character headers require proper Unicode handling.

## Use Case: Querying Equipment Data

```python
# Example query for equipment row with specific label ID
query_result = query_excel_file(
    file_path='/opt/data/网络机房设备信息表（含内部编码）.xlsx',
    sheet_name='网络机房',
    column_names=['标签 ID'],
    value=4096,
    return_format='table'  # dict or DataFrame row
)

# Output:
# Row 2 Data:
#     标签ID: 4096.0
#     机柜编号：(null)
#     设备型号：Huawei S6720-30C-EI-24S
#     设备类型：交换机
```

## How to Run Excel Queries

### Step 1: Verify pandas is installed

```bash
/usr/bin/python3 -c 'import pandas; print(f"Pandas {pandas.__version__} installed')"
```

### Step 2: Execute the query script with arguments

```bash
# Basic usage
python3 scripts/excel_queryer.py --query "标签ID" 4096 "/opt/data/网络机房设备信息表（含内部编码）.xlsx"

# Find all rows matching criteria in a sheet
python3 scripts/excel_queryer.py --columns "标签 ID,设备型号,设备类型" --value "Huawei S6720-30C-EI-24S" "/path/to/file.xlsx"

# Query multiple sheets at once
python3 scripts/excel_queryer.py --sheets "网络机房,应用机房" --query "资产编号"  "/path/to/file.xlsx"
```

### Step 3: Get formatted results as table or list

```python
result = query_excel_file(
    file_path='/opt/data/网络机房设备信息表（含内部编码）.xlsx',
    sheet_name='网络机房',
    column_names=['标签 ID'], value=4096,
    return_format='table'
)

# result is:
# {<IndexSlice>: [(Row data from matching row)]}
```

## Code Template for Reuse

This skill includes two reusable scripts in the scripts/ directory:

1. **find_row.py** - Quick usage example to find a specific row
2. **excel_queryer.py** - Full interactive CLI tool with options

### Key Script Features:

- **Type conversion**: `f8` dtype preserves "3.5" format as string, handles null values from Excel
- **Chinese column support**: Handles headers with Chinese characters like `标签 ID`, `机柜 编号`
- **Flexibility**: Supports querying by single value or multiple columns AND values
- **Error handling**: Falls back to openpyxl engine if pandas encounters encoding issues

## Common Patterns

### Pattern 1: Query by single column, single value

```bash
python3 scripts/excel_queryer.py \
  --query "标签 ID" \
  '4096' \
  '/opt/data/网络机房设备信息表（含内部编码）.xlsx'
```

### Pattern 2: Query by multiple columns, AND logic

```bash
python3 scripts/excel_queryer.py \
  --columns "标签 ID,资产编号" \
  '4096,H2107875' \
  '/opt/data/网络机房设备信息表（含内部编码）.xlsx'
```

### Pattern 3: Query by device model across all sheets

```bash
python3 scripts/excel_queryer.py \
  --columns "设备型号" \
  'H3C UniServer R4900 G3' \
  '/opt/data/网络机房设备信息表（含内部编码）.xlsx'
```

### Pattern 4: Check if a value exists in cell (case-insensitive)

```bash
python3 scripts/excel_queryer.py \
  --columns "设备型号,设备类型" \
  'Dell PowerEdge,RAC' \
  '/opt/data/网络机房设备信息表（含内部编码）.xlsx'
```

### Pattern 5: Export results to CSV after query

The script automatically creates CSV files in the current working directory (e.g., ./network_equipment_网络机房.csv).

## Error Handling Scenarios

| Scenario | Expected Outcome |
|-----------|------------------|
| Invalid column name | Show warning; try to search similar columns |
| Value not found in sheet | Print "No rows match criteria" |
| Encoding failure | Fall back to openpyxl engine with string conversion |
| Empty cell handling | Display as `(null)` in output |

## Troubleshooting

### Issue: Float values show as "." instead of format

**Cause**: pandas stores 3.5 as float64; Excel might not load correctly  
**Fix**: The skill automatically converts `f8` columns to strings if needed, preserving "3.5" format

### Issue: Chinese characters displayed incorrectly

**Cause**: CSV saved UTF-8-sig for Excel compatibility; some editors default to ISO-8859-1  
**Fix**: The script saves with proper encoding; use `codepage=65001` parameter in terminal

## Related Resources

### Column Name Translation Reference

| Chinese | English | Example |
|---------|---------|----------|
| 标签 ID | Label ID | Primary equipment identifier |
| 机柜编号 | Rack Number | Physical rack unit |
| 运行中心编号 | Operation Center ID | Central server code (e.g., XHB02-20200001) |

### Common Equipment Types

- `交换机` - Switch
- `服务器` - Server  
- `防火墙` - Firewall/Security Gateway
- `存储服务器` - Storage Server
- `磁盘阵列` - SAN Storage Array

## Usage Tips

1. **Always verify column indexing**: Column names may have hidden whitespace or special characters
2. **Use quotes for values with spaces**: Single/double quote strings in command line argument
3. **Check return formats**: Use `return_format='dict'` for easy JSON serialization later
4. **Multiple value matching**: Combine multiple columns/values with AND (`"A,B"` → A AND B)

## Quick Start Checklist

1. ✓ Python 3.x installed locally
2. ✓ pandas >= 2.0 available via apt (`python3-pandas `or pip)
3. ✓ Excel file has proper UTF-8 encoding
4. ✓ CSV output directory writable (`/opt/data/`)

---

**Author**: Hermes Agent  
**Last Updated**: 2026
**Tested On**: Ubuntu 13+ with Python 3.13+, pandas 2.x, xlrd/openpyxl
