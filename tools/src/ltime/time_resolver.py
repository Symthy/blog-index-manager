from datetime import datetime

ENTRY_DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
LOCAL_DATE_TIME_FORMAT = "%Y%m%d%H%M%S"


def resolve_entry_current_time() -> str:
    current_time = datetime.now()
    return current_time.strftime(ENTRY_DATE_TIME_FORMAT)


def convert_entry_datetime_to_str(dtime: datetime) -> str:
    return dtime.strftime(ENTRY_DATE_TIME_FORMAT)


def resolve_current_time_sequence() -> str:
    current_time = datetime.now()
    return current_time.strftime(LOCAL_DATE_TIME_FORMAT)
