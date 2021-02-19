#########################################################
#                                                       #
#                   TOMAS ADAM TAITZ                    #
#                                                       #
#########################################################

from flask import Flask, escape, request, render_template, url_for, redirect # Flask tools
import logging # Enable logging
import os # Enable OS tools
import time # Use time to get last access
from encoder import Encoder # This is our links manager
from forms import Transform # This is our Flask webpage
from fileManager import FileManager, logsFile # This will manage out filesystem
from urlData import URLData
# from orchestrator import Orchestrator


# fileManager will be responsible in interacting with our OS's file system
fileManager = FileManager()


# Define logs file
#logsFile = fileManager.logsFile

 ### ENABLE LOGS ###
LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"
# logging.basicConfig(filename = "/logs.log", level=logging.DEBUG, format=LOG_FORMAT) # FOR SERVER TESTING
logging.basicConfig(filename = "/home/taitz/Documents/Python/urlshortener/logs.log", level=logging.DEBUG, format=LOG_FORMAT) # FORM LOCAL TESTING
logger = logging.getLogger()

### Clear logger ###
try:
    open(logsFile, "w").close()
except OSError:
    print("!CRITICAL! - LOGS FILE NOT FOUND AT "+logsFile+"\nCreating a new logs file")
    logger.critical("!CRITICAL! - LOGS FILE NOT FOUND AT "+logsFile+"\nCreating a new logs file")
    f = open(logsFile, "xt") # Create a new logs file
    f.close # close file


# orchestrator = Orchestrator()

hostname = "http://localhost:5000/"
dictionary = {} # Here we will store all the elements

try: # GET STARTING JSON
    dictionary = fileManager.readDict() # Load saved dictionary
except TypeError: # AN ERROR HAS OCCURED WHILE OPEINING THE JSON
    logger.error("A TYPE error has occurred while opening the dict.json\nTrying one last time")
    try: # TRY ONE LAST TIME TO OPEN THE JSON OR CREATE A VOLATIL DICTIONARY
        dictionary = fileManager.readDict() # Load saved dictionary
    except TypeError: # JSON KEEPS SENDING AN ERROR. CREATE A VOLATIL DICTIONARY
        logger.critical("! CRITICAL ! JSON was not able to load up. Creating a virtual dictionary.\n!!!THIS DATA MIGHT GET LOST!!!")
        dictionary = {"lastcode": 1}#
encoder = Encoder(id = dictionary["lastcode"])

# Call for FLASK
app = Flask(__name__)

# Secret Key
app.config['SECRET_KEY'] = '5d071b5d37b540f9c327e85f9f39f048'




# Create webpages
@app.route('/', methods=["GET", "POST"]) #index
def index():
    """ This is the main webpage.\n
    It creates a form where the user writes a URL and it delivers a corresponding code (if remote URL) or an actual webpage (if local URL)\n  """
    ## return render_template(INDEXFILENAME.HTML, DATA)
    form = Transform() # Get custom form
    destiny = None
    newURL = None
    message = None

    # When the form is valid
    if form.validate_on_submit():

        destiny = str(form.url.data) # Get destiny from the form, if any

        if form.submit.data: # The user wants to transform the data
            logger.info("ACTION: TRANSFORM")

            if (hostname in destiny): # The destiny includes the HOSTNAME
                logger.info("URL already existng, returning saved data")
                destiny = destiny[len(hostname):] # Get the code after "HOSTNAME/"

                if dictionary[destiny]: # Does the code exist in the Dictionary?
                    # The local URL is in the Dictionary
                    logger.info ("Destiny for " + destiny + " has been found.")
                    data = dictionary[destiny] # Get the full list from the local URL
                    newURL = data[1] # Get the Remote URL from the list associated to the local URL
                    logger.info("Local URL " + destiny + " is associated to " + newURL)
                else: # The local URL is not part of the dictionary
                        logger.warning ("MAIN:INDEX() - Local URL " + destiny + " is not part of the saved data.")

            else: # The destiny is a real URL

                # Is the destiny already in the dictionary?
                logger.info("Check if " + destiny + " already exists.")
                if destiny in str(dictionary): # destiny is in the dictionary.
                    logger.info(destiny + " exists. Extracting code")
                    newURL = long2shrt(destiny) # Get code
                    newURL = hostname + newURL # Printable version
                else: # Failed to find destiny in the dictionary. Create a new entry.
                    logger.info("Generating new code")
                    newCode = encoder.long2shrt()
                    logger.info("Creating new URLData object")
                    urlData = URLData(newCode, destiny)
                    logger.info("Updating Local Dictionary")
                    updateLocalDict(newCode, urlData)
                    saveDictToDisk()
                    logger.info("Saving to Disk has ended")
                    newURL = hostname + newCode # Final URL will be the hostname + the new encoding

                # if destiny in dictionary.values():
                #     logger.info("Destiny " + destiny + " already exists in the dictionary.\nLooking for it's key")
                #     for key in dictionary:
                #         if dictionary[key] == destiny:
                #             newCode = key
                #             break
                #     logger.info("Encoding for " + destiny + " already exists as " + dictionary[newCode])
                #     newURL = hostname + newCode
                # else:
                        # logger.info("Destiny " + destiny + " doesn't exists in the dictionary\nEncoding " + destiny)
                        # #TODO que devuelva solo el encodeado, no el hostname
                        # newCode = encoder.long2shrt()
                        # logger.info("updating Local Dictionary function")
                        # updateLocalDict(destiny, newCode)
                        # saveDictToDisk()
                        # logger.info("Saving to Disk has ended")
                        # newURL = hostname + newCode # Final URL will be the hostname + the new encoding


        elif form.remove.data: # The user wants to remove the data
            logger.debug("ACTION: REMOVE")
            localURL = None

            if destiny[len(hostname):] in dictionary.keys(): # destiny is a local URL
                logger.info("The URL is registered and it's local")
                localURL = destiny[len(hostname):] # shortnen destiny just once
                remoteURL = dictionary[localURL][1]

            elif destiny in str(dictionary): # Look if the destiny is registered
                logger.info("The Remote URL is registered")
                localURL = long2shrt(destiny) # Get the local URL for the remote one
                remoteURL = destiny

            else:
                logger.info("The URL " + destiny + " wasn't in the registry")
                message = "The URL " + destiny + " wasn't in the registry"

            if(localURL): # True if there is a URL to remove
                dictionary.pop(localURL) # Destroy link between local and remote URL
                saveDictToDisk()
                logger.info("Link between " + localURL + " and " + remoteURL + " has been destroyed.")
                message = "Link between " + localURL + " and " + remoteURL + " has been destroyed."

    return render_template('index.html', methods=["POST"], title="URL Shortener", form=form, newURL=newURL, message=message)




