
import os 

from log_config import log, pformat

from solidata_api.application import create_app

app = create_app( app_name='SOLIDATA_API', run_mode="prod" )

if __name__ == "main" :
  	
	log.debug("\n--- STARTING SOLIDATA API ---\n")

	app.run()