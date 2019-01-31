
import os 

from log_config import log, pformat

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### FLASK-SOCKETIO
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
from flask_socketio import SocketIO

from solidata_api.application import create_app

app = create_app( app_name='SOLIDATA_API', run_mode="prod" )

if __name__ == "main" :
  	
	log.debug("\n--- STARTING SOLIDATA API (PROD) ---\n")

	### initiate socketio
	socketio = SocketIO(app)
	
	app.run()