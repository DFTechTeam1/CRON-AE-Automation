import json
import os
from pathlib import Path
from utils.logger import logging


def save_json(destination: str, data: dict) -> None:
    logging.info(f'Data saved to {destination}.')
    file = open(destination, 'w')
    try:
        json.dump(data, file, indent=4)
    finally:
        file.close()
    return


def load_json(filepath: str) -> dict:
    if os.path.exists(filepath):
        logging.info(f'Loading JSON data from {filepath}.')
        return json.loads(Path(filepath).read_text())
    logging.warning(f'JSON file: {filepath} not exist! Skipping.')
