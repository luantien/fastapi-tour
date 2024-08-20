from datetime import datetime, timezone

def get_current_utc_time():
    return datetime.now(timezone.utc)
