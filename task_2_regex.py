"""
Task 2: Regex

Run the script using command:

python task_2_regex.py
"""
import os
import re

import pandas as pd

#ROOT_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = "candidateEvalData/dim_df_correct.csv"

dim_df = pd.read_csv(INPUT_FILE)
raw_text_series = dim_df["rawDim"]

height, width, depth = [None, None, None]

def parse_dimensions(re_pattern, raw_str):
    print(re.findall(re_pattern, raw_str)[-1])
    return re.findall(re_pattern, raw_str)[-1]

def clean_seperators(raw_vals):
    return [num.replace(',', '.') for num in raw_vals]

def parse_unit(raw_str):
    if 'in' in raw_str:
        return 2.54
    if 'mm' in raw_str:
        return 0.1
    if 'cm' in raw_str:
        return 1
    return 1

def get_dimensions(re_pattern, raw_str):
    _parsed_vals = parse_dimensions(re_pattern, raw_str)
    _clean_vals = clean_seperators(_parsed_vals)
    convert_mult = parse_unit(raw_str)

    # Padding the obtained list and reassigning individually
    ht_str, wt_str, dt_str = _clean_vals[0:3] + ([None] * ( 3 - len(_clean_vals)))

    # Converting from other units to cm
    ht = (float(ht_str) * convert_mult) if ht_str != None else None
    wt = (float(wt_str) * convert_mult) if wt_str != None else None
    dt = (float(dt_str) * convert_mult) if dt_str != None else None

    return ht, wt, dt

# Regex for Example 1
#height_str, width_str = re.findall('(\d+\.?,?\d*)', raw_text_series[0])
#height = float(height_str.replace(',', '.'))
#weight = float(weight_str.replace(',', '.'))
re_pattern = '(\d+\.?,?\d*)×(\d+\.?,?\d*)'
raw_str = dim_df['rawDim'][0]
height, width, depth = get_dimensions(re_pattern, raw_str)
print(f"Height: {height}, Width: {width}, Depth: {depth}")

# Regex for Example 2
re_pattern = '(\d+\.?,?\d*) x (\d+\.?,?\d*)'
raw_str = dim_df['rawDim'][1]
height, width, depth = get_dimensions(re_pattern, raw_str)
print(f"Height: {height}, Width: {width}, Depth: {depth}")

# Regex for Example 3
re_pattern = '(\d+\.?,?\d*) x (\d+\.?,?\d*) x (\d+\.?,?\d*)'
raw_str = re.findall('(.+?cm)', dim_df['rawDim'][2])[0]
print(raw_str)
height, width, depth = get_dimensions(re_pattern, raw_str)
print(f"Height: {height}, Width: {width}, Depth: {depth}")

# Regex for Example 4
re_pattern = '(\d+\.?,?\d*) × (\d+\.?,?\d*) cm'
raw_str = re.findall('\((.+?cm)\)', dim_df['rawDim'][3])[-1]
height, width, depth = get_dimensions(re_pattern, raw_str)
print(f"Height: {height}, Width: {width}, Depth: {depth}")

# Regex for Example 5
re_pattern = '(\d+\.?,?\d*) by (\d+\.?,?\d*)'
raw_str = dim_df['rawDim'][4]
height, width, depth = get_dimensions(re_pattern, raw_str)
print(f"Height: {height}, Width: {width}, Depth: {depth}")
