# -*- encoding: utf-8 -*-

"""
appserver.py  
- creates an application instance and runs the dev server
"""

import os

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### SET LOGGER 
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

from log_config import log, pformat
# log.debug('>>> TESTING LOGGER')


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### RUN APPSERVER
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

if __name__ == '__main__':  

	""" 
	runner for the SOLIDATA backend Flask app 

	in command line just type : 
	"python appserver.py"

	"""

	log.debug("\n--- STARTING SOLIDATA API ---\n")

	from solidata_api.application import create_app

	app = create_app()
	
	app_port 	= int(app.config["DOMAIN_PORT"])
	app_host 	= app.config["DOMAIN_ROOT"]
	app_debug = app.config["DEBUG"]


	# simple flask runner
	print("== "*30)
	app.run( debug=app_debug, host=app_host, port=app_port, threaded=True )