@app.route("/<input>", methods=["GET"])
def reroute(input):
    """ For any link that is not index, it will search input in the dictionary and send the user to it. """

    if (input in dictionary.keys()): # Check if newURL actually exists
        destiny = dictionary[input][1] # Get the Remote URL from the corresponding JSON
        updateDestinyData(input)
        saveDictToDisk()
        logger.info("gonna take you to " + destiny)
        return redirect(destiny)
    else: # Send to INDEX page if the new URL didn't exist
        return redirect(hostname)




@app.route("/debug/json", methods=["GET"])
def json(): # View json
    """ Expose the local json over the webpage """
    return render_template('json.html', json=str(dictionary))




def long2shrt(remoteURL): # Get the Local URL for an existing Remote URL.
    """ Get the Local URL for an existing Remote URL.\n
    Example:
        localURL = long2shrt(remoteURL)
        localURL = long2shrt("http://google.com")"""
    logger.info("Looking at all the values")
    for value in dictionary.values(): # Get every value
        try: # The first item of the JSON is not serialized
            r = value[1]
            # logger.debug("Looking at URLData for " + value.getLocal() ":" + value.getRemote() )
        except TypeError:
            logger.warning("Tried to load a json for item " + str(value) + " but it wasn't serialized.")
        else:
            try:
                if remoteURL == r: # If the remote URL value has been found, return the local URL
                    logger.info("Remote URL " + remoteURL + " is associated to local " + value[0])
                    return value[0] # Return local URL
            except AttributeError: # This occurs it's trying to open a non URLData object.
                logger.warning("Tried to get the Remote URL for " + str(value) + " but it wasn't a URLDeta object.")
            except UnboundLocalError:
                logger.warning("Tried to get the Remote URL for " + str(value) + " but it wasn't a big enough list")
    # The remoteURL is not part of dictionary
    logger.info(remoteURL + " is not part of the saved dictionary")
    return None



def updateLocalDict(newURL, urlData): # locally save the new entry
    """ Hold on memory the current dictionary.\n
        This won't save the current dictionary in disk

        Example:
            updateLocalDict(encoded, urlData)
            updateLocalDict(XXYYZZ, http://google.com)
        """
    dictionary[newURL] = urlData.getList()
    return



def updateDestinyData(key): # Update the information of given generated URL
    """ Update local dictionary when a URL is triggered.\n
    It adds 1 to the count of times accessed.\n
    It updates the last time accessed.\n
    It updated local dictionary"""

    dictionary[key][2] = dictionary[key][2] + 1 # Increase the amount of times URL has been accessed
    dictionary[key][4] = time.asctime(time.localtime(time.time())) # Update date it was accessed
    return




def saveDictToDisk(): # Save local dictionary to disk
    """ Save the current dictionary into the disk """
    fileManager.writeDict(dictionary)
    # fileManager.addItem(destiny, newURL)




if __name__ == '__main__': # SERVER DEBUG OPTIONS
    # app.run(host="0.0.0.0", port=80, debug=True) # FOR SERVER TESTING
    app.run(debug=True) # FOR LOCAL TESTING