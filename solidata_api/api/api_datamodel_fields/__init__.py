# -*- encoding: utf-8 -*-

"""
api_datamodel_fields/__init__.py
"""

from solidata_api.api import *

# from log_config import log, pformat
log.debug("\n>>> api_datamodel_fields ... creating api blueprint for DATAMODEL TEMPLATES")


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### create blueprint and api wrapper
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

blueprint = Blueprint( 'api_datamodel_fields', __name__, template_folder=app.config["TEMPLATES_FOLDER"] )
# blueprint = Blueprint( 'api_dataset_inputs', __name__, template_folder='templates' )
api = Api( 	blueprint,
						title						= "Solidata API : DATAMODEL FIELDS",
						version					= "0.1",
						description			= "create, list, delete, edit... datamodel fields",
						doc							= '/documentation',
						default					= 'create',
						authorizations	= auth_check,
						security				='apikey' # globally ask for pikey auth
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

from .endpoint_dmf import 		ns as ns_dmf_list
api.add_namespace(ns_dmf_list)

from .endpoint_dmf_create import 		ns as ns_dmf_create
api.add_namespace(ns_dmf_create)

from .endpoint_dmf_edit import 		ns as ns_dmf_edit
api.add_namespace(ns_dmf_edit)
