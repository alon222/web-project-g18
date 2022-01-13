import datetime


def from_datetime_str_to_datetime(datetime_str: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(datetime_str)


def convert_datetime_to_timestamp(ts: datetime.datetime) -> str:
    return ts.strftime('%Y-%m-%d %H:%M:%S')