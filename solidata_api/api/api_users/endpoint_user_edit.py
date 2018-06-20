# -*- encoding: utf-8 -*-

"""
endpoint_user_edit.py  
- provides the API endpoints for consuming and producing
	REST requests and responses
"""

from log_config import log
log.debug(">>> api_users ... creating api endpoints for USER_EDITION")

from  datetime import datetime, timedelta
from	bson import json_util
from	bson.objectid import ObjectId
from	bson.json_util import dumps

from flask import current_app, request
from flask_restplus import Namespace, Resource, fields, marshal, reqparse
from 	werkzeug.security 	import 	generate_password_hash, check_password_hash

### import JWT utils
import jwt
from flask_jwt_extended import (
		jwt_required, jwt_optional, create_access_token, create_refresh_token,
		get_jwt_identity, get_jwt_claims
)

### import mongo utils
from solidata_api.application import mongo
from solidata_api._core.queries_db import * # mongo_users, etc...

### import auth utils
from solidata_api._auth import token_required

# ### import data serializers
# from solidata_api._serializers.schema_users import *  

### create namespace
ns = Namespace('user_edit', description='User edition')

### import parsers
from solidata_api._parsers.parser_pagination import pagination_arguments

### import models 
from .models import * # model_user, model_new_user
model_new_user  = NewUser(ns).model
model_user_out  = User_out(ns).model
model_user_in   = User_in(ns).model



### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES 
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###


@ns.doc(security='apikey')
@ns.route("/<id>")
@ns.response(404, 'user not found')
@ns.param('id', 'The user identifier')
class User(Resource) :
		
	"""
	Show a single user item and lets you delete them
	"""

	@ns.doc('get_user_infos')
	@token_required
	@ns.marshal_with(model_user_out)
	def get(self, id):
		"""
		Fetch a given user
		"""
		return "fetching user {} ".format(id) # DAO.get(id)

	@ns.doc('delete_user_infos')
	@token_required
	@ns.response(204, 'Todo deleted')
	def delete(self, id):
		"""
		Delete a user given its identifier
		"""
		# DAO.delete(id)
		return '', 204

	@ns.doc('update_user_infos')
	@ns.expect(model_user_in)
	@token_required
	@ns.marshal_with(model_user_in)
	def put(self, id):
		"""
		Update an user given its identifier
		"""

		return "updating user " # DAO.update(id, api.payload)