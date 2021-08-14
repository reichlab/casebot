import os
import json
from types import SimpleNamespace

CONFIG_FILE_PATH = "../config.json"

def parse_config_file():
  with open(CONFIG_FILE_PATH, "r") as config_file:
    config = json.load(config_file, object_hook=lambda d: SimpleNamespace(**d))

  port = config.port

  token = os.environ.get(config.env.bot_token.name) \
    if not config.env.bot_token.value \
    else config.env.bot_token.value

  secret = os.environ.get(config.env.signing_secret.name) \
    if not config.env.signing_secret.value \
    else config.env.signing_secret.value

  return port, token, secret

