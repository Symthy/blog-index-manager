from datetime import datetime
from typing import Optional

ENTRY_DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
LOCAL_DATE_TIME_FORMAT = "%Y%m%d%H%M%S"


def get_current_datetime() -> datetime:
    return datetime.now()


def resolve_entry_current_time() -> str:
    current_time = get_current_datetime()
    return current_time.strftime(ENTRY_DATE_TIME_FORMAT)


def convert_datetime_to_entry_time_str(date_time: Optional[datetime]) -> str:
    if date_time is None:
        return ''
    return date_time.strftime(ENTRY_DATE_TIME_FORMAT)


def convert_entry_time_str_to_datetime(entry_time: str) -> Optional[datetime]:
    if entry_time is None or len(entry_time) == 0:
        return None
    return datetime.strptime(entry_time, ENTRY_DATE_TIME_FORMAT)


def convert_datetime_to_month_day_str(date_time: Optional[datetime]) -> str:
    if date_time is None:
        return ''
    return date_time.strftime('%Y/%m')


def resolve_current_time_sequence() -> str:
    current_time = get_current_datetime()
    return current_time.strftime(LOCAL_DATE_TIME_FORMAT)


def convert_datetime_to_time_sequence(date_time: Optional[datetime]) -> str:
    if date_time is None:
        return ''
    return date_time.strftime(LOCAL_DATE_TIME_FORMAT)


def resolve_current_time_date_time() -> str:
    current_time = datetime.now()
    return current_time.strftime("%Y%m%d_%H%M%S")
