import os
from slack_bolt import App
from config import parse_config_file
import home

# entry point
PORT, TOKEN, SECRET = parse_config_file()
APP = App(token=TOKEN, signing_secret=SECRET)

# home tab
@APP.event("app_home_opened")
def update_home_tab(client, event, logger):
  home.update_home_tab(client, event, logger)

# Start your app
if __name__ == "__main__":
  APP.start(port=int(os.environ.get("PORT", PORT)))