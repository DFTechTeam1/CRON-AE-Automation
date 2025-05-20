import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.monitor import DataMonitoring
from utils.helper import save_json, load_json
from utils.logger import logging
from services.ftp import NasFTP
from src.secret import NAS_HOST, NAS_PASSWORD, NAS_PORT, NAS_USERNAME, NAS_OUTPUT


PROJECT_DIR = Path(__file__).resolve().parents[1]
MOUNT_DIR = os.path.join(PROJECT_DIR, 'mount')
FINISHED_JSON_PATH = os.path.join(
    MOUNT_DIR, '192.168.100.104', 'Database_Asset_3', 'ae_auto_asset', 'json', 'is_finished.json'
)
QUEUE_JSON_PATH = os.path.join(PROJECT_DIR, 'json', 'queue.json')

data = DataMonitoring()
ftp = NasFTP(username=NAS_USERNAME, password=NAS_PASSWORD, port=NAS_PORT, host=NAS_HOST)

finished_entry = load_json(filepath=FINISHED_JSON_PATH)
if finished_entry:
    asset = data.extract(MOUNT_DIR, 'psd')
    template = data.extract(MOUNT_DIR, 'aep')

    formatted = data.format(assets=asset, templates=template)
    filtered_entry = [entry for entry in formatted if entry not in finished_entry]

    save_json(QUEUE_JSON_PATH, data=filtered_entry)
    ftp.upload(remote_path=NAS_OUTPUT, local_path=QUEUE_JSON_PATH)
else:
    logging.warning('Skip updating entry. Comparing json file not found.')
