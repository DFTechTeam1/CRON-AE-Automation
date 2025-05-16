import json
from utils.logger import logging
from pytz import timezone
from datetime import datetime
from typing import Union, Literal


def local_time(type: Literal['string', 'date'] = 'date') -> Union[datetime, str]:
    current_time = datetime.now(timezone('Asia/Jakarta')).replace(tzinfo=None)
    if type == 'string':
        return current_time.strftime('%Y%m%d%H%M')
    return current_time


def save_json(destination: str, data: dict) -> None:
    logging.info(f'Data saved to {destination}.')
    file = open(destination, 'w')
    try:
        json.dump(data, file, indent=4)
    finally:
        file.close()
    return
