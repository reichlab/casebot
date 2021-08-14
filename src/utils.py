import datetime

def get_last_monday():
  return datetime.date.today() -\
    datetime.timedelta(days=datetime.date.today().weekday())