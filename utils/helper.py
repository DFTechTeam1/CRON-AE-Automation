from pytz import timezone
from datetime import datetime
from typing import Union, Literal


def local_time(type: Literal["string", "date"] = "date") -> Union[datetime, str]:
    current_time = datetime.now(timezone('Asia/Jakarta')).replace(tzinfo=None)
    if type is "string":
        return current_time.strftime("%Y%m%d%H%M")
    return current_time