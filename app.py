from slack_bolt import App
from config import parse_config_file
from home import *

# entry point
TOKEN, SECRET = parse_config_file()
APP = App(token=TOKEN, signing_secret=SECRET)

# home tab
@APP.event("app_home_opened")
def get_home_tab(client, event, logger):
  update_home_tab(client, event, logger)

# Start your app
if __name__ == "__main__":
  APP.start()