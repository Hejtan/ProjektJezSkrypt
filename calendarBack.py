import calendar as cal
import datetime as dt
import pytz
from itertools import chain

class calendarRoom:

    def __init__(self, name: str, password: str ) -> None:
        self.cald = cal.Calendar()
        self.name = name
        self.password = password
        self.hourInd = []       
        # unavailable hours individually: 
        #    (dt.datetime: starth, dt.datetime: endh)
        self.hourDay = []       
        # unavailable hours every day: 
        #    (0<=int<=23: starth, 0<=int<=47: endh), endh>23 means next day
        self.hourWee = []       
        # unavailable hours every week on particular day: 
        #    (1<=int<=7: dayofweek, 0<=int<=23: starth, 0<=int<=47: endh),
        #    endh>23 means next day
        self.hourBiW = []       
        # unavailable hours every other week on 
        #    particular day: (1<=int<=7: dayofweek, 0/1: TP/TN,
        #    0<=int<=23: starth, 0<=int<=47: endh)
        self.hourMon = []       
        # unavailable hours every month of particular day: 
        #    (1<=int<=31: dayofmonth, 0<=int<=23: starth, 0<=int<=47: endh)
        self.reqLenH = 0        # required available time each day: int>=0
        self.reqWeDS = []       
        # available starting days in a week, empty means all: 1<=int<=7
        self.reqWeDE = []       
        # available ending days in a week, empty means all: 1<=int<=7
    # unavailable days are just implemented as unavailable 24h


    def findFreeTime(self, dates: int):
        date = dt.datetime.now().date()
        mon = range(1, 13)
        result = []
        while len(result) < dates and date.year < dt.datetime.now().year + 5:
            calendar = list(chain.from_iterable(self.cald.yeardatescalendar(date.year)))
            for i in range(0, 2):
                calendar = list(chain.from_iterable(calendar))
            calendar = {day: set(range(0, 24)) for day in calendar}
            for hour in self.hourMon:
                if hour[2] > 24:
                    rem = range(hour[1], 24)
                    for r in rem:
                        for m in mon:
                            calendar[dt.date(date.year, m, hour[0])].discard(r)
                    rem = range(0, hour[2]-24)
                    for r in rem:
                        for m in mon:
                            calendar[dt.date(date.year, m, hour[0]) / 
                            +dt.timedelta(days=1)].discard(r)
                else:
                    rem = range(hour[1], hour[2])
                    for r in rem:
                        for m in mon:
                            calendar[dt.date(date.year, m, hour[0])].discard(r)

            for hour in self.hourBiW:
                d = dt.date(date.year, 1, 1)
                while (d.isocalendar().weekday != hour[0]
                       and d.isocalendar().week % 2 == hour[1]):
                    d += dt.timedelta(days=1)
                if hour[3] > 24:
                    while d.year == date.year:
                        rem = range(hour[2], 24)
                        for r in rem:
                            calendar[d].discard(r)
                        rem = range(0, hour[3]-24)
                        for r in rem:
                            calendar[d+dt.timedelta(days=1)].discard(r)
                        d += dt.timedelta(days=14)
                else:
                    while d.year == date.year:
                        rem = range(hour[2], hour[3])
                        for r in rem:
                            calendar[d].discard(r)
                        d += dt.timedelta(days=14)

            for hour in self.hourWee:
                d = dt.date(date.year, 1, 1)
                while d.isocalendar().weekday != hour[0]:
                    d += dt.timedelta(days=1)
                if hour[2] > 24:
                    while d.year == date.year:
                        rem = range(hour[1], 24)
                        for r in rem:
                            calendar[d].discard(r)
                        rem = range(0, hour[2]-24)
                        for r in rem:
                            calendar[d+dt.timedelta(days=1)].discard(r)
                        d += dt.timedelta(days=7)
                else:
                    while d.year == date.year:
                        rem = range(hour[1], hour[2])
                        for r in rem:
                            calendar[d].discard(r)
                        d += dt.timedelta(days=7)

            for hour in self.hourInd:
                d = hour[0].date()
                h = hour[0].hour
                while not (d == hour[1].date() and h == hour[1].hour):
                    calendar[d].discard(h)
                    h += 1
                    if h == 24:
                        h = 0
                        d += dt.timedelta(days=1)

            dhelper = date
            hhelper = 30
            period = []
            while dhelper.year == date.year:
                hours = list(calendar[dhelper])
                hours.sort()
                for h in hours:
                    if h == (hhelper+1)%24:
                        x = dt.datetime.combine(dhelper, dt.time(hour=h))
                        period.append(x)
                    else:
                        if len(period) >= dates:
                            result.append(period)
                        period = []
                        x = dt.datetime.combine(dhelper, dt.time(hour=h))
                        period.append(x)
                    hhelper = h
                dhelper += dt.timedelta(days=1)

            date = dt.date(date.year+1, 1, 1)
        return result[0:dates]


example = calendarRoom("name", "pass")
example.hourInd.append((dt.datetime(2022, 6, 11, 13),
                        dt.datetime(2022, 6, 11, 17)))
example.hourDay.append((22, 7+24)) #from 10pm to 7am next day
example.hourWee.append((7, 1, 18)) #from 4pm to 6pm on sundays
example.hourWee.append((3, 5, 23)) #from 5am to 11pm on wednesdays
example.hourBiW.append((6, 1, 13, 17)) #from 1pm to 5pm on saturdays TN
example.hourMon.append((1, 4, 9)) #first day each month from 4am to 9am
example.reqLenH = 15    # 15 hours in a row each day

x=example.findFreeTime(3)
print(x[0], "\n")
print(x[1], "\n")
print(x[2], "\n")