import datetime


def eightDigits():
    now = datetime.datetime.now()
    return f'{now.year}{now.month:0>2}{now.day:0>2}'
