import os
import json
from pathlib import Path

# setup
# read all JSON components from ui-components/
components_path_list = {
  entry.name.split(".")[0] : entry.path for entry in os.scandir(Path("./ui-components"))
  if entry.is_file() and entry.name.endswith(".json")
}

def bfm():
  with open(components_path_list["baseline-finished-message"]) as bfm_json:
    return json.load(bfm_json)