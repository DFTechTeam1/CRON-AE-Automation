import sys
import os
from utils.logger import logging
from typing import Optional
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))


class DataMonitoring:
    def __init__(self):
        pass

    def format(self, assets: list, templates: list) -> Optional[dict]:
        return [
            {
                'asset_path': asset,
                'template_path': template,
                'output_path': '192.168.100.104/Database_Asset_3/ae_auto_asset/Output',
            }
            for asset in assets
            for template in templates
        ]

    def extract(self, path: str, endswith: str) -> list:
        found_files = []

        for root, dirs, files in os.walk(path):
            for filename in files:
                if filename.lower().endswith((endswith)):
                    fullpath = os.path.join(root, filename)
                    if not os.path.exists(fullpath):
                        logging.warning(f'File {fullpath} does not exist.')
                    else:
                        relative_path = fullpath.split('mount/')[1]
                        found_files.append(relative_path)
        if not found_files:
            raise FileNotFoundError(
                f"No file with extension {endswith} found! Please ensure data is already mounted in '{path}'."
            )

        return found_files
