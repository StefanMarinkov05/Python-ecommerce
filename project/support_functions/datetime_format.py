from datetime import datetime


def get_current_time():
    return datetime.now().replace(microsecond=0)

def parse_datetime(datetime_str):
    return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
