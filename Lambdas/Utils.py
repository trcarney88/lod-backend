import arrow

def getWaitTime(interval):
    now = arrow.utcnow()
    time = now.shift(hours=interval)
    ret = time.for_json()
    return ret
