
import os 
from log_config import log, pformat

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ENV VARS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
from dotenv import load_dotenv
from pathlib import Path  # python3 only
env_path_global = Path('.') / '.env.global'
env_path_mongodb = Path('.') / '.env.mongodb'
env_path_mailing = Path('.') / '.env.mailing'

load_dotenv(env_path_global, verbose=True)
load_dotenv(env_path_mongodb, verbose=True)
load_dotenv(env_path_mailing, verbose=True)

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### FLASK-SOCKETIO
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
from flask_socketio import SocketIO

from solidata_api.application import create_app


### READ ENV VARS
run=os.getenv('RUN_MODE', 'prod')
docker=os.getenv('DOCKER_MODE', 'docker_off')
mongodb=os.getenv('MONGODB_MODE', 'distant')

RSA=os.getenv('RSA_MODE', False)
anojwt=os.getenv('ANOJWT_MODE', False)
antispam=os.getenv('ANTISPAM_MODE', False)
antispam_val=os.getenv('ANTISPAM_VAL', 'my-string-to-check')



app = create_app( 
  app_name='SOLIDATA_API_PROD', 

  run_mode=run, 
  docker_mode=docker,
  mongodb_mode=mongodb,

  RSA_mode=RSA,
  anojwt_mode=anojwt,
  antispam_mode=antispam,
  antispam_value=antispam_val,
)

### initiate socketio
socketio = SocketIO(app)

if __name__ == "main" :
  	
	log.debug("\n--- STARTING AUTH API (PROD) ---\n")
	
	app.run()