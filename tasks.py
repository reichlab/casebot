import subprocess
import os
from pathlib import Path

COVID_MODELS_DIR = Path("/code/reichlab/covidModels/weekly-submission")

def baseline():
  # run make all in covidModels directory
  result = subprocess.run([
    "make",                                   # make
    "-C",                                     # directory flag
    f"{COVID_MODELS_DIR}/weekly-submission",  # covidModels does its make in weekly-submission
    "all"                                     # all
  ])
  
  # return path to plot folder and CSV folder
  # return None if make all failed
  if result.returncode != 0:
    # save output from result to log file
    
    return (1, FileNotFoundError)
  else:
    return (0, COVID_MODELS_DIR/"COVIDhub-baseline-plots")