#########################################################
#                                                       #
#                   TOMAS ADAM TAITZ                    #
#                                                       #
#########################################################

from flask import Flask, escape, request, render_template, url_for, redirect # Flask tools
import logging # Enable logging
import os # Enable OS tools
from encoder import Encoder # This is our links manager
from forms import Transform # This is our Flask webpage
from fileManager import FileManager, logsFile # This will manage out filesystem
# from orchestrator import Orchestrator


# fileManager will be responsible in interacting with our OS's file system
fileManager = FileManager()


# Define logs file
# logsFile = fileManager.logsFile

 ### ENABLE LOGS ###
LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"
logging.basicConfig(filename = logsFile, level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger()

### Clear logger ###
try:
    open(logsFile, "w").close()
except OSError:
    print("!CRITICAL! - LOGS FILE NOT FOUND AT "+logsFile)
    logger.critical("!CRITICAL! - LOGS FILE NOT FOUND AT "+logsFile)


# orchestrator = Orchestrator()
encoder = Encoder()
hostname = "http://localhost:5000/"
dictionary = {} # Here we will store all the elements

dictionary = fileManager.readDict()

# Call for FLASK
app = Flask(__name__)

# Secret Key
app.config['SECRET_KEY'] = '5d071b5d37b540f9c327e85f9f39f048'

# Create webpages
@app.route('/', methods=["GET", "POST"]) #index
@app.route('/index', methods=["GET", "POST"])
def index():
    ## return render_template(INDEXFILENAME.HTML, DATA)
    form = Transform() # Get custom form
    destiny = None
    newURL = None

    # When the form is valid
    if form.validate_on_submit():
        destiny = str({form.url.data}) # Get destiny from the form, if any
        if (hostname in destiny):
            # The destiny includes the HOSTNAME
            logger.info("URL already existng, returning saved data")
            for key in dictionary: # Look for the URL on the dictionary
                if dictionary[key] == destiny:
                    logger.info ("Destiny for " + destiny + " has been found and it's " + key)
                    newURL = key
            # newURL = encoder.shrt2long(destiny) # GET THE ORIGNAL URL
        else:
            # The destiny is a real URL

            # Is the destiny already in the dictionary?
            if destiny in dictionary:
                logger.info("Encoding for " + destiny + " already exists as " + dictionary[destiny])
                newURL = dictionary[destiny]
            else:
                logger.info("Encoding " + destiny)
                newURL = encoder.long2shrt(destiny)
                logger.info("updating Local Dictionary function")
                updateLocalDict(destiny, newURL)
                saveDictToDisk()
                logger.info("AddItem has returned")
        # return redirect(url_for("index"))
    return render_template('index.html', methods=["POST"], title="URL Shortener", form=form, newURL=newURL)


def updateLocalDict(destiny, newURL):
    """ Hold on memory the current dictionary
        This won't save the current dictionary in disk

        Example:
            updateLocalDict(destinyURL, localURL)
            updateLocalDict(http://google.com, localhost/XXYYZZ)
        """
    dictionary[destiny] = newURL
    return

def saveDictToDisk():
    """ Save the current dictionary into the disk """
    fileManager.writeDict(dictionary)
    # fileManager.addItem(destiny, newURL)


# while(True):
#     print("//////////////////////////")
#     destiny = input("URL to reduce: ")
#     print(encoder.long2shrt(destiny))
#     print(encoder.getCode(key="ricky")) # Use 'key = destiny' to get a specific code for that destiny
#     print(encoder.shrt2long(hostname+"2"))