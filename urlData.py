import time

local = ""
remote = ""
calls = 0
born = 0.0
lastUsed = 0.0

class URLData():
    """ This object carries the data for every URL.\n
    It requires a Local argument with the custom URL.\n
    It requires a Remote argument with the destiny URL.\n
    Example:
        URLData(newURL, destiny,) """

    def __init__(self, local, domain, calls = 0, born = time.time(), lastUsed = 0.0):
        self.local = local
        self.domain = domain
        self.born = born
        self.calls = calls
        self.lastUsed = lastUsed

    def getLocal():
        """ Returns local's URL """
        return self.local

    def getRemote():
        """ Returns remote's URL """
        return self.remote

    def getCalls():
        """ Returns the amount of Calls """
        return self.calls

    def getBorn():
        """ Returns born date in time() format """
        return self.born

    def getLastUsed():
        """ Returns last time used in time() format """
        return self.lastUsed