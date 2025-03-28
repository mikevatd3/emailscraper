import json
from pathlib import Path
from shutil import copy
import requests

from emailscraper.inbox import setup_inbox
from emailscraper.dataset import build_dataset
from emailscraper import setup_logging


def extract_mischooldata_from_email():
    # Open directory map configuration
    directory_map = json.loads((Path.cwd() / "conf" / "directory_map.json").read_text())

    logger = setup_logging()

    logger.info("Connecting to inbox.")
    inbox = setup_inbox(logger)

    logger.info("Finding recent messages from mischooldata.")
    messages = inbox.find_valid_mischooldata_messages()


    logger.info(f"Found {len(messages)} datasets to download.")
    for message in messages:
        dataset = build_dataset(message)
        logger.info(f"Downloading and saving {dataset.filename}.")

        file = requests.get(dataset.dl_link, verify=False)

        save_path = (
            Path("V:") /
            "DATA" /
            "Education" /
            directory_map[dataset.raw_name] /
            "Data" /
            dataset.year /
            "Raw" /
            f"{dataset.raw_name}_{dataset.year}.csv"
        )

        with open(save_path, "wb") as f:
            f.write(file.content)

        logger.info(f"Finished downloading and saving {dataset.name}")


if __name__ == "__main__":
    extract_mischooldata_from_email()