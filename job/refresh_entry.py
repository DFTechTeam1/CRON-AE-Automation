import subprocess
import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.logger import logging

commands = [
    [
        'sh',
        '/home/ai/Project/CRON-AE-Automation/scripts/run_mounter.sh',
        '--env',
        'production'
    ],
    [
        'sh',
        '/home/ai/Project/CRON-AE-Automation/scripts/run_executor.sh',
        '--path',
        '/home/ai/Project/CRON-AE-Automation/job/update.py',
        '--env',
        'production'
    ],
]


def run_command(cmd: list, retries: int = 3, delay: int = 5, background: bool = False) -> None:
    attempt = 0
    while attempt < retries:
        logging.info(
            f'Running: {" ".join(cmd)} {"in background" if background else ""} (Attempt {attempt + 1}/{retries})'
        )
        try:
            if background:
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                logging.info('Started in background.')
                return
            else:
                result = subprocess.run(cmd, check=True, text=True, capture_output=True)
                logging.info(result.stdout)
                return
        except subprocess.CalledProcessError as e:
            logging.error(f'Command failed: {" ".join(cmd)}')
            logging.error('STDERR:', e.stderr)
            attempt += 1
            if attempt < retries:
                logging.warning(f'Retrying in {delay} seconds...')
                time.sleep(delay)
            else:
                logging.error('All retries failed.')
                sys.exit(e.returncode)


for command in commands:
    run_command(command)