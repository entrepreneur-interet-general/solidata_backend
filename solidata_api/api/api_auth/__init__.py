# -*- encoding: utf-8 -*-

"""
api_auth/__init__.py
- provides the API endpoints for consuming and producing
	REST requests and responses
"""

from solidata_api.api import *

# from log_config import log, pformat
log.debug("\n>>> api_auth ... creating api blueprint for AUTH")



### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### create blueprint and api wrapper
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

blueprint = Blueprint( 'api_auth', __name__, template_folder=app.config["TEMPLATES_FOLDER"] )
# blueprint = Blueprint( 'api_auth', __name__, template_folder='templates' )

### enable CORS on blueprint
# CORS(blueprint)

### create API
api = Api( 	blueprint,
						title				= "Solidata API : AUTH SERVER",
						version				= "0.1",
						description			= "auth server / manages tokens",
						doc					= '/documentation',
						default				= 'login',
						authorizations		= auth_check,
						# security='apikey' # globally ask for apikey auth
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


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### import api namespaces / add namespaces to api wrapper
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###


from .endpoint_user_login import 	ns as ns_user_login
api.add_namespace(ns_user_login)

from .endpoint_user_tokens import 	ns as ns_user_refresh
api.add_namespace(ns_user_refresh)

from .endpoint_user_password import ns as ns_user_password
api.add_namespace(ns_user_password)
