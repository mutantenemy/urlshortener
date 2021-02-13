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
#logsFile = fileManager.logsFile

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

hostname = "http://localhost:5000/"
dictionary = {} # Here we will store all the elements
dictionary = fileManager.readDict()
encoder = Encoder(len(dictionary))

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
        destiny = str(form.url.data) # Get destiny from the form, if any

        if (hostname in destiny):
            # The destiny includes the HOSTNAME
            logger.info("URL already existng, returning saved data")
            destiny = destiny[len(hostname):] # Get the code after "HOSTNAME/"
            if dictionary[destiny]:
                # The local URL is in the Dictionary
                logger.info ("Destiny for " + destiny + " has been found and it's " + dictionary[destiny])
                newURL = dictionary[destiny] # Look for the original URL in the dictionary
            else:
                # The local URL is not in the Dictionary
                logger.error ("MAIN:INDEX() - Hostname " + hostname + " was in Destiny " + destiny + ", but it's value was empty")

        else:
            # The destiny is a real URL

            # Is the destiny already in the dictionary?
            if destiny in dictionary.values():
                logger.info("Destiny " + destiny + " already exists in the dictionary.\nLooking for it's key")
                for key in dictionary:
                    if dictionary[key] == destiny:
                        newCode = key
                        break
                logger.info("Encoding for " + destiny + " already exists as " + dictionary[newCode])
                newURL = hostname + newCode
            else:
                logger.info("Destiny " + destiny + " doesn't exists in the dictionary\nEncoding " + destiny)
                #TODO que devuelva solo el encodeado, no el hostname
                newCode = encoder.long2shrt(destiny)
                logger.info("updating Local Dictionary function")
                updateLocalDict(destiny, newCode)
                saveDictToDisk()
                logger.info("Saving to Disk has ended")
                newURL = hostname + newCode # Final URL will be the hostname + the new encoding
        # return redirect(url_for("index"))
    return render_template('index.html', methods=["POST"], title="URL Shortener", form=form, newURL=newURL)

@app.route("/<input>", methods=["GET"])
def reroute(input):
    """ For any link that is not index, it will search input in the dictionary and send the user to it """
    # TODO Checkear errores
    destiny = dictionary[input]
    logger.info("gonna take you to " + destiny)
    return redirect(destiny)

def updateLocalDict(destiny, newURL):
    """ Hold on memory the current dictionary
        This won't save the current dictionary in disk

        Example:
            updateLocalDict(encoded, destinyURL)
            updateLocalDict(XXYYZZ, http://google.com)
        """
    dictionary[newURL] = destiny
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