# -*- encoding: utf-8 -*-

"""
api_tags/__init__.py
"""

from solidata_api.api import *

# from log_config import log, pformat
log.debug("\n>>> api_tags ... creating api blueprint for DATAMODEL TAGS")


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### create blueprint and api wrapper
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

blueprint = Blueprint( 'api_tags', __name__, template_folder=app.config["TEMPLATES_FOLDER"] )
# blueprint = Blueprint( 'api_dataset_inputs', __name__, template_folder='templates' )

### enable CORS on blueprint
# CORS(blueprint)

### create API
api = Api( 	blueprint,
						title				= "Solidata API : DATAMODEL TAGS",
						version				= "0.1",
						description			= "create, list, delete, edit... datamodel tags",
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

from .endpoint_tag_create import 	ns as ns_tag_create
api.add_namespace(ns_tag_create)

from .endpoint_tag import 			ns as ns_tag_list
api.add_namespace(ns_tag_list)

# from .endpoint_tag_edit import 		ns as ns_tag_edit
# api.add_namespace(ns_tag_edit)
