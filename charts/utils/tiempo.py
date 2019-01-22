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


def delta(timestamp):
    '''
    Calculate how many days past from a given timestamp till now.
    '''
    timestamp = int(str(timestamp)[:10])
    return datetime.datetime.now() - datetime.datetime.fromtimestamp(timestamp)


def buildClass(d):
    '''
    Build css class by a given timedelta

    :param d: timedelta
    '''

    if d.days < 7:
        _class = 'one_week'
    elif 7 <= d.days < 14:
        _class = 'two_weeks'
    elif 14 <= d.days < 28:
        _class = 'two_weeks'
    elif 28 <= d.days < 90:
        _class = 'three_months'
    elif 90 <= d.days < 365:
        _class = 'one_year'
    elif 365 <= d.days < 730:
        _class = 'two_years'
    else:
        _class = 'back_catalogue'

    return _class
