import os
import json
from pathlib import Path
from pprint import pprint

# setup
# read all JSON components from ui-components/
components_path_list = {
  entry.name.split(".")[0] : entry.path for entry in os.scandir(Path("./ui-components"))
  if entry.is_file() and entry.name.endswith(".json")
}

def bfm():
  with open(components_path_list["baseline-finished-message"]) as f:
    return json.load(f)

def bfm_confirm():
  with open(components_path_list["baseline-finished-message-confirm"]) as f:
    return json.load(f)

def bfm_deny():
  with open(components_path_list["baseline-finished-message-deny"]) as f:
    return json.load(f)