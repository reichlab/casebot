import os
import pyyaml
# Use the package we installed
from slack_bolt import App

# Initializes your app with your bot token and signing secret


# Add functionality here
def start_app():

  app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
  )

  app.start()

# Start your app
if __name__ == "__main__":
  start_app()