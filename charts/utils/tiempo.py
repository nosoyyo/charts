import datetime


def eightDigits():
    now = datetime.datetime.now()
    return f'{now.year}{now.month:0>2}{now.day:0>2}'


def ft(timestamp):
    '''
    Here is especially for the timestamp contains in NetEase Json
    which looks like `1543766400000`
    '''

    timestamp = int(str(timestamp)[:-3])
    t = datetime.datetime.fromtimestamp(timestamp)
    return f'{t.year}{t.month:0>2}{t.day:0>2}'
