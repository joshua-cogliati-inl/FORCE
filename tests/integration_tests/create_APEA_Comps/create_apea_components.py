# Copyright 2022, Battelle Energy Alliance, LLC
# ALL RIGHTS RESERVED
"""
Creating the Aspen APEA components from the HYSYS output files.

It takes the following argument:
1 - A folder that contains the Aspen APEA xlxs output files

Example
python create_apea_components.py APEA_outputs/
"""
#!/usr/bin/env python
import sys
import os
import argparse
sys.path.append(os.path.dirname(__file__).split("FORCE")[:-1][0]+"FORCE/src")
from apea import extract_all_apea_components

# # Specifying terminal command arguments
if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    description="Extract all the APEA components"
  )
  # Inputs from the user
  parser.add_argument("apea_xlsx_outputs_folder_path", help="apea_xlsx_outputs_folder_path")
  args = parser.parse_args()

  extract_all_apea_components(args.apea_xlsx_outputs_folder_path)