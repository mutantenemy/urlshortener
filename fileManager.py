import logging # Enable logging
import os # Enable OS tools
import json

# Define logs file
workspace = "/home/taitz/Documents/Python/urlshortener"
logsFile = workspace + "/logs.log"
dictionary = workspace + "/dict.json"

 ### ENABLE LOGS ###
LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"
logging.basicConfig(filename = logsFile, level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger()

class FileManager:
    """ This objects manages interaction with the OS and it's file system """

    def readDict(self):
        """ Open the dictionary in memory """
        data = {}
        try:
            logging.info("Opeining dict.json")
            with open(dictionary, "r") as json_file:
                logging.info("dict.json has successfuly opened")
                data = json.load(json_file)
            logging.debug("Dictionary contains: " + str(data))
            return data
        except OSError:
            print("!CRITICAL! - DICTIONARY FILE NOT FOUND AT "+dictionary)
            logger.critical("!CRITICAL! - DICTIONARY FILE NOT FOUND AT "+dictionary)
            return {}

    def writeDict(self, data):
        """ Save Dictionary's data into filesystem """
        try:
            with open(dictionary, 'w') as json_file:
                json.dump(data, json_file)
        except OSError:
            print("!CRITICAL! - DICTIONARY FILE NOT FOUND AT "+dictionary)
            logger.critical("!CRITICAL! - DICTIONARY FILE NOT FOUND AT "+dictionary)
        finally:
            return

    def addItem(self, destiny, newURL):
        """ Add a new entry into the Dictonary
            item must be a tuple """
        logging.info("FileManager called to add a new item")
        data = {}
        logging.info("Starting to read the dictionary")
        data = self.readDict()
        logging.info("Reading dictionary ended")
        logging.info("Starting to append new items" + destiny + ":" + newURL)
        data[destiny] = newURL
        logging.info("Starting to write into the dictionary")
        self.writeDict(data)
        logging.info("Writing dictionary ended")
        return

    def rmvItem(self, item):
        """ pop out an item from the dictionary """

    def backup(self):
        """ save a backup of the dictionary """

    def createLink(self, code):
        """ Create a new link with the following Code """

    def destroyLink(self, code = None, destiny = None):
        """ Destroy a link by destiny's URL or by Code """