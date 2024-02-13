# Copyright 2022, Battelle Energy Alliance, LLC
# ALL RIGHTS RESERVED
"""
A script that creates/updates the component sets in HERON from a set of Aspen HYSYS and APEA output xlsx files. 
The script also creates the components cost functions

This is a full test combines the functionality of other tests related to Aspen-HERON interaction:

It takes the following arguments:
1- The folder containing the HYSYS output XLSX files
2- The folder containing the APEA output XLSX files
3- A folder that contains the user-defined files that idntify which components to group together
4- The initial HERON XML file that needs to be updated

Example:
python aspen_to_heron.py HYSYS_outputs/ APEA_outputs/ Sets1/ heron_input.xml
"""


#!/usr/bin/env python
# Importing libraries and modules
import os
import sys
import argparse

# import from the vertical_inegration/src
sys.path.insert(1, os.path.dirname(__file__).split("FORCE")[:-1][0]+"FORCE/src")
import convert_utils as xm
from hysys import extract_all_hysys_components
from apea import extract_all_apea_components
from force import create_all_force_components_from_hysys_apea, extract_all_force_componentsets
from heron import create_componentsets_in_HERON


# Specifying user inputs and output file
if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    description="Starting by XLSX output files from aspen HYSYS and APEA, create the cost functions of components sets and create/upadate the component sets in the HERON input XML file"
    )
    # Inputs from the user
  parser.add_argument("hyses_xlsx_outputs_folder_path", help="hyses_xlsx_outputs_folder_path")
  parser.add_argument("apea_xlsx_outputs_folder_path", help="apea_xlsx_outputs_folder_path")
  parser.add_argument("componentSets_folder", help="The paths of folders that contain the setfiles. Setfiles are files that list the components that the user wants to group together as one list")
  parser.add_argument("HERON_Input_XML", help="The original HERON input XML file to which the new component data are transferred")
  args = parser.parse_args()
  
  print("\n",'\033[95m', "Step1 (creating HYSES and APEA components) begins", '\033[0m', "\n")
  hysys_comps_list = extract_all_hysys_components(args.hyses_xlsx_outputs_folder_path)[1]
  apea_comps_list = extract_all_apea_components(args.apea_xlsx_outputs_folder_path)[1]
  print("\n",'\033[95m', "Step1 (creating HYSES and APEA components) is complete", '\033[0m', "\n")

  print("\n",'\033[95m', "Step2 (creating HYSES and APEA FORCE components) begins", '\033[0m', "\n")
  FORCE_comps_list = create_all_force_components_from_hysys_apea( [hysys_comps_list, apea_comps_list ], args.hyses_xlsx_outputs_folder_path)[0]
  print("\n",'\033[95m', "Step2 (creating HYSES and APEA FORCE components) is complete", '\033[0m', "\n")

  

  print("\n",'\033[95m', "Step3 (creating FORCE components Sets) begins", '\033[0m', "\n")
  extract_all_force_componentsets(args.componentSets_folder, FORCE_comps_list)
  print("\n",'\033[95m', "Step3 (creating FORCE componentsSets) is complete", '\033[0m', "\n")

  print("\n",'\033[95m', "Step4 (Component Sets are loaded to the HERON input XMl file) begins", '\033[0m', "\n")
  new_HERON_tree = create_componentsets_in_HERON (args.componentSets_folder, args.HERON_Input_XML)

  parnet_folder_name = os.path.abspath(os.path.join(args.HERON_Input_XML, os.pardir))
  filename = os.path.basename(args.HERON_Input_XML)


  output_file = parnet_folder_name+"/new_"+filename
  file_exists = os.path.exists(output_file)
  if file_exists:
    os.remove(output_file)

  with open(output_file, "w", encoding="utf8") as out:
    print((xm.prettify(new_HERON_tree )), file=out)

  print (f" \n The new HERON file is updated/created at: '{output_file}' ")
  print("\n",'\033[95m',"Step4 (Component Sets are loaded to the HERON input XMl file) is complete", '\033[0m', "\n")