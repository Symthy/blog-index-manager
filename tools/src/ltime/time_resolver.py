from datetime import datetime

DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"


def resolve_current_time() -> str:
    current_time = datetime.now()
    return current_time.strftime(DATE_TIME_FORMAT)


def convert_datetime_to_str(dtime: datetime) -> str:
    return dtime.strftime(DATE_TIME_FORMAT)
