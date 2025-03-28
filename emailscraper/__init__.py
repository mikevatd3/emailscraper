import json
import tomllib
import logging.config
from pathlib import Path


with open(Path().cwd() / "config.toml", "rb") as f:
    config = tomllib.load(f)


def setup_logging():
    with open(Path.cwd() / "logging_config.json") as f:
        logging_config = json.load(f)

    logging.config.dictConfig(logging_config)

    return logging.getLogger(config["app"]["name"])
