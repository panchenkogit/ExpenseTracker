from datetime import datetime, date
from dateutil.relativedelta import relativedelta


TIMESPANS = {1: {"days": 1}, 2: {"weeks": 1}, 3: {"months": 1}, 4: {"years": 1}}


def date_to_timestamp(d: date) -> int:
    """Преобразовать date в timestamp"""
    return int(datetime(d.year, d.month, d.day, 0, 0, 0).timestamp())


def сounting_payment_day(frequency_id: int, start_date: datetime.date) -> datetime.date:
    if frequency_id not in TIMESPANS:
        raise ValueError("Некорректный frequency_id")
    return start_date + relativedelta(**TIMESPANS[frequency_id])
