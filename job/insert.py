import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from services.monitor import DataMonitoring
from utils.helper import save_json
from services.ftp import NasFTP
from src.secret import NAS_HOST, NAS_PASSWORD, NAS_PORT, NAS_USERNAME, NAS_OUTPUT


PROJECT_DIR = Path(__file__).resolve().parents[1]
MOUNT_DIR = os.path.join(PROJECT_DIR, 'mount')
JSON_PATH = os.path.join(PROJECT_DIR, 'json', 'queue.json')

data = DataMonitoring()
ftp = NasFTP(username=NAS_USERNAME, password=NAS_PASSWORD, port=NAS_PORT, host=NAS_HOST)

asset = data.extract(MOUNT_DIR, 'psd')
template = data.extract(MOUNT_DIR, 'aep')
formatted = data.format(assets=asset, templates=template)
save_json(JSON_PATH, data=formatted)
ftp.upload(remote_path=NAS_OUTPUT, local_path=JSON_PATH)
