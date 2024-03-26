from datetime import datetime, timedelta


def get_today() -> datetime:
    return datetime.now()


def get_today_human() -> str:
    return datetime.now().strftime("%A, %B %d")


def get_yesterday() -> datetime:
    yesterday = get_today() - timedelta(days=1)
    return yesterday.replace(hour=0, minute=0, second=0, microsecond=0)


def get_yesterday_human() -> str:
    return get_yesterday().strftime("%A, %B %d")


def get_yesterday_unix() -> int:
    return int(get_yesterday().timestamp()) * 1000
