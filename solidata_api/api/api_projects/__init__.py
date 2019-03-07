# -*- encoding: utf-8 -*-

"""
api_projects/__init__.py
- provides the API endpoints for consuming and producing
	REST requests and responses
"""

from solidata_api.api import *

# from log_config import log, pformat
log.debug("\n>>> api_projects ... creating api blueprint for PROJECTS")

document_type		= "prj"

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### create blueprint and api wrapper
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

blueprint = Blueprint( 'api_projects', __name__, template_folder=app.config["TEMPLATES_FOLDER"] )
# blueprint = Blueprint( 'api_projects', __name__, template_folder='templates' )

### enable CORS on blueprint
# CORS(blueprint)

### create API
api = MyApi( 	blueprint,
						title	= "Solidata API : PROJECTS",
						version	= app.config["APP_VERSION"],
						description	= app.config["CODE_LINK"] + " : create, list, delete, edit... projects",
						doc	= '/documentation',
						default	= 'create',
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

from .endpoint_prj_create import 	ns as ns_prj_create
api.add_namespace(ns_prj_create)

from .endpoint_prj import 			ns as ns_prj_list
api.add_namespace(ns_prj_list)

from .endpoint_prj_edit import 		ns as ns_prj_edit
api.add_namespace(ns_prj_edit)

from .endpoint_prj_mapping import 	ns as ns_prj_mapping
api.add_namespace(ns_prj_mapping)

from .endpoint_prj_solidify import 	ns as ns_prj_solidify
api.add_namespace(ns_prj_solidify)