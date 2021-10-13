from typing import Tuple
import os
import json
from types import SimpleNamespace

CONFIG_FILE_PATH: str = "./config.json"

def parse_config_file() -> Tuple[str, str, str]:
    with open(CONFIG_FILE_PATH, "r") as config_file:
        config: object = json.load(config_file, object_hook=lambda d: SimpleNamespace(**d))

    port: str = config.port

    token: str = os.environ.get(config.env.bot_token.name) \
        if not config.env.bot_token.value \
        else config.env.bot_token.value

    secret: str = os.environ.get(config.env.signing_secret.name) \
        if not config.env.signing_secret.value \
        else config.env.signing_secret.value

    return port, token, secret

