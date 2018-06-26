# -*- encoding: utf-8 -*-

"""
endpoint_refresh_token.py  
- provides the API endpoints for consuming and producing
	REST requests and responses
"""

from log_config import log, pformat
log.debug(">>> api_users ... creating api endpoints for USER_REFRESH_TOKEN")


# from  datetime import datetime, timedelta
# from	bson import json_util
# from	bson.objectid import ObjectId
# from	bson.json_util import dumps

from flask import current_app, request
from flask_restplus import Namespace, Resource #, fields, marshal, reqparse
# from 	werkzeug.security 	import 	generate_password_hash, check_password_hash

### import JWT utils
# import jwt
from flask_jwt_extended import (
		jwt_refresh_token_required, create_access_token,
		get_jwt_identity
)

### import mongo utils
# from solidata_api.application import mongo
from solidata_api._core.queries_db import mongo_users

### import auth utils
# from solidata_api._auth import token_required

# ### import data serializers
# from solidata_api._serializers.schema_users import *  

### create namespace
ns = Namespace('refresh', description='User refresh token ')

### import parsers
# from solidata_api._parsers.parser_pagination import pagination_arguments

### import models 
from .models import * # model_user, model_new_user
model_user					= User_out(ns).model


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

# cf : http://flask-jwt-extended.readthedocs.io/en/latest/refresh_tokens.html

# The jwt_refresh_token_required decorator insures a valid refresh
# token is present in the request before calling this endpoint. We
# can use the get_jwt_identity() function to get the identity of
# the refresh token, and use the create_access_token() function again
# to make a new access token for this identity.
@ns.route('/')
class Refresh(Resource) :

	@ns.doc(security='apikey')
	@jwt_refresh_token_required
	def post(self) : 
		"""
		refresh the access token
		"""

		### DEBUGGING
		print()		
		log.debug( self.__class__.__name__ )
		log.debug ("payload : \n{}".format(pformat(ns.payload)))

		current_user = get_jwt_identity()
		log.debug("current_user : \n %s", current_user)

		### retrieve user from db to get all infos
		user = mongo_users.find_one( {"infos.email" : current_user }, {"_id": 0 })
		log.debug("user : \n %s", pformat(user)) 

		user_light 	= marshal( user , model_user)

		new_access_token = {
				'access_token': create_access_token(identity=user_light, fresh=False)
		}
		
		return new_access_token, 200