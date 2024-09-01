from datetime import datetime, timezone
import time

def get_current_utc_time() -> datetime:
    return datetime.now(timezone.utc)

def get_current_timestamp() -> int:
    return int(time.time())
