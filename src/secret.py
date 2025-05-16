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
ROOT_PATH = os.getenv('ROOT_PATH')
DIVA_PG_SQL_PORT = os.getenv('DIVA_PG_SQL_PORT')
DIVA_PG_SQL_USER = os.getenv('DIVA_PG_SQL_USER')
DIVA_PG_SQL_PASSWORD = os.getenv('DIVA_PG_SQL_PASSWORD')
DIVA_PG_SQL_DATABASE = os.getenv('DIVA_PG_SQL_DATABASE')
DIVA_PG_SQL_HOST = os.getenv('DIVA_PG_SQL_HOST')
POSTGRES_URL = f'postgresql+asyncpg://{DIVA_PG_SQL_USER}:{DIVA_PG_SQL_PASSWORD}@{DIVA_PG_SQL_HOST}:{DIVA_PG_SQL_PORT}/{DIVA_PG_SQL_DATABASE}'
