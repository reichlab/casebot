import datetime

def get_last_monday() -> datetime.date:
    return (
        datetime.date.today() -
            datetime.timedelta(days=datetime.date.today().weekday())
    )