import datetime


class Bulder(object):
    def __init__(self):
        self.learn = ""
        self.sleep = ""
        self.sport = ""
        self.time = str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute)
        self.mentors = ""

    def setLearn(self, result: str):
        self.learn = result

    def setSleep(self, result: str):
        self.sleep = result

    def setSport(self, result: str):
        self.sport = result

    def setMentors(self, result: str):
        self.mentors = result

    def setTime(self, result: str):
        self.time = result
