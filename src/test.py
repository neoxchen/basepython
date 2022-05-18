import datetime


def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    # Target day is today
    if days_ahead == 7:
        days_ahead = 0
    return d + datetime.timedelta(days_ahead)


now = datetime.datetime.utcnow()
next_monday = next_weekday(now, 2)
next_monday = datetime.datetime.combine(next_monday, datetime.time(7, 0, 0))

seconds = (next_monday - now).total_seconds()

print(seconds)
print(now)
print(now > datetime.time())
