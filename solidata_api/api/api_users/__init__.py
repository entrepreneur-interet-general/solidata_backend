# -*- encoding: utf-8 -*-

"""
api_users/__init__.py
- provides the API endpoints for consuming and producing
	REST requests and responses
"""

from log_config import log, pformat
log.debug(">>> api_users ... creating api blueprint for USERS")

from flask import Blueprint
from flask_restplus import Api

### import db collections dict
from solidata_api.application import mongo


### create blueprint and api wrapper
blueprint = Blueprint( 'api_users', __name__ )
api = Api( 	blueprint,
						title="SOLIDATA - USERS API",
						version="0.1",
						description="create, list, delete, edit... users",
						doc='/documentation',
						default='users'
)


### import api namespaces / add namespaces to api wrapper
from .endpoint_users import 		ns as ns_users_list
api.add_namespace(ns_users_list)

from .endpoint_user_edit import ns as ns_user_edit
api.add_namespace(ns_user_edit)