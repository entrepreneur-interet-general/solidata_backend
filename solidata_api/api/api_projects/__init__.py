# -*- encoding: utf-8 -*-

"""
api_projects/__init__.py
- provides the API endpoints for consuming and producing
	REST requests and responses
"""

from solidata_api.api import *

# from log_config import log, pformat
log.debug("\n>>> api_projects ... creating api blueprint for PROJECTS")

# from flask import Blueprint, current_app as app
# from flask_restplus import Api

### import db collections dict
# from solidata_api.application import mongo
# from solidata_api._auth.authorizations import authorizations as auth_check
# from solidata_api._auth.auth_decorators import token_required


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### create blueprint and api wrapper
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

blueprint = Blueprint( 'api_projects', __name__, template_folder='templates' )
api = Api( 	blueprint,
						title						= "Solidata API : PROJECTS",
						version					= "0.1",
						description			= "create, list, delete, edit... projects",
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

from .endpoint_projects import 		ns as ns_proj_list
api.add_namespace(ns_proj_list)

from .endpoint_proj_create import 		ns as ns_proj_create
api.add_namespace(ns_proj_create)

from .endpoint_proj_edit import 		ns as ns_proj_edit
api.add_namespace(ns_proj_edit)
