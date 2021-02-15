import logging # Import logging

id = 1

class Encoder():
    """ THIS IS THE ENCODER CLASS """

    def __init__(self, id):
        hostname = "http://localhost:5000/"
        self.id = id

        ### ENABLE LOGS ###
        LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"
        logging.basicConfig(filename = "/home/taitz/Documents/Python/urlshortener/logs.log", level=logging.DEBUG, format=LOG_FORMAT)
        logger = logging.getLogger()

    def long2shrt (self, destiny):
        """ Will shorten destiny into a new URL.\n 
        I won't check has been already added."""

        # Creating new entry
        # Generating new URL code
        newURL = self.base62(self.id)
        self.id += 1
        return newURL


    # def shrt2long (self, newURL):
    #     """ DEPRECATED Transforms an encoded URL into the actual destiny"""
    #     destiny = None
    #     logging.info("Looking for " + newURL + " actual destiny")

    #     # Does the generated URL already exist?
    #     for key in self.url2id.keys():
    #         logging.debug("Looking into the dictonary for key: " + key + " which contains " + str(self.url2id[key]))
    #         # The generated URL exists in the dictionary
    #         if newURL[-1] == str(self.url2id[key]):
    #             logging.info("I've found " + str(key) + " for the URL code " + newURL[-1])
    #             destiny = str(key)
    #             return (newURL + " is actually " + destiny)
    #     # The generated URL doesn't exist in the dictionary
    #     logging.warn(newURL + " was no were to be found in the dictionary.\nUse DEBUG logs to view the contents of the dictionary.")
    #     logging.debug(self.url2id.items())
    #     return ("Destiny for " + newURL + " has not being created. Try adding it first.")


    # def getCode (self, key = None):
    #     """ DEPRECATED - Print in console all the tuples\n
    #     use a KEY to print a specific tuple"""
    #     if key:
    #         try:
    #             self.url2id[key]
    #         except KeyError:
    #             logging.warn ("encoder.getCode() failed to find key " + key + ".\nKeyError has been correctly handled.")
    #             return ("Destiny " + key + " has not being created. Try adding it first.")
    #         else:
    #             return (key + ":" + str(self.url2id[key]))
    #         finally:
    #             logging.warn ("encoder.getCode() has not returned correctly from it's TRY")
    #             # return False
    #     else:
    #         return self.url2id.items()


    # def check4Existing(self, key):
    #     """ DEPRECATED - Check if URL exists in the dictionary """
    #     return key in self.url2id

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