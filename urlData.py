import time
import logging

local = ""
remote = ""
calls = 0
born = 0.0
lastUsed = 0.0

### ENABLE LOGS ###
LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"
# logging.basicConfig(filename = "/logs.log", level=logging.DEBUG, format=LOG_FORMAT) # FOR SERVER TESTING
logging.basicConfig(filename = "/home/taitz/Documents/Python/urlshortener/logs.log", level=logging.DEBUG, format=LOG_FORMAT) # FOR LOCAL TESTING
logger = logging.getLogger()

class URLData():
    """ This object carries the data for every URL.\n
    It requires a Local argument with the custom URL.\n
    It requires a Remote argument with the destiny URL.\n
    Example:
        URLData(newURL, destiny,) """

    def __init__(self, local, remote, calls = 0, born = time.time(), lastUsed = 0.0, urlData=None):
        """ Makes a URLData object. \n
        You can import a urlData list as follows:
            [local, remote, calls, born, lastUsed]"""
        if (urlData):
            fromList(urlData)
        else:
            self.local = local
            self.remote = remote
            self.born = born
            self.calls = calls
            self.lastUsed = lastUsed

    def getLocal(self):
        """ Returns local's URL """
        return self.local

    def getRemote(self):
        """ Returns remote's URL """
        return self.remote

    def getCalls(self):
        """ Returns the amount of Calls """
        return self.calls

    def getBorn(self):
        """ Returns born date in time() format """
        return self.born

    def getLastUsed(self):
        """ Returns last time used in time() format """
        return self.lastUsed

    def call(self):
        """ Add a call to this object """
        self.calls += 1
        return

    def getList(self):
        """ Return a list of the whole object as follows:
            [local, remote, calls, born, lastUsed] """
        items = [self.local, self.remote, self.calls, self.born, self.lastUsed]
        logger.debug("ITEMS: " + items[1])
        return items

    def fromList(self, list):
        """ Provide a list with URLData to create an object.
        List but be written as follows:
            [local, remote, calls, born, lastUsed] """
        self.local = list[0]
        self.remote = list[1]
        self.calls = list[2]
        self.born = list[3]
        self.lastUsed = list[4]