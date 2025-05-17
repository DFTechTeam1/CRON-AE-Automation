import os
from dotenv import load_dotenv
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]

env_file = os.getenv('ENV_FILE', os.path.join(PROJECT_DIR, 'env', '.env.development'))

if os.path.exists(env_file):
    load_dotenv(dotenv_path=env_file)
else:
    raise FileNotFoundError(f'Environment file not found: {env_file}')

NAS_USERNAME = os.getenv('NAS_USERNAME')
NAS_PASSWORD = os.getenv('NAS_PASSWORD')
NAS_PORT = os.getenv('NAS_PORT')
NAS_HOST = os.getenv('NAS_HOST')
NAS_PATH = os.getenv('NAS_PATH')
NAS_OUTPUT = os.getenv('NAS_OUTPUT')
