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
        dictionary = '{"lastcode": 1}' # 
finally: # set last code used + 1
    encoder = Encoder(dictionary["lastcode"])

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

        if form.submit.data: # The user wants to transform the data
            logger.info("ACTION: TRANSFORM")

            if (hostname in destiny): # The destiny includes the HOSTNAME
                logger.info("URL already existng, returning saved data")
                destiny = destiny[len(hostname):] # Get the code after "HOSTNAME/"
                if dictionary[destiny]:
                    # The local URL is in the Dictionary
                    logger.info ("Destiny for " + destiny + " has been found and it's " + dictionary[destiny])
                    newURL = dictionary[destiny] # Look for the original URL in the dictionary
                else:
                    # The local URL is not in the Dictionary
                    logger.error ("MAIN:INDEX() - Hostname " + hostname + " was in Destiny " + destiny + ", but it's value was empty")

            else: # The destiny is a real URL

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


        elif (form.remove.data): # The user wants to remove the data
            logger.debug("ACTION: REMOVE")
            if destiny[len(hostname):] in dictionary.keys(): # destiny is a local URL
                destiny = destiny[len(hostname):] # shortnen destiny just once
                logger.info("Removing " + dictionary[destiny] + ":" + hostname+destiny)
                dictionary.pop(destiny) # Remove destiny from dictionary
                saveDictToDisk()

            elif destiny in dictionary.values(): # destiny is a real URL
                logger.info("Destiny " + destiny + " exists in the dictionary.\nLooking for it's key")
                for key in dictionary:
                    if dictionary[key] == destiny:
                        logger.info("Removing " + key + ":" + destiny)
                        dictionary.pop(key)
                        saveDictToDisk()
                        break

            else: # destiny is not part of the dictionary
                logger.info("ERROR - " + destiny + " is not listed")


    return render_template('index.html', methods=["POST"], title="URL Shortener", form=form, newURL=newURL)




@app.route("/<input>", methods=["GET"])
def reroute(input):
    """ For any link that is not index, it will search input in the dictionary and send the user to it """
    if (input in dictionary.keys()): # Check if newURL actually exists
        destiny = dictionary[input]
        logger.info("gonna take you to " + destiny)
        return redirect(destiny)
    else: # Send to INDEX page if the new URL didn't exist
        return redirect(hostname)




@app.route("/debug/json", methods=["GET"])
def json():
    """ Expose the local json over the webpage """
    return render_template('json.html', json=str(dictionary))




def updateLocalDict(destiny, newURL):
    """ Hold on memory the current dictionary
        This won't save the current dictionary in disk

        Example:
            updateLocalDict(encoded, destinyURL)
            updateLocalDict(XXYYZZ, http://google.com)
        """
    dictionary["lastcode"] = encoder.getID()
    dictionary[newURL] = destiny
    return




def saveDictToDisk():
    """ Save the current dictionary into the disk """
    fileManager.writeDict(dictionary)
    # fileManager.addItem(destiny, newURL)

if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=80, debug=True) # FOR SERVER TESTING
    app.run(debug=True) # FOR LOCAL TESTING


# while(True):
#     print("//////////////////////////")
#     destiny = input("URL to reduce: ")
#     print(encoder.long2shrt(destiny))
#     print(encoder.getCode(key="ricky")) # Use 'key = destiny' to get a specific code for that destiny
#     print(encoder.shrt2long(hostname+"2"))