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
from solidata_api._auth import admin_required, current_user_required # token_required

### import mongo utils
from solidata_api.application import mongo
from solidata_api._core.queries_db import * # mongo_users, etc...


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
@ns.route("/<string:user_oid>")
@ns.response(404, 'user not found')
@ns.param('user_oid', 'The user unique identifier')
class User(Resource) :
		
	"""
	User edition
	GET - Shows a single user item infos 
	PUT - Updates user infos
	DELETE - Lets you delete them
	"""

	@current_user_required
	@ns.doc('get_user_infos')
	# @jwt_required
	# @ns.marshal_with(model_user_out)
	def get(self, user_oid):
		"""
		Fetch a given user
		"""

		### check if user requiring info is current user or admin
		log.debug("user_oid : %s", user_oid)

		### retrieve personnal infos from user in db
		user = mongo_users.find_one({"_id" : ObjectId(user_oid)})
		log.debug("user : %s", pformat(user))

		### possible no user found if access as admin and random _id search
		user_out = marshal( user, model_user_out )

		### marchall info

		
		return {
							"msg"		  : "infos for user with oid {}".format(user_oid),
							"data"		: user_out
					}, 200
		# return "fetching user {} ".format(user_oid) # DAO.get(id)


	@ns.doc('delete_user_infos')
	@jwt_required
	@ns.response(204, 'Todo deleted')
	def delete(self, user_oid):
		"""
		Delete a user given its identifier
		"""



		# DAO.delete(id)
		return '', 204

	@ns.doc('update_user_infos')
	@jwt_required
	@ns.expect(model_user_out)
	# @token_required
	# @ns.marshal_with(model_user_in)
	def put(self, user_oid):
		"""
		Update an user given its identifier
		"""

		return "updating user " # DAO.update(id, api.payload)