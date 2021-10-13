import os
import logging
from slack_bolt import App

# internal components
from config import parse_config_file
import home
import slash_commands
import actions
import ui_components

# logging setup
logger = logging.getLogger("casebot")
logger.setLevel(logging.DEBUG)

# get config variables
PORT, TOKEN, SECRET = parse_config_file()

# make app
app = App(token=TOKEN, signing_secret=SECRET)

### bot configurations ###

# home tab
@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    home.update_home_tab(client, event, logger)

# actions (button events)
# maps action ids to functions in actions.py
actions_dict = {
    "bfm_confirm": actions.response_bfm_confirm
}

@app.action("bfm_confirm")
def dispatch_baseline_pr(ack, say, respond, client):
    # acknowledge the command
    # (must be done, otherwise Slack will show error)
    ack()
    respond(text=ui_components.bfm_confirm(), replace_original=True)
    try:
        actions_dict["bfm_confirm"](say, client)
        say("PR successfully created.")
    except:
        say("Could not create PR; please check VM logs for details.")

@app.action("bfm_deny")
def denied_baseline_pr(ack, respond):
    ack()
    respond(text=ui_components.bfm_deny(), replace_original=True)

# slash commands
# maps command strings to functions in slash_commands.py
slash_commands_dict = {
    "hello": slash_commands.respond_hello,
    "build": slash_commands.respond_build
}

@app.command("/casebot")
def dispatch_slash_command(ack, say, command, client):
    # acknowledge the command
    # (must be done, otherwise Slack will show error)
    ack()

    # parse the first phrase (use space as separator)
    arguments = command["text"].split(" ")
    subcommand = arguments[0]
    try:
        slash_commands_dict[subcommand](say, command, client, arguments[1:])
    except KeyError:
        say("Sorry, I don't understand that command. Maybe we can add it as a new one?")

    logging.info(command)

### end bot configurations ###

# entry point
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", PORT)))