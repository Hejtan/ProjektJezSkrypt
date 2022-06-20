import tkinter as tk
import requests as rqs
from datetime import datetime as dt, timedelta as tdl
import calendar as cal

url = "http://127.0.0.1:8000/"


class GUI:

    def __init__(self):
        self.window = tk.Tk()
        self.resultWindow = None
        self.greetFrame = None
        self.roomFrame = None
        self.greetingLabel = None
        self.nameLabel = None
        self.nameInput = None
        self.passwInput = None
        self.passwLabel = None
        self.joinRoom = None
        self.createRoom = None
        self.limitFrame = None
        self.limitButtons = []
        self.removeFrame = None
        self.removeButtons = []
        self.otherFrame = None
        self.maxLabel = None
        self.maxInput = None
        self.freeButton = None
        self.leaveRoomButton = None
        self.openRoomName = ""
        self.openRoomPassw = ""
        self.resultList = []
        self.askWindow = None
        self.askLabel = None

    def run(self):
        """starts program"""
        self.openGreetingScreen()
        self.window.mainloop()

    def openGreetingScreen(self):
        """provides interface for creating/entering rooms"""
        self.greetFrame = tk.Frame(self.window)
        self.greetFrame.grid(row=0, column=0)
        self.roomFrame = tk.Frame(self.window)
        self.roomFrame.grid(row=1, column=0)
        self.window.rowconfigure(0, weight=1, minsize=30)
        self.window.rowconfigure(1, weight=1, minsize=100)
        self.window.columnconfigure(0, weight=1, minsize=400)
        for i in range(3):
            self.roomFrame.rowconfigure(i, weight=1, minsize=30)
        for i in range(4):
            self.roomFrame.columnconfigure(i, weight=1, minsize=100)

        self.greetingLabel = tk.Label(
            master=self.greetFrame,
            text="Welcome to the example GUI",
            height=1
        )
        self.greetingLabel.pack()

        self.nameLabel = tk.Label(
            master=self.roomFrame,
            text="Room name:",
            height=1
        )
        self.nameLabel.grid(row=0, column=1, sticky="e")
        self.nameInput = tk.Entry(
            master=self.roomFrame
        )
        self.nameInput.grid(row=0, column=2)
        self.passwLabel = tk.Label(
            master=self.roomFrame,
            text="Room password:",
            height=1
        )
        self.passwLabel.grid(row=1, column=1, sticky="e")
        self.passwInput = tk.Entry(
            master=self.roomFrame
        )
        self.passwInput.grid(row=1, column=2)

        self.createRoom = tk.Button(
            master=self.roomFrame,
            text="Create Room",
            command=self.makeNewRoom
        )
        self.createRoom.grid(row=2, column=0, padx=10, pady=10)
        self.joinRoom = tk.Button(
            master=self.roomFrame,
            text="Join room",
            command=self.enterRoom
        )
        self.joinRoom.grid(row=2, column=3, padx=10, pady=10)

    def runRoom(self):
        """creates interface for room"""
        self.roomFrame = tk.Frame(master=self.window)
        self.roomFrame.grid(row=1, column=0)
        self.greetingLabel.config(text="Room " + self.openRoomName)

        self.limitFrame = tk.Frame(master=self.roomFrame)
        self.limitFrame.grid(row=0, column=0)
        for i in range(9):
            self.limitFrame.rowconfigure(i, weight=1)
        for label, command in (
                ("Add Individual Hour Limit", self.hourLimitInd),
                ("Add Daily Hour Limit", self.hourLimitDay),
                ("Add Weekly Hour Limit", self.hourLimitWee),
                ("Add Biweekly Hour Limit", self.hourLimitBiw),
                ("Add Monthly Hour Limit", self.hourLimitMon),
                ("Add Individual Day Limit", self.dayLimitInd),
                ("Add Weekly Day Limit", self.dayLimitWee),
                ("Add Biweekly Day Limit", self.dayLimitBiw),
                ("Add Monthly Day Limit", self.dayLimitMon)):
            self.limitButtons.append(tk.Button(
                master=self.limitFrame,
                command=command,
                text=label,
                width=25,
                bg="lime"
            ))
        for button in self.limitButtons:
            button.pack()

        self.removeFrame = tk.Frame(master=self.roomFrame)
        self.removeFrame.grid(row=0, column=1)
        for i in range(5):
            self.removeFrame.rowconfigure(i, weight=1)
        for label, command in (
                ("Remove Individual Hour Limit", self.removeLimitInd),
                ("Remove Daily Hour Limit", self.removeLimitDay),
                ("Remove Weekly Hour Limit", self.removeLimitWee),
                ("Remove Biweekly Hour Limit", self.removeLimitBiw),
                ("Remove Monthly Hour Limit", self.removeLimitMon)):
            self.removeButtons.append(tk.Button(
                master=self.removeFrame,
                command=command,
                text=label,
                width=25,
                bg="red"
            ))
        for button in self.removeButtons:
            button.pack()

        self.otherFrame = tk.Frame(master=self.roomFrame)
        self.otherFrame.grid(row=0, column=2)
        for i in range(8):
            self.otherFrame.rowconfigure(i, weight=1, minsize=30)
        self.setReqButton = tk.Button(
            master=self.otherFrame,
            command=self.setRequirement,
            text="Set min period length",
            bg="yellow"
        )
        self.setReqButton.grid(row=0, column=0)
        self.maxLabel = tk.Label(master=self.otherFrame, text="Max shown:")
        self.maxLabel.grid(row=1, column=0)
        self.maxInput = tk.Entry(master=self.otherFrame)
        self.maxInput.grid(row=2, column=0)
        self.freeButton = tk.Button(
            master=self.otherFrame,
            command=self.seekFree,
            text="Find free time",
            bg="cyan"
        )
        self.freeButton.grid(row=4, column=0)
        self.leaveRoomButton = tk.Button(
            master=self.otherFrame,
            command=self.leaveRoom,
            text="Leave Room",
            bg="orange"
        )
        self.leaveRoomButton.grid(row=7, column=0)

    def makeNewRoom(self):
        """attempts to create new room using provided details"""
        if not self.nameInput.get():
            self.greetingLabel.config(text="Enter a name")
        elif not self.passwInput.get():
            self.greetingLabel.config(text="Enter a password")
        else:
            req = rqs.get(
                url+"room/"+self.nameInput.get()+"/check/exist"
            )
            if req.text == "true":
                self.greetingLabel.config(text="The name is already taken")
            else:
                req = rqs.post(
                    url+"add/",
                    params={
                        "name": self.nameInput.get(),
                        "passw": self.passwInput.get()
                    }
                )
                self.openRoomName = self.nameInput.get()
                self.openRoomPassw = self.passwInput.get()
                self.runRoom()

    def enterRoom(self):
        """attempts to enter the room with chosen name using provided passw"""
        if not self.nameInput.get():
            self.greetingLabel.config(text="Enter a name")
        elif not self.passwInput.get():
            self.greetingLabel.config(text="Enter a password")
        else:
            req = rqs.get(
                url+"room/"+self.nameInput.get()+"/check/rightpass",
                params={"passw": self.passwInput.get()}
            )
            if req.status_code == 404:
                self.greetingLabel.config(text="Room doesn't exist")
            elif req.text == "false":
                self.greetingLabel.config(text="Wrong password")
            else:
                self.openRoomName = self.nameInput.get()
                self.openRoomPassw = self.passwInput.get()
                self.runRoom()

    def leaveRoom(self):
        """leaves room, returns to greeting screen"""
        self.roomFrame.destroy()
        self.openRoomName = ""
        self.openRoomPassw = ""
        self.limitButtons = []
        self.removeButtons = []
        self.greetingLabel.destroy()
        self.openGreetingScreen()

    def hourLimitInd(self):
        """opens window to add individual hour limit"""
        self.askWindow = tk.Tk()
        self.askLabel = tk.Label(
            master=self.askWindow,
            text="Specify new individual hour limit (format: YYYY/MM/DD-HH):",
            bg="lime"
        )
        labelFr = tk.Label(
            master=self.askWindow,
            text="From:"
        )
        entryFr = tk.Entry(master=self.askWindow)
        labelTo = tk.Label(
            master=self.askWindow,
            text="To:"
        )
        entryTo = tk.Entry(master=self.askWindow)

        def end():
            req = rqs.post(
                url+"room/"+self.openRoomName+"/add/limithour",
                params={
                    "passw": self.openRoomPassw,
                    "fr": entryFr.get(),
                    "to": entryTo.get()
                }
            )
            if req:
                self.greetingLabel.config(text="Limit added successfully")
            else:
                self.greetingLabel.config(text="Error while adding limit")
            self.askWindow.destroy()

        okbutt = tk.Button(
            master=self.askWindow,
            text="Confirm",
            command=end
        )

        self.askLabel.pack()
        labelFr.pack()
        entryFr.pack()
        labelTo.pack()
        entryTo.pack()
        okbutt.pack()
        self.askWindow.focus_force()
        self.askWindow.mainloop()

    def hourLimitDay(self):
        """opens window to add daily hour limit"""
        self.askWindow = tk.Tk()
        self.askLabel = tk.Label(
            master=self.askWindow,
            text="Specify new daily hour limit:",
            bg="lime"
        )
        labelFr = tk.Label(
            master=self.askWindow,
            text="From:"
        )
        entryFr = tk.Entry(master=self.askWindow)
        labelTo = tk.Label(
            master=self.askWindow,
            text="To:"
        )
        entryTo = tk.Entry(master=self.askWindow)

        def end():
            req = rqs.post(
                url+"room/"+self.openRoomName+"/add/limithourdaily",
                params={
                    "passw": self.openRoomPassw,
                    "fr": entryFr.get(),
                    "to": entryTo.get()
                }
            )
            if req:
                self.greetingLabel.config(text="Limit added successfully")
            else:
                self.greetingLabel.config(text="Error while adding limit")
            self.askWindow.destroy()

        okbutt = tk.Button(
            master=self.askWindow,
            text="Confirm",
            command=end
        )

        self.askLabel.pack()
        labelFr.pack()
        entryFr.pack()
        labelTo.pack()
        entryTo.pack()
        okbutt.pack()
        self.askWindow.focus_force()
        self.askWindow.mainloop()

    def hourLimitWee(self):
        """opens window to add weekly hour limit"""
        self.askWindow = tk.Tk()
        self.askLabel = tk.Label(
            master=self.askWindow,
            text="Specify new weekly hour limit:",
            bg="lime"
        )
        labelDay = tk.Label(
            master=self.askWindow,
            text="Day of week"
        )
        entryDay = tk.Entry(self.askWindow)
        labelFr = tk.Label(
            master=self.askWindow,
            text="From:"
        )
        entryFr = tk.Entry(master=self.askWindow)
        labelTo = tk.Label(
            master=self.askWindow,
            text="To:"
        )
        entryTo = tk.Entry(master=self.askWindow)

        def end():
            req = rqs.post(
                url+"room/"+self.openRoomName+"/add/limithourweekly",
                params={
                    "passw": self.openRoomPassw,
                    "day": entryDay.get(),
                    "fr": entryFr.get(),
                    "to": entryTo.get()
                }
            )
            if req:
                self.greetingLabel.config(text="Limit added successfully")
            else:
                self.greetingLabel.config(text="Error while adding limit")
            self.askWindow.destroy()

        okbutt = tk.Button(
            master=self.askWindow,
            text="Confirm",
            command=end
        )

        self.askLabel.pack()
        labelDay.pack()
        entryDay.pack()
        labelFr.pack()
        entryFr.pack()
        labelTo.pack()
        entryTo.pack()
        okbutt.pack()
        self.askWindow.focus_force()
        self.askWindow.mainloop()

    def hourLimitBiw(self):
        """opens window to add biweekly hour limit"""
        self.askWindow = tk.Tk()
        self.askLabel = tk.Label(
            master=self.askWindow,
            text="Specify new biweekly hour limit:",
            bg="lime"
        )
        labelDay = tk.Label(
            master=self.askWindow,
            text="Day of week"
        )
        entryDay = tk.Entry(self.askWindow)
        labelWeek = tk.Label(
            self.askWindow,
            text="Week number (even or odd):"
        )
        entryWeek = tk.Entry(self.askWindow)
        labelFr = tk.Label(
            master=self.askWindow,
            text="From:"
        )
        entryFr = tk.Entry(master=self.askWindow)
        labelTo = tk.Label(
            master=self.askWindow,
            text="To:"
        )
        entryTo = tk.Entry(master=self.askWindow)

        def end():
            req = rqs.post(
                url+"room/"+self.openRoomName+"/add/limithourbiweekly",
                params={
                    "passw": self.openRoomPassw,
                    "day": entryDay.get(),
                    "week": entryWeek.get(),
                    "fr": entryFr.get(),
                    "to": entryTo.get()
                }
            )
            if req:
                self.greetingLabel.config(text="Limit added successfully")
            else:
                self.greetingLabel.config(text="Error while adding limit")
            self.askWindow.destroy()

        okbutt = tk.Button(
            master=self.askWindow,
            text="Confirm",
            command=end
        )

        self.askLabel.pack()
        labelDay.pack()
        entryDay.pack()
        labelWeek.pack()
        entryWeek.pack()
        labelFr.pack()
        entryFr.pack()
        labelTo.pack()
        entryTo.pack()
        okbutt.pack()
        self.askWindow.focus_force()
        self.askWindow.mainloop()

    def hourLimitMon(self):
        """opens window to add monthly hour limit"""
        self.askWindow = tk.Tk()
        self.askLabel = tk.Label(
            master=self.askWindow,
            text="Specify new monthly hour limit:",
            bg="lime"
        )
        labelDay = tk.Label(
            master=self.askWindow,
            text="Day of month"
        )
        entryDay = tk.Entry(self.askWindow)
        labelFr = tk.Label(
            master=self.askWindow,
            text="From:"
        )
        entryFr = tk.Entry(master=self.askWindow)
        labelTo = tk.Label(
            master=self.askWindow,
            text="To:"
        )
        entryTo = tk.Entry(master=self.askWindow)

        def end():
            req = rqs.post(
                url+"room/"+self.openRoomName+"/add/limithourmonthly",
                params={
                    "passw": self.openRoomPassw,
                    "day": entryDay.get(),
                    "fr": entryFr.get(),
                    "to": entryTo.get()
                }
            )
            if req:
                self.greetingLabel.config(text="Limit added successfully")
            else:
                self.greetingLabel.config(text="Error while adding limit")
            self.askWindow.destroy()

        okbutt = tk.Button(
            master=self.askWindow,
            text="Confirm",
            command=end
        )

        self.askLabel.pack()
        labelDay.pack()
        entryDay.pack()
        labelFr.pack()
        entryFr.pack()
        labelTo.pack()
        entryTo.pack()
        okbutt.pack()
        self.askWindow.focus_force()
        self.askWindow.mainloop()

    def dayLimitInd(self):
        """opens window to add individual day limit"""
        self.askWindow = tk.Tk()
        self.askLabel = tk.Label(
            master=self.askWindow,
            text="Specify new individual day limit (format: YYYY/MM/DD):",
            bg="lime"
        )
        labelFr = tk.Label(
            master=self.askWindow,
            text="From:"
        )
        entryFr = tk.Entry(master=self.askWindow)
        labelTo = tk.Label(
            master=self.askWindow,
            text="To:"
        )
        entryTo = tk.Entry(master=self.askWindow)

        def end():
            req = rqs.post(
                url+"room/"+self.openRoomName+"/add/limitday",
                params={
                    "passw": self.openRoomPassw,
                    "fr": entryFr.get(),
                    "to": entryTo.get()
                }
            )
            if req:
                self.greetingLabel.config(text="Limit added successfully")
            else:
                self.greetingLabel.config(text="Error while adding limit")
            self.askWindow.destroy()

        okbutt = tk.Button(
            master=self.askWindow,
            text="Confirm",
            command=end
        )

        self.askLabel.pack()
        labelFr.pack()
        entryFr.pack()
        labelTo.pack()
        entryTo.pack()
        okbutt.pack()
        self.askWindow.focus_force()
        self.askWindow.mainloop()

    def dayLimitBiw(self):
        """opens window to add biweekly day limit"""
        self.askWindow = tk.Tk()
        self.askLabel = tk.Label(
            master=self.askWindow,
            text="Specify new biweekly day limit:",
            bg="lime"
        )
        labelWeek = tk.Label(
            self.askWindow,
            text="Week number (even/odd):"
        )
        entryWeek = tk.Entry(self.askWindow)
        labelFr = tk.Label(
            master=self.askWindow,
            text="From:"
        )
        entryFr = tk.Entry(master=self.askWindow)
        labelTo = tk.Label(
            master=self.askWindow,
            text="To:"
        )
        entryTo = tk.Entry(master=self.askWindow)

        def end():
            req = rqs.post(
                url+"room/"+self.openRoomName+"/add/limitdaybiweekly",
                params={
                    "passw": self.openRoomPassw,
                    "week": entryWeek.get(),
                    "fr": entryFr.get(),
                    "to": entryTo.get()
                }
            )
            if req:
                self.greetingLabel.config(text="Limit added successfully")
            else:
                self.greetingLabel.config(text="Error while adding limit")
            self.askWindow.destroy()

        okbutt = tk.Button(
            master=self.askWindow,
            text="Confirm",
            command=end
        )

        self.askLabel.pack()
        labelWeek.pack()
        entryWeek.pack()
        labelFr.pack()
        entryFr.pack()
        labelTo.pack()
        entryTo.pack()
        okbutt.pack()
        self.askWindow.focus_force()
        self.askWindow.mainloop()

    def dayLimitWee(self):
        """opens window to add weekly day limit"""
        self.askWindow = tk.Tk()
        self.askLabel = tk.Label(
            master=self.askWindow,
            text="Specify new weekly day limit:",
            bg="lime"
        )
        labelFr = tk.Label(
            master=self.askWindow,
            text="From:"
        )
        entryFr = tk.Entry(master=self.askWindow)
        labelTo = tk.Label(
            master=self.askWindow,
            text="To:"
        )
        entryTo = tk.Entry(master=self.askWindow)

        def end():
            req = rqs.post(
                url+"room/"+self.openRoomName+"/add/limitdayweekly",
                params={
                    "passw": self.openRoomPassw,
                    "fr": entryFr.get(),
                    "to": entryTo.get()
                }
            )
            if req:
                self.greetingLabel.config(text="Limit added successfully")
            else:
                self.greetingLabel.config(text="Error while adding limit")
            self.askWindow.destroy()

        okbutt = tk.Button(
            master=self.askWindow,
            text="Confirm",
            command=end
        )

        self.askLabel.pack()
        labelFr.pack()
        entryFr.pack()
        labelTo.pack()
        entryTo.pack()
        okbutt.pack()
        self.askWindow.focus_force()
        self.askWindow.mainloop()

    def dayLimitMon(self):
        """opens window to add monthly day limit"""
        self.askWindow = tk.Tk()
        self.askLabel = tk.Label(
            master=self.askWindow,
            text="Specify new monthly day limit:",
            bg="lime"
        )
        labelFr = tk.Label(
            master=self.askWindow,
            text="From:"
        )
        entryFr = tk.Entry(master=self.askWindow)
        labelTo = tk.Label(
            master=self.askWindow,
            text="To:"
        )
        entryTo = tk.Entry(master=self.askWindow)

        def end():
            req = rqs.post(
                url+"room/"+self.openRoomName+"/add/limitdaymonthly",
                params={
                    "passw": self.openRoomPassw,
                    "fr": entryFr.get(),
                    "to": entryTo.get()
                }
            )
            if req:
                self.greetingLabel.config(text="Limit added successfully")
            else:
                self.greetingLabel.config(text="Error while adding limit")
            self.askWindow.destroy()

        okbutt = tk.Button(
            master=self.askWindow,
            text="Confirm",
            command=end
        )

        self.askLabel.pack()
        labelFr.pack()
        entryFr.pack()
        labelTo.pack()
        entryTo.pack()
        okbutt.pack()
        self.askWindow.focus_force()
        self.askWindow.mainloop()

    def removeLimitInd(self):
        """opens a window to remove one individual limit"""
        req = rqs.get(
            url+"room/"+self.openRoomName+"/check/limithour",
            params={"passw": self.openRoomPassw}
        )
        if req.text == "[]":
            self.greetingLabel.config(text="No limits of this type")
        else:
            self.askWindow = tk.Tk()
            self.askLabel = tk.Label(
                self.askWindow,
                text="Choose which limit to remove",
                bg="red"
            )
            self.askLabel.pack()
            selection = tk.IntVar(self.askWindow)
            radio = []
            i = 0
            for limit in req.json():
                txtdt = dt.strptime(limit[0], "%Y-%m-%dT%H:%M:%S")
                txt = dt.strftime(txtdt, "%c - ")
                txtdt = dt.strptime(limit[1], "%Y-%m-%dT%H:%M:%S")
                txt += dt.strftime(txtdt, "%c")
                radio.append(tk.Radiobutton(
                    self.askWindow,
                    text=txt,
                    value=i,
                    var=selection
                ))
                i += 1
            for r in radio:
                r.pack()

            def end():
                req = rqs.delete(
                    url+"room/"+self.openRoomName+"/remove/limithour",
                    params={
                        "passw": self.openRoomPassw,
                        "nr": str(selection.get())
                    }
                )
                if req:
                    text = "Limit removed successfully"
                else:
                    text = "Error while removing limit"
                self.greetingLabel.config(text=text)
                self.askWindow.destroy()
            button = tk.Button(
                self.askWindow,
                text="Remove selected",
                command=end
            )
            button.pack()
            self.askWindow.focus_force()
            self.askWindow.mainloop()

    def removeLimitDay(self):
        """opens a window to remove one daily limit"""
        req = rqs.get(
            url+"room/"+self.openRoomName+"/check/limithourdaily",
            params={"passw": self.openRoomPassw}
        )
        if req.text == "[]":
            self.greetingLabel.config(text="No limits of this type")
        else:
            self.askWindow = tk.Tk()
            self.askLabel = tk.Label(
                self.askWindow,
                text="Choose which limit to remove",
                bg="red"
            )
            self.askLabel.pack()
            selection = tk.IntVar(self.askWindow)
            radio = []
            i = 0
            for limit in req.json():
                txt = ""
                if limit[0] < 10:
                    txt += "0"
                txt += str(limit[0])
                txt += " - "
                x = limit[1]
                if x > 23:
                    x -= 24
                if x < 10:
                    txt += "0"
                txt += str(x)
                radio.append(tk.Radiobutton(
                    self.askWindow,
                    text=txt,
                    value=i,
                    var=selection
                ))
                i += 1
            for r in radio:
                r.pack()

            def end():
                req = rqs.delete(
                    url+"room/"+self.openRoomName+"/remove/limithourdaily",
                    params={
                        "passw": self.openRoomPassw,
                        "nr": str(selection.get())
                    }
                )
                if req:
                    text = "Limit removed successfully"
                else:
                    text = "Error while removing limit"
                self.greetingLabel.config(text=text)
                self.askWindow.destroy()

            button = tk.Button(
                self.askWindow,
                text="Remove selected",
                command=end
            )
            button.pack()
            self.askWindow.focus_force()
            self.askWindow.mainloop()

    def removeLimitWee(self):
        """opens a window to remove one weekly limit"""
        req = rqs.get(
            url+"room/"+self.openRoomName+"/check/limithourweekly",
            params={"passw": self.openRoomPassw}
        )
        if req.text == "[]":
            self.greetingLabel.config(text="No limits of this type")
        else:
            self.askWindow = tk.Tk()
            self.askLabel = tk.Label(
                self.askWindow,
                text="Choose which limit to remove",
                bg="red"
            )
            self.askLabel.pack()
            selection = tk.IntVar(self.askWindow)
            radio = []
            i = 0
            for limit in req.json():
                txt = cal.day_abbr[limit[0]-1]
                txt += ": "
                txt += str(limit[1])
                txt += " - "
                txt += str(limit[2])
                radio.append(tk.Radiobutton(
                    self.askWindow,
                    text=txt,
                    value=i,
                    var=selection
                ))
                i += 1
            for r in radio:
                r.pack()

            def end():
                req = rqs.delete(
                    url+"room/"+self.openRoomName+"/remove/limithourweekly",
                    params={
                        "passw": self.openRoomPassw,
                        "nr": str(selection.get())
                    }
                )
                if req:
                    text = "Limit removed successfully"
                else:
                    text = "Error while removing limit"
                self.greetingLabel.config(text=text)
                self.askWindow.destroy()
            button = tk.Button(
                self.askWindow,
                text="Remove selected",
                command=end
            )
            button.pack()
            self.askWindow.focus_force()
            self.askWindow.mainloop()

    def removeLimitBiw(self):
        """opens a window to remove one biweekly limit"""
        req = rqs.get(
            url+"room/"+self.openRoomName+"/check/limithourbiweekly",
            params={"passw": self.openRoomPassw}
        )
        if req.text == "[]":
            self.greetingLabel.config(text="No limits of this type")
        else:
            self.askWindow = tk.Tk()
            self.askLabel = tk.Label(
                self.askWindow,
                text="Choose which limit to remove",
                bg="red"
            )
            self.askLabel.pack()
            selection = tk.IntVar(self.askWindow)
            radio = []
            i = 0
            for limit in req.json():
                txt = cal.day_abbr[limit[0]-1]
                if limit[1] % 2 == 0:
                    txt += " even: "
                else:
                    txt += " odd: "
                txt += str(limit[2])
                txt += " - "
                txt += str(limit[3])
                radio.append(tk.Radiobutton(
                    self.askWindow,
                    text=txt,
                    value=i,
                    var=selection
                ))
                i += 1
            for r in radio:
                r.pack()

            def end():
                req = rqs.delete(
                    url+"room/"+self.openRoomName+"/remove/limithourbiweekly",
                    params={
                        "passw": self.openRoomPassw,
                        "nr": str(selection.get())
                    }
                )
                if req:
                    text = "Limit removed successfully"
                else:
                    text = "Error while removing limit"
                self.greetingLabel.config(text=text)
                self.askWindow.destroy()
            button = tk.Button(
                self.askWindow,
                text="Remove selected",
                command=end
            )
            button.pack()
            self.askWindow.focus_force()
            self.askWindow.mainloop()

    def removeLimitMon(self):
        """opens a window to remove one monthly limit"""
        req = rqs.get(
            url+"room/"+self.openRoomName+"/check/limithourmonthly",
            params={"passw": self.openRoomPassw}
        )
        if req.text == "[]":
            self.greetingLabel.config(text="No limits of this type")
        else:
            self.askWindow = tk.Tk()
            self.askLabel = tk.Label(
                self.askWindow,
                text="Choose which limit to remove",
                bg="red"
            )
            self.askLabel.pack()
            selection = tk.IntVar(self.askWindow)
            radio = []
            i = 0
            for limit in req.json():
                txt = "Day "
                if limit[0] < 10:
                    txt += "0"
                txt += str(limit[0])
                txt += ": "
                txt += str(limit[1])
                txt += " - "
                txt += str(limit[2])
                radio.append(tk.Radiobutton(
                    self.askWindow,
                    text=txt,
                    value=i,
                    var=selection
                ))
                i += 1
            for r in radio:
                r.pack()

            def end():
                req = rqs.delete(
                    url+"room/"+self.openRoomName+"/remove/limithourmonthly",
                    params={
                        "passw": self.openRoomPassw,
                        "nr": str(selection.get())
                    }
                )
                if req:
                    text = "Limit removed successfully"
                else:
                    text = "Error while removing limit"
                self.greetingLabel.config(text=text)
                self.askWindow.destroy()
            button = tk.Button(
                self.askWindow,
                text="Remove selected",
                command=end
            )
            button.pack()
            self.askWindow.focus_force()
            self.askWindow.mainloop()

    def setRequirement(self):
        """opens window to set required period length"""
        self.askWindow = tk.Tk()
        self.askLabel = tk.Label(
            master=self.askWindow,
            text="Choose minimum length of free period",
            bg="yellow"
        )
        entry = tk.Entry(master=self.askWindow)

        def end():
            req = rqs.post(
                url+"room/"+self.openRoomName+"/set/reqlenh",
                params={"passw": self.openRoomPassw, "req": entry.get()}
            )
            self.askWindow.destroy()

        okbutt = tk.Button(
            master=self.askWindow,
            text="Confirm choice",
            command=end
        )

        self.askLabel.pack()
        entry.pack()
        okbutt.pack()
        self.askWindow.focus_force()
        self.askWindow.mainloop()

    def seekFree(self):
        """shows results of looking for free periods"""
        if not self.maxInput.get():
            self.greetingLabel.config("Enter max number of periods of time")
        else:
            req = rqs.get(
                url+"room/"+self.openRoomName+"/freetime/"+self.maxInput.get(),
                params={"passw": self.openRoomPassw}
            )
            self.resultWindow = tk.Tk()
            self.resultLabel = tk.Label(
                master=self.resultWindow,
                bg="cyan",
                text="Found free periods:"
            )
            self.resultLabel.pack()
            res = req.json()
            for period in res:
                time = dt.strptime(period[0], "%Y-%m-%dT%H:%M:%S")
                txt = dt.strftime(time, "%c")
                time = dt.strptime(period[-1], "%Y-%m-%dT%H:%M:%S")
                time += tdl(hours=1)
                txt += dt.strftime(time, " - %c")

                label = tk.Label(master=self.resultWindow, text=txt)
                self.resultList.append(label)
                self.resultList[-1].pack()
            self.resultWindow.mainloop()


x = GUI()
x.run()
