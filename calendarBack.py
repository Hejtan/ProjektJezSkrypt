import calendar as cal
import datetime as dt
from itertools import chain


class calendarRoom:

    cald = cal.Calendar()

    def __init__(self, name: str, password: str) -> None:
        self.cald = cal.Calendar()
        self.name = name
        self.password = password
        self.lastMod = dt.datetime.now()
        # unavailable hours individually:
        #    (dt.datetime: starth, dt.datetime: endh)
        self.hourInd = []
        # unavailable hours every day:
        #    (0<=int<=23: starth, 0<=int<=47: endh), endh>23 means next day
        self.hourDay = []
        # unavailable hours every week on particular day:
        #    (1<=int<=7: dayofweek, 0<=int<=23: starth, 0<=int<=47: endh),
        #    endh>23 means next day
        self.hourWee = []
        # unavailable hours every other week on
        #    particular day: (1<=int<=7: dayofweek, 0/1: TP/TN,
        #    0<=int<=23: starth, 0<=int<=47: endh)
        self.hourBiW = []
        # unavailable hours every month of particular day:
        #    (1<=int<=31: dayofmonth, 0<=int<=23: starth, 0<=int<=47: endh)
        self.hourMon = []
        self.reqLenH = 1        # required available time each day: int>0
    # unavailable days are just implemented as unavailable 24h

    def findFreeTime(self, dates: int):
        """take int, return first int available free date ranges in list"""
        self.lastMod = dt.datetime.now()
        date = dt.datetime.now().date()
        mon = range(1, 13)
        result = []
        while len(result) < dates and date.year < dt.datetime.now().year + 5:
            calendar = self.cald.yeardatescalendar(date.year)
            calendar = list(chain.from_iterable(calendar))
            for i in range(0, 2):
                calendar = list(chain.from_iterable(calendar))
            calendar = {day: set(range(0, 24)) for day in calendar}
            for hour in self.hourMon:
                if hour[2] > 23:
                    rem = range(hour[1], 24)
                    for r in rem:
                        for m in mon:
                            if cal.monthrange(date.year, m)[1] >= hour[0]:
                                day = dt.date(date.year, m, hour[0])
                                calendar[day].discard(r)
                    rem = range(0, hour[2]-24)
                    for r in rem:
                        for m in mon:
                            if cal.monthrange(date.year, m)[1] >= hour[0]:
                                day = dt.date(date.year, m, hour[0])
                                day += dt.timedelta(days=1)
                                calendar[day].discard(r)
                else:
                    rem = range(hour[1], hour[2])
                    for r in rem:
                        for m in mon:
                            calendar[dt.date(date.year, m, hour[0])].discard(r)

            for hour in self.hourBiW:
                d = dt.datetime(date.year, 1, 1)
                weekday = int(dt.datetime.strftime(d, "%u"))
                while weekday != hour[0]:
                    d += dt.timedelta(days=1)
                    weekday = int(dt.datetime.strftime(d, "%u"))
                week = int(dt.datetime.strftime(d, "%V"))
                if week % 2 != hour[1]:
                    d += dt.timedelta(days=7)
                d = d.date()
                if hour[3] > 23:
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
                if hour[2] > 23:
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

            for hour in self.hourDay:
                if hour[1] > 23:
                    rem = range(hour[0], 24)
                    for r in rem:
                        for key in calendar:
                            calendar[key].discard(r)
                    rem = range(0, hour[1]-24)
                    for r in rem:
                        for key in calendar:
                            calendar[key].discard(r)
                else:
                    rem = range(hour[0], hour[1])
                    for r in rem:
                        for key in calendar:
                            calendar[key].discard(r)

            for hour in self.hourInd:
                d = hour[0].date()
                h = hour[0].hour
                while not (d == hour[1].date() and h == hour[1].hour):
                    if d in calendar:
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
                if len(hours) == 0:
                    if len(period) >= self.reqLenH:
                        result.append(period)
                    period = []
                hours.sort()
                for h in hours:
                    if h == (hhelper+1) % 24:
                        x = dt.datetime.combine(dhelper, dt.time(hour=h))
                        period.append(x)
                    else:
                        if len(period) >= self.reqLenH:
                            result.append(period)
                        period = []
                        x = dt.datetime.combine(dhelper, dt.time(hour=h))
                        period.append(x)
                    hhelper = h
                dhelper += dt.timedelta(days=1)

            date = dt.date(date.year+1, 1, 1)
        return result[0:dates]

    def limitHour(self, fr: dt.datetime, to: dt.datetime):
        """take two datetime, add their range to unavailable times"""
        self.lastMod = dt.datetime.now()
        self.hourInd.append((fr, to))

    def limitHourDaily(self, fr: int, to: int):
        """take two int representing hours, add them to daily taken times"""
        self.lastMod = dt.datetime.now()
        if fr < to:
            self.hourDay.append((fr, to))
        else:
            self.hourDay.append((fr, to+24))

    def limitHourWeekly(self, day: int, fr: int, to: int):
        """take day of the week and two hours as int, add them to limits"""
        self.lastMod = dt.datetime.now()
        if fr < to:
            self.hourWee.append((day, fr, to))
        else:
            self.hourWee.append((day, fr, to+24))

    def limitHourBiweekly(self, day: int, week: int, fr: int, to: int):
        """take 4 int as day of week, parity of week and hour range,
        add them to limits"""
        self.lastMod = dt.datetime.now()
        if fr < to:
            self.hourBiW.append((day, week, fr, to))
        else:
            self.hourBiW.append((day, week, fr, to+24))

    def limitHourMonthly(self, day: int, fr: int, to: int):
        """take 3 int as day of month and hour range, add them to limits"""
        self.lastMod = dt.datetime.now()
        if fr < to:
            self.hourMon.append((day, fr, to))
        else:
            self.hourMon.append((day, fr, to+24))

    def limitDay(self, fr: dt.date, to: dt.date):
        """take 2 date, add the range as unavailable"""
        self.lastMod = dt.datetime.now()
        date = dt.datetime(fr.year, fr.month, fr.day)
        to = dt.datetime(to.year, to.month, to.day)
        while date < to:
            d2 = dt.timedelta(days=1)+date
            self.hourInd.append((date, d2))
            date = d2

    def limitDayWeekly(self, fr: int, to: int):
        """take 2 int as day of week range, add range to weekly limit"""
        self.lastMod = dt.datetime.now()
        if fr <= to:
            for i in range(fr, to+1):
                self.hourWee.append((i, 0, 24))
        else:
            for i in range(fr, 8):
                self.hourWee.append((i, 0, 24))
            for i in range(1, to):
                self.hourWee.append((i, 0, 24))

    def limitDayBiweekly(self, week: int, fr: int, to: int):
        """take 3 int as week nr and day of week range, add range to biweek"""
        self.lastMod = dt.datetime.now()
        if fr <= to:
            for i in range(fr, to+1):
                self.hourBiW.append((i, week, 0, 24))
        else:
            for i in range(fr, 8):
                self.hourBiW.append((i, week, 0, 24))
            for i in range(1, to):
                self.hourBiW.append((i, week, 0, 24))

    def limitDayMonthly(self, fr: int, to: int):
        """take 2 int as day of month range, add range to month limit"""
        self.lastMod = dt.datetime.now()
        for i in range(fr, to+1):
            self.hourMon.append((i, 0, 24))

    def removeLimitHour(self, nr: int):
        """take list position, remove hour limit of this position"""
        self.lastMod = dt.datetime.now()
        if len(self.hourInd) > nr:
            del self.hourInd[nr]

    def removeLimitHourDaily(self, nr: int):
        """take list position, remove daily hour limit of this position"""
        self.lastMod = dt.datetime.now()
        if len(self.hourDay) > nr:
            del self.hourDay[nr]

    def removeLimitHourWeekly(self, nr: int):
        """take list position, remove weekly hour limit of this position"""
        self.lastMod = dt.datetime.now()
        if len(self.hourWee) > nr:
            del self.hourWee[nr]

    def removeLimitHourBiweekly(self, nr: int):
        """take list position, remove biweekly hour limit of this position"""
        self.lastMod = dt.datetime.now()
        if len(self.hourBiW) > nr:
            del self.hourBiW[nr]

    def removeLimitHourMonthly(self, nr: int):
        """take list position, remove monthly hour limit of this position"""
        self.lastMod = dt.datetime.now()
        if len(self.hourMon) > nr:
            del self.hourMon[nr]

    def setRequiredHour(self, n: int):
        """set reqLenH to n"""
        self.reqLenH = n

    def getRequiredHour(self):
        """return reqLenH"""
        return self.reqLenH
