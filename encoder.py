import logging # Import logging

id = 1

class Encoder():
    """ THIS IS THE ENCODER CLASS """

    def __init__(self, id = 1):
        hostname = "http://localhost:80/"
        self.id = id

        ### ENABLE LOGS ###
        LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"
        # logging.basicConfig(filename = "/logs.log", level=logging.DEBUG, format=LOG_FORMAT) # FOR SERVER TESTING
        logging.basicConfig(filename = "/urlshortener/logs.log", level=logging.DEBUG, format=LOG_FORMAT) # FOR LOCAL TESTING
        logger = logging.getLogger()

    def long2shrt (self):
        """ Will shorten destiny into a new URL.\n
        I won't check has been already added."""

        # Creating new entry
        # Generating new URL code
        newURL = self.base62(self.id)
        self.id += 1
        return newURL
        
    def base62(self, index):
        """ Transform an INT into an encoded string on base62"""

        # Set the possible characters
        characters = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        base = len(characters) # Get the amount of character for possible encoding
        newID = [] # This will append all the characters

        while index > 0:
            val = index % base # Get a value between 0 to 61
            newID.append(characters[val]) # Add to the returning value a character
            index = index // base # Reduce the original index

        return "".join(newID[::-1]) # Reverse one by one the characters

    def getID(self):
        return self.id