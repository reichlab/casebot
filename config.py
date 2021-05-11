import os
import yaml

CONFIG_FILE_PATH = "./config.yml"

def parse_config_file():
  # read in config file
  with open(CONFIG_FILE_PATH, "r") as config_file:
    config = yaml.safe_load(config_file.read())

  bot_token = os.environ.get(config.env.bot_token.name) \
    if not config.env.bot_token.value \
    else config.env.bot_token.value

  secret = os.environ.get(config.env.signing_secret.name) \
    if not config.env.signing_secret.value \
    else config.env.signing_secret.value

  return bot_token, secret