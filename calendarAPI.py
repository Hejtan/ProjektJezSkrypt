from calendarBack import calendarRoom
from fastapi import FastAPI, HTTPException
from collections import defaultdict
from datetime import datetime as dt

app = FastAPI()
hotel = defaultdict(calendarRoom)


@app.post("/add/")
def addRoom(name: str, passw: str):
    """take name and password, make new room"""
    if name == "" or passw == "":
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
    return hotel[name].findFreeTime(int(n))


@app.post("/room/{name}/add/limithour")
def limitHour(name: str, passw: str, fr: str, to: str):
    """in name room with passw password run limitHour(fr, to)
    required format for fr and to is: YYYY/MM/DD-HH"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    if fr > to:
        raise HTTPException(status_code=400, detail="fr has to be before to")
    frdt = dt.strptime(fr, "%Y/%m/%d-%H")
    todt = dt.strptime(to, "%Y/%m/%d-%H")
    hotel[name].limitHour(frdt, todt)


@app.post("/room/{name}/add/limithourdaily")
def limitHourDaily(name: str, passw: str, fr: int, to: int):
    """in name room with passw password run limitHourDaily(fr, to)"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    if not (0 <= fr < 24 and 0 <= to < 24):
        raise HTTPException(status_code=400, detail="day has 24 hours")
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
    hotel[name].limitHourMonthly(day, fr, to)


@app.post("/room/{name}/add/limitday")
def limitDay(name: str, passw: str, fr: str, to: str):
    """in name room with passw password run limitDay(fr, to)
    fr and to MUST be in format: YYYY/MM/DD"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    if fr > to:
        raise HTTPException(status_code=400, detail="fr has to be before to")
    frdt = dt.strptime(fr, "%Y/%m/%d")
    todt = dt.strptime(to, "%Y/%m/%d")
    hotel[name].limitDay(frdt, todt)


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


@app.post("/room/{name}/set/reqlenh")
def setReqLenH(name: str, passw: str, req: int):
    """int the room with name and passw set required hour length to be found"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    if req <= 0:
        raise HTTPException(status_code=400, detail="Hour length below 1")
    hotel[name].reqLenH = req


@app.delete("/room/{name}/remove/limithour")
def removeLimitHour(name: str, passw: str, nr: int):
    """in name room with passw password remove hourInd[nr]"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    if len(hotel[name].hourInd) <= nr:
        raise HTTPException(status_code=400, detail="nr is out of bounds")
    hotel[name].removeLimitHour(nr)


@app.delete("/room/{name}/remove/limithourdaily")
def removeLimitHourDaily(name: str, passw: str, nr: int):
    """in name room with passw password remove hourDay[nr]"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    if len(hotel[name].hourDay) <= nr:
        raise HTTPException(status_code=400, detail="nr is out of bounds")
    hotel[name].removeLimitHourDaily(nr)


@app.delete("/room/{name}/remove/limithourweekly")
def removeLimitHourWeekly(name: str, passw: str, nr: int):
    """in name room with passw password remove hourWee[nr]"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    if len(hotel[name].hourWee) <= nr:
        raise HTTPException(status_code=400, detail="nr is out of bounds")
    hotel[name].removeLimitHourWeekly(nr)


@app.delete("/room/{name}/remove/limithourbiweekly")
def removeLimitHourBiweekly(name: str, passw: str, nr: int):
    """in name room with passw password remove hourBiW[nr]"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    if len(hotel[name].hourBiW) <= nr:
        raise HTTPException(status_code=400, detail="nr is out of bounds")
    hotel[name].removeLimitHourBiweekly(nr)


@app.delete("/room/{name}/remove/limithourmonthly")
def removeLimitHourMonthly(name: str, passw: str, nr: int):
    """in name room with passw password remove hourMon[nr]"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    if len(hotel[name].hourMon) <= nr:
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


@app.get("/room/{name}/check/reqlenh")
def getReqLenH(name: str, passw: str):
    """return reqlenh of room with name and passw"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    if hotel[name].password != passw:
        raise HTTPException(status_code=400, detail="Wrong password")
    return hotel[name].reqLenH


@app.get("/room/{name}/check/exist")
def checkIfExists(name: str):
    """checks if room with name exists"""
    return name in hotel


@app.get("/room/{name}/check/rightpass")
def checkRightPass(name: str, passw: str):
    """checks if name room has passw password"""
    if name not in hotel:
        raise HTTPException(status_code=404, detail="Such room can't be found")
    return hotel[name].password == passw
