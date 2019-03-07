# -*- encoding: utf-8 -*-

"""
api_dataset_outputs/__init__.py
"""

from solidata_api.api import *

# from log_config import log, pformat
log.debug("\n>>> api_dataset_outputs ... creating api blueprint for DATASET OUTPUTS")

document_type		= "dso"

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### create blueprint and api wrapper
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

blueprint = Blueprint( 'api_dataset_outputs', __name__, template_folder=app.config["TEMPLATES_FOLDER"] )
# blueprint = Blueprint( 'api_dataset_inputs', __name__, template_folder='templates' )

### enable CORS on blueprint
# CORS(blueprint)

### create API
# api = MyApi(  	blueprint,
api = MyApi(  	blueprint,
						title = "Solidata API : DATASET OUTPUTS",
						version	= app.config["APP_VERSION"],
						description	= app.config["CODE_LINK"] + " : create, list, delete, edit... dataset outputs",
						doc	= '/documentation',
						default = 'edit',
						authorizations = auth_check,
						# security			='apikey' # globally ask for pikey auth
)
# log.debug("api : \n%s", pformat(api.__dict__))

### errors handlers

@api.errorhandler
def default_error_handler(e):
		message = 'An unhandled exception occurred.'
		log.exception(message)

		if not app.config["FLASK_DEBUG"]:
				return {'message': message}, 500


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### import api namespaces / add namespaces to api wrapper
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

from .endpoint_dso import 		ns as ns_dso_list
api.add_namespace(ns_dso_list)

from .endpoint_dso_edit import 	ns as ns_dso_edit
api.add_namespace(ns_dso_edit)

