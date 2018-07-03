# -*- encoding: utf-8 -*-

"""
api_users/__init__.py
- provides the API endpoints for consuming and producing
	REST requests and responses
"""

from log_config import log, pformat
log.debug("\n>>> api_users ... creating api blueprint for USERS")

from flask import Blueprint, current_app as app
from flask_restplus import Api

### import db collections dict
# from solidata_api.application import mongo
from solidata_api._auth.authorizations import authorizations as auth_check
# from solidata_api._auth.auth_decorators import token_required


### create blueprint and api wrapper
blueprint = Blueprint( 'api_users', __name__, template_folder='templates' )
api = Api( 	blueprint,
						title						= "Solidata API : USERS",
						version					= "0.2",
						description			= "create, list, delete, edit... users",
						doc							= '/documentation',
						default					= 'register',
						authorizations	= auth_check,
						# security='apikey' # globally ask for pikey auth
)


### errors handlers

@api.errorhandler
def default_error_handler(e):
		message = 'An unhandled exception occurred.'
		log.exception(message)

		if not app.config["FLASK_DEBUG"]:
				return {'message': message}, 500


# @api.errorhandler(NoResultFound)
# def database_not_found_error_handler(e):
#     log.warning(traceback.format_exc())
#     return {'message': 'A database result was required but none was found.'}, 404


### import api namespaces / add namespaces to api wrapper
from .endpoint_users import 		ns as ns_users_list
api.add_namespace(ns_users_list)

# from .endpoint_user_login import ns as ns_user_login
# api.add_namespace(ns_user_login)

from .endpoint_user_register import ns as ns_user_register
api.add_namespace(ns_user_register)

from .endpoint_user_edit import ns as ns_user_edit
api.add_namespace(ns_user_edit)