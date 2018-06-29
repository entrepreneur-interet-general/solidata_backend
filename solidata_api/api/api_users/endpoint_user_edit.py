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
# from .models import * # model_user, model_new_user
from solidata_api._models.models_user import *  
model_new_user		= NewUser(ns).model
model_user_out		= User_infos(ns).model_complete
model_user_in			= User_infos(ns).model_in
model_user_update	= User_infos(ns).model_update
model_user_token	= User_infos(ns).model_for_token



### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES 
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###


@ns.doc(security='apikey')
@ns.route("/<string:user_oid>/")
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
	# @ns.marshal_with(model_user_out)
	def get(self, user_oid):
		"""
		Fetch a given user given its _id in DB
		"""

		### DEBUGGING
		print()
		log.debug( "ROUTE class : %s", self.__class__.__name__ )

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


	@ns.doc('delete_user')
	@current_user_required
	# @ns.response(204, 'Todo deleted')
	def delete(self, user_oid):
		"""
		Delete an user given its _id
		"""

		### DEBUGGING
		print()
		log.debug( "ROUTE class : %s", self.__class__.__name__ )

		### check if user requiring info is current user or admin
		log.debug("user_oid : %s", user_oid)

		### delete user from db
		mongo_users.delete_one({"_id" : ObjectId(user_oid)})


		### TO DO - delete user info from all projects and other datasets 
		### TO DO - OR choice to keep at least email / or / delete all data


		return {
							"msg"		  : "user deleted : oid {} ".format(user_oid),
					}, 204


@ns.doc(security='apikey')
@ns.route("/<string:user_oid>/<field_to_update>")
# @ns.route("/<string:user_oid>/<field_to_update>/<string:data_oid>")
@ns.response(404, 'user not found')
@ns.param('user_oid', 'The user unique identifier')
class User_update(Resource) :
  	
	### TO DO 
	@ns.doc('update_user_infos')
	@current_user_required
	# @ns.expect(model_user_update)
	def put(self, user_oid, field_to_update=None) : #, data_oid=None):
		"""
		TO DO - Update an user given its _id / for client use
		only takes the following client infos : 
		> user_basics : 
			- name
			- surmame 
			- email
		> user_preferences_in : 
			- lang
		> user_professional : 
			- struct_
			- profiles
		"""

		### DEBUGGING
		print()
		log.debug( "ROUTE class : %s", self.__class__.__name__ )
		log.debug("user_oid : %s", user_oid)

		### retrieve user's data from payload
		user_updated_data = ns.payload
		log.debug("user_updated_data : \n %s" , pformat(user_updated_data) ) 

		### retrieve personnal infos from user in db
		user = mongo_users.find_one({"_id" : ObjectId(user_oid)})
		log.debug("user : \n %s", pformat(user))

		### marshall user in order to make tokens
		user_light 					= marshal( user, model_user_token )
		user_light["_id"] 	= str(user["_id"])

		### remake access and refresh token
		access_token 	= create_access_token(  identity = user_light )
		# refresh_token = user["auth"]["refr_tok"] # create_refresh_token( identity = user_light )
		tokens = {
				'access_token'	: access_token,
				# 'refresh_token'	: refresh_token
		}

		### update user info from data in pyaload




		return "updating user {} ".format(user_oid) # DAO.update(id, api.payload)