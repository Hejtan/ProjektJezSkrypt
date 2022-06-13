from calendarBack import calendarRoom
from fastapi import FastAPI, HTTPException
from collections import defaultdict
import datetime as dt


app = FastAPI()
hotel = defaultdict(calendarRoom)


@app.post("/add/")
def addRoom(name: str, passw: str):
    """take name and password, make new room"""
    if name is "" or passw is "":
        raise HTTPException(status_code=400, detail="Need name and password")
    if name in hotel:
        raise HTTPException(status_code=400, detail="Room already exists")
    hotel[name] = calendarRoom(name, passw)
    return hotel[name]


@app.delete("/delete/{name}")
def removeRoom(name: str, passw: str):
    """take name and password, remove room"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    del hotel[name]


@app.get("/room/{name}/freetime/{n}")
def findFreeTime(name: str, passw: str, n: int):
    """take name, password, n, run findFreeTime(n) for room"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    return hotel[name].findFreeTime(n)


@app.post("/room/{name}/add/limithour")
def limitHour(name: str, passw: str, fr: dt.datetime, to: dt.datetime):
    """in name room with passw password run limitHour(fr, to)"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    if fr > to:
        raise HTTPException(status_code=400, detail="fr has to be before to")
    hotel[name].limitHour(fr, to)


@app.post("/room/{name}/add/limithourdaily")
def limitHourDaily(name: str, passw: str, fr: int, to: int):
    """in name room with passw password run limitHourDaily(fr, to)"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    if not (0 <= fr <= 24 and 0 <= to <= 24):
        raise HTTPException(status_code=400, detail="day has 24 hours")
    if to < fr:
        to += 24
    hotel[name].limitHourDaily(fr, to)


@app.post("/room/{name}/add/limithourweekly")
def limitHourWeekly(name: str, passw: str, day: int, fr: int, to: int):
    """in name room with passw password run limitHourWeekly(day, fr, to)"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    if not (0 <= fr <= 24 and 0 <= to <= 24):
        raise HTTPException(status_code=400, detail="day has 24 hours")
    if not 1 <= day <= 7:
        raise HTTPException(status_code=400, detail="Week has 7 days")
    if to < fr:
        to += 24
    hotel[name].limitHourWeekly(day, fr, to)


@app.post("/room/{name}/add/limithourbiweekly")
def limitHourBiweekly(name: str, passw: str, day: int,
                      week: int, fr: int, to: int):
    """in name room with passw password 
    run limitHourBiweekly(day, week, fr, to)"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    if not (0 <= fr <= 24 and 0 <= to <= 24):
        raise HTTPException(status_code=400, detail="day has 24 hours")
    if not 1 <= day <= 7:
        raise HTTPException(status_code=400, detail="Week has 7 days")
    if to < fr:
        to += 24
    hotel[name].limitHourBiweekly(day, week, fr, to)


@app.post("/room/{name}/add/limithourmonthly")
def limitHourMonthly(name: str, passw: str, day: int, fr: int, to: int):
    """in name room with passw password run limitHourMonthly(day, fr, to)"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    if not (0 <= fr <= 24 and 0 <= to <= 24):
        raise HTTPException(status_code=400, detail="day has 24 hours")
    if not 1 <= day <= 31:
        raise HTTPException(status_code=400, 
                            detail="Months have from 28 to 31 days")
    if to < fr:
        to += 24
    hotel[name].limitHourBiweekly(day, fr, to)


@app.post("/room/{name}/add/limitday")
def limitDay(name: str, passw: str, fr: dt.date, to: dt.date):
    """in name room with passw password run limitDay(fr, to)"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    if fr > to:
        raise HTTPException(status_code=400, detail="fr has to be before to")
    hotel[name].limitDay(fr, to)


