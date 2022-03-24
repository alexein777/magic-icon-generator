from datetime import datetime
import re


def get_timestamp() -> str:
    now = str(datetime.now())
    return re.sub(r'[ .]', '_', now.replace(':', ''))
