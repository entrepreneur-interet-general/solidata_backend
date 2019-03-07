# -*- encoding: utf-8 -*-

"""
api_users/__init__.py
"""

from solidata_api.api import *

# from log_config import log, pformat
log.debug("\n>>> api_users ... creating api blueprint for USERS")

document_type		= "usr"

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### create blueprint and api wrapper
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

blueprint = Blueprint( 'api_users', __name__, template_folder=app.config["TEMPLATES_FOLDER"] )
# blueprint = Blueprint( 'api_users', __name__, template_folder='templates' )

### enable CORS on blueprint
# CORS(blueprint)

### create API
api = Api(  	blueprint,
						title	= "Solidata API : USERS",
						version	= app.config["APP_VERSION"],
						description	= app.config["CODE_LINK"] +  " : create, list, delete, edit... users",
						doc	= '/documentation',
						default = 'register',
						authorizations = auth_check,
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


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### import api namespaces / add namespaces to api wrapper
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###


from .endpoint_usr import 			ns as ns_usr_list
api.add_namespace(ns_usr_list)

# from .endpoint_user_login import ns as ns_user_login
# api.add_namespace(ns_user_login)

from .endpoint_usr_register import 	ns as ns_usr_register
api.add_namespace(ns_usr_register)

from .endpoint_usr_edit import		ns as ns_usr_edit
api.add_namespace(ns_usr_edit)