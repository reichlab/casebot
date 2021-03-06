import logging
from datetime import date
from pathlib import Path
from pprint import pprint

from slack_sdk.errors import SlackApiError

import ui_components
import utils
from tasks import baseline

logger = logging.getLogger("casebot")

LAST_MONDAY = utils.get_last_monday()
D_NAME = f"COVIDhub-baseline-{LAST_MONDAY}-deaths.pdf"
C_NAME = f"COVIDhub-baseline-{LAST_MONDAY}-cases.pdf"
H_NAME = f"COVIDhub-baseline-{LAST_MONDAY}-hospitalizations.pdf"

def respond_hello(say, command, client, args):
    say(f"Hello to you too, <@{command['user_id']}>!")
    logger.info(pprint(command))

def respond_build(say, command, client, args):
    if args[0] == "baseline":
        say("Will trigger baseline build! Please wait for the build to finish and plots to be collected.")

        # long running process...
        rv, plot_folder_path = baseline()

        # only turn on for testing
        #plot_folder_path = Path("/code/covidModels/weekly-submission/COVIDhub-baseline-plots")
        #rv = 0

        # done with build! check results
        if rv == 0:
            # try uploading file to slack
            try:
                last_monday = utils.get_last_monday()
                
                # construct filenames for deaths, cases, and hospitalizations plots
                d_plot_path = plot_folder_path/str(LAST_MONDAY)/D_NAME
                c_plot_path = plot_folder_path/str(LAST_MONDAY)/C_NAME
                h_plot_path = plot_folder_path/str(LAST_MONDAY)/H_NAME

                # get channel from which command was issued
                channel_id = command["channel_id"]

                # join channel
                client.conversations_join(channel=channel_id)

                # upload to said channel with plots
                client.files_upload(
                    channels=channel_id,
                    initial_comment=f"Deaths plot made on {last_monday}",
                    file=d_plot_path.as_posix()
                )
                client.files_upload(
                    channels=channel_id,
                    initial_comment=f"Cases plot made on {last_monday}",
                    file=c_plot_path.as_posix()
                )
                client.files_upload(
                    channels=channel_id,
                    initial_comment=f"Hospitalizations plot made on {last_monday}",
                    file=h_plot_path.as_posix()
                )

                # show modal
                modal = ui_components.bfm()
                say(modal)
                # modal button actions handled by another function

            except SlackApiError as e:
                # change this to say in a private channel.
                say("I could not upload plots to this channel. Help!")
                say("Here's what happened:")
                say(f"{e.response}")
        else:
            say("Baseline build was not successful. Please check system logs for details.")
    else:
        say("I don't know how to build that yet. Maybe we can add it as a new target?")