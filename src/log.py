import sys

class Logging:
    def __init__(self, level=0):
        self.set_level(level)

    def set_level(self, _level):
        if(type(_level)!=int or _level<0): raise ValueError("level must be positive integar, got %s"%_level)
        self.level=_level

    def _log(self, message, level):
        if(level<=self.level): sys.stdout.write(message)

    def debug(self, message):
        self._log(message,3)

    def info(self, message):
        self._log(message,2)

    def warn(self, message):
        self._log(message,1)

    def __repr__(self):
        s_level = ("quiet", "warn", "info", "debug")
        l = min(self.level,3)
        return("logging level: %s"%s_level[l])

        
if(__name__=="__main__"):
    l = Logging(0)
    l.set_level(6)
    l.debug("debug\n")
    l.info("info\n")
    l.warn("warn\n")
    print(l)
