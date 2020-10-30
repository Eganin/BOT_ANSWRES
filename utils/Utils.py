import re


class Utils(object):
    def __init__(self): pass

    def is_time_input(self,time: str) -> bool:
        pattern: str = "\d{2}:\d{2}"
        answer = re.fullmatch(pattern=pattern, string=time)
        return True if answer else False
