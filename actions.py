import os
import shutil
import subprocess
from github import GitHub
from pathlib import Path

import utils

def response_bfm_confirm(say, client):
  last_monday = utils.get_last_monday()
  last_monday_nodash = ''.join(str(last_monday).split('-'))

  baseline_csv_folder_path = Path("../covidModels/weekly-submission/forecasts/COVIDhub-baseline")
  baseline_csv_file_path = baseline_csv_folder_path/f"{last_monday}-COVIDhub-baseline.csv"
  hub_path = Path("../covid19-forecast-hub")
  baseline_folder_in_hub_path = hub_path/"data-processed"/"COVIDhub-baseline"

  # save current dir
  saved_dir = os.curdir

  # change to hub dir
  os.chdir(hub_path)
  
  # fetch & pull
  subprocess.run(["git", "fetch", "&", "git", "pull"])

  # make new branch (baseline-<today's date>)
  new_branch_name = f"baseline-{last_monday_nodash}"
  subprocess.run(["git", "checkout", "-b", new_branch_name])

  # copy CSV from covidModels to hub
  shutil.copy(baseline_csv_file_path, baseline_folder_in_hub_path)

  # add and commit
  subprocess.run(["git", "add", "-A"])
  subprocess.run(["git", "commit", "-m", f"\"baseline build, {last_monday_nodash}\""])

  # push to origin
  subprocess.run(["git", "push", "--set-upstream", "origin", new_branch_name])

  # make PR with pygithub:
  #   (req.) head = branch/commit from
  #   (req.) base = branch to
  #          title = title of PR
  #          body = body of PR
  #          issue = link
  g = GitHub(os.getenv("GH_TOKEN"))
  repo = g.get_repo("reichlab/covid19-forecast-hub")
  head = new_branch_name
  base = "test"
  title = f"baseline build, {last_monday_nodash}"
  body = f'''
## Description

baseline build, {last_monday_nodash}

- Team name: COVIDhub-baseline
- Model name that is being updated: baseline

  '''
  repo.create_pull(title=title, body=body, head=head, base=base)

  # change back to main branch
  subprocess.run(["git", "checkout", "master"])

  # change back to previous dir
  os.chdir(saved_dir)
