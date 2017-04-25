import datetime


def get_datetime_prefix():
    now = datetime.datetime.now()
    prefix = '{:04d}-{:02d}-{:02d}-{:02d}-{:02d}-{:02d}'.\
             format(now.year,
                    now.month,
                    now.day,
                    now.hour,
                    now.minute,
                    now.second)
    return prefix