@app.post("/room/{name}/add/limitdayweekly")
def limitDayWeekly(name: str, passw: str, fr: int, to: int):
    """in name room with passw password run limitDayWeekly(fr, to)"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    if not (1 <= fr <= 7 and 1 <= to <= 7):
        raise HTTPException(status_code=400, detail="week has 7 days")
    hotel[name].limitDayWeekly(fr, to)


@app.post("/room/{name}/add/limitdaybiweekly")
def limitDayBiweekly(name: str, passw: str, week: int, fr: int, to: int):
    """in name room with passw password run limitDayBiweekly(week, fr, to)"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    if not (1 <= fr <= 7 and 1 <= to <= 7):
        raise HTTPException(status_code=400, detail="week has 7 days")
    hotel[name].limitDayBiweekly(week, fr, to)


@app.post("/room/{name}/add/limitdaymonthly")
def limitDayMonthly(name: str, passw: str, fr: int, to: int):
    """in name room with passw password run limitDayMonthly(fr, to)"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    if not (1 <= fr <= 31 and 1 <= to <= 31):
        raise HTTPException(status_code=400, detail="Month has 28-31 days")
    if fr > to:
        raise HTTPException(status_code=400, detail="fr has to be before to")
    hotel[name].limitDayMonthly(fr, to)


@app.delete("/room/{name}/remove/limithour")
def removeLimitHour(name: str, passw: str, nr: int):
    """in name room with passw password remove hourInd[nr]"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    if len(hotel[name].hourInd) >= nr:
        raise HTTPException(status_code=400, detail="nr is out of bounds")
    hotel[name].removeLimitHour(nr)


@app.delete("/room/{name}/remove/limithourdaily")
def removeLimitHourDaily(name: str, passw: str, nr: int):
    """in name room with passw password remove hourDay[nr]"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    if len(hotel[name].hourDay) >= nr:
        raise HTTPException(status_code=400, detail="nr is out of bounds")
    hotel[name].removeLimitHourDaily(nr)


@app.delete("/room/{name}/remove/limithourweekly")
def removeLimitHourWeekly(name: str, passw: str, nr: int):
    """in name room with passw password remove hourWee[nr]"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    if len(hotel[name].hourWee) >= nr:
        raise HTTPException(status_code=400, detail="nr is out of bounds")
    hotel[name].removeLimitHourWeekly(nr)


@app.delete("/room/{name}/remove/limithourbiweekly")
def removeLimitHourBiweekly(name: str, passw: str, nr: int):
    """in name room with passw password remove hourBiW[nr]"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    if len(hotel[name].hourBiW) >= nr:
        raise HTTPException(status_code=400, detail="nr is out of bounds")
    hotel[name].removeLimitHourBiweekly(nr)


@app.delete("/room/{name}/remove/limithourmonthly")
def removeLimitHourMonthly(name: str, passw: str, nr: int):
    """in name room with passw password remove hourMon[nr]"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    if len(hotel[name].hourMon) >= nr:
        raise HTTPException(status_code=400, detail="nr is out of bounds")
    hotel[name].removeLimitHourMonthly(nr)


@app.get("/room/{name}/check/limithour")
def getLimitHour(name: str, passw: str):
    """return hourInd of room with name and passw"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    return hotel[name].hourInd


@app.get("/room/{name}/check/limithourdaily")
def getLimitHourDaily(name: str, passw: str):
    """return hourDay of room with name and passw"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    return hotel[name].hourDay


@app.get("/room/{name}/check/limithourweekly")
def getLimitHourWeekly(name: str, passw: str):
    """return hourWee of room with name and passw"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    return hotel[name].hourWee


@app.get("/room/{name}/check/limithourbiweekly")
def getLimitHourBiweekly(name: str, passw: str):
    """return hourWee of room with name and passw"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    return hotel[name].hourBiW


@app.get("/room/{name}/check/limithourmonthly")
def getLimitHourMonthly(name: str, passw: str):
    """return hourMon of room with name and passw"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    return hotel[name].hourMon