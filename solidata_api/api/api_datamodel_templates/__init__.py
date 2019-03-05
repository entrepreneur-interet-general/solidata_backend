# -*- encoding: utf-8 -*-

"""
api_datamodel_templates/__init__.py
"""

from solidata_api.api import *

# from log_config import log, pformat
log.debug("\n>>> api_dataset_inputs ... creating api blueprint for DATAMODEL TEMPLATES")

document_type		= "dmt"

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### create blueprint and api wrapper
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

blueprint = Blueprint( 'api_datamodel_templates', __name__, template_folder=app.config["TEMPLATES_FOLDER"] )
# blueprint = Blueprint( 'api_dataset_inputs', __name__, template_folder='templates' )

### enable CORS on blueprint
# CORS(blueprint)

### create API
api = Api( 	blueprint,
						title				= "Solidata API : DATAMODEL TEMPLATES",
						version			= "0.1",
						description	= app.config["CODE_LINK"] +  " : create, list, delete, edit... datamodel templates",
						doc					= '/documentation',
						default			= 'create',
						authorizations = auth_check,
						# security		='apikey' # globally ask for pikey auth
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

from .endpoint_dmt_create import 	ns as ns_dmt_create
api.add_namespace(ns_dmt_create)

from .endpoint_dmt import 			ns as ns_dmt_list
api.add_namespace(ns_dmt_list)

from .endpoint_dmt_edit import 		ns as ns_dmt_edit
api.add_namespace(ns_dmt_edit)
