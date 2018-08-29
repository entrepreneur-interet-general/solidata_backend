# -*- encoding: utf-8 -*-

"""
api_datamodel_recipes/__init__.py
"""

from solidata_api.api import *

# from log_config import log, pformat
log.debug("\n>>> api_datamodel_recipes ... creating api blueprint for DATAMODEL RECIPES")


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### create blueprint and api wrapper
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

blueprint = Blueprint( 'api_recipes', __name__, template_folder=app.config["TEMPLATES_FOLDER"] )
# blueprint = Blueprint( 'api_dataset_inputs', __name__, template_folder='templates' )

### enable CORS on blueprint
CORS(blueprint)

### create API
api = Api( 	blueprint,
						title				= "Solidata API : DATAMODEL RECIPES",
						version				= "0.1",
						description			= "create, list, delete, edit... datamodel recipes",
						doc					= '/documentation',
						default				= 'create',
						authorizations		= auth_check,
						security			='apikey' # globally ask for pikey auth
)


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

from .endpoint_rec_create import 	ns as ns_rec_create
api.add_namespace(ns_rec_create)

# from .endpoint_rec import 			ns as ns_rec_list
# api.add_namespace(ns_rec_list)

# from .endpoint_rec_edit import 		ns as ns_rec_edit
# api.add_namespace(ns_rec_edit)
