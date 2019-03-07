# -*- encoding: utf-8 -*-

"""
api_dataset_inputs/__init__.py
- provides the API endpoints for consuming and producing
	REST requests and responses
"""

from solidata_api.api import *

# from log_config import log, pformat
log.debug("\n>>> api_dataset_inputs ... creating api blueprint for DATASET INPUTS")

document_type		= "dsi"

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### create blueprint and api wrapper
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

blueprint = Blueprint( 'api_dataset_inputs', __name__, template_folder=app.config["TEMPLATES_FOLDER"] )
# blueprint = Blueprint( 'api_dataset_inputs', __name__, template_folder='templates' )

### enable CORS on blueprint
# CORS(blueprint)

### create API
api = MyApi( 	blueprint,
						title	= "Solidata API : DATASET INPUTS",
						version	= app.config["APP_VERSION"],
						description	= app.config["CODE_LINK"] + " : create, list, delete, edit... dataset inputs",
						doc	= '/documentation',
						default	= 'create',
						authorizations= auth_check,
						# security			='apikey' # globally ask for apikey auth
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

from .endpoint_dsi_create import ns as ns_dsi_create
api.add_namespace(ns_dsi_create)

from .endpoint_dsi 				import ns as ns_dsi_list
api.add_namespace(ns_dsi_list)

from .endpoint_dsi_edit 	import ns as ns_dsi_edit
api.add_namespace(ns_dsi_edit)

from .endpoint_dsi_reload import 	ns as ns_dsi_reload
api.add_namespace(ns_dsi_reload)
