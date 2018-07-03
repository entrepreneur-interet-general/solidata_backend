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
		jwt_required, jwt_optional, fresh_jwt_required,
		create_access_token, create_refresh_token,
		get_jwt_identity, get_jwt_claims
)
from solidata_api._auth import admin_required, current_user_required, anonymous_required # token_required

### import mongo utils
from solidata_api.application import mongo
from solidata_api._core.queries_db import * # mongo_users, etc...


# ### import data serializers
# from solidata_api._serializers.schema_users import *  

### create namespace
ns = Namespace('user_edit', description="Users : user's info edition related endpoints")

### import parsers
from solidata_api._parsers.parser_pagination import pagination_arguments

### import models 
from solidata_api._models.models_user import *  
model_new_user				= NewUser(ns).model
model_user_out				= User_infos(ns).model_complete_out
model_user_out_admin	= User_infos(ns).mod_complete_in
# model_user_update	= User_infos(ns).model_update
# model_user_access	= User_infos(ns).model_access



### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES 
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 


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
	
	@ns.doc('get_user_infos')
	# @ns.marshal_with(model_user_out)
	@current_user_required
	def get(self, user_oid):
		"""
		Fetch an user given its _id (<user_oid>) in DB

		>
			--- needs 	: a valid access_token (as admin or current user) in the header, an oid of the user
			>>> returns : msg, user data marshalled
		"""

		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )

		### check if user requiring info is current user or admin
		log.debug("user_oid : %s", user_oid)

		### check if client is an admin or if is the current user
		claims 	= get_jwt_claims() 
		log.debug("claims : \n %s", pformat(claims) )
		is_client_admin = claims["auth"]["role"]

		### retrieve personnal infos from user in db
		user = mongo_users.find_one({"_id" : ObjectId(user_oid)})
		log.debug("user : %s", pformat(user))

		### possible no user found if access as admin and random _id search
		if user : 
			
			if is_client_admin == "admin" : 
				### marshall infos for admin
				user_out = marshal( user, model_user_out_admin )

			else :
				### marchall info for user
				user_out = marshal( user, model_user_out )


			return {
								"msg"		  : "infos for user with oid {}".format(user_oid),
								"data"		: user_out
						}, 200

		else : 
			return {
					"msg"		  : "no user found with oid {}".format(user_oid),
			}, 401



	@ns.doc('delete_user')
	# @ns.response(204, 'Todo deleted')
	@current_user_required
	def delete(self, user_oid):
		"""
		Delete an user given its _id / only doable by admin or current_user
		
		> 
			--- needs   : a valid access_token (as admin or current user) in the header, an user_oid of the user in the request
			>>> returns : msg, response 204 as user is deleted
		
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
@ns.response(404, 'user not found')
@ns.param('user_oid', 'The user unique identifier in DB')
class User_update(Resource) :
		
	### TO DO 
	@ns.doc('update_user_infos')
	# @ns.expect(model_user_update)
	@current_user_required
	def put(self, user_oid, field_to_update=None) : #, data_oid=None):
		"""
		TO DO - Update an user given its _id / for client use
		only takes the following client infos : 

		--- 

		> user_basics : 
			- name
			- surmame 
			- email --> sends a confirmation email with refresh token valid 3 days
		
		> user_auth :
			- pwd --> sends a confirmation email with refresh token valid 1 days

		> user_preferences_in : 
			- lang
		
		> user_professional : 
			- struct_
			- profiles
		
		>
			--- needs 	: a valid access_token (as admin or current user) in the header, an user_oid of the user + the field to update in the request
			>>> returns : msg, updated data copy

		"""

		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug("ROUTE class : %s", self.__class__.__name__ )
		log.debug("user_oid : %s", user_oid)

		### retrieve user's data from payload
		user_updated_data = ns.payload
		log.debug("user_updated_data : \n %s", pformat(user_updated_data) ) 

		### retrieve personnal infos from user in db
		user = mongo_users.find_one({"_id" : ObjectId(user_oid)})
		log.debug("user : \n %s", pformat(user))

		### marshall user in order to make tokens
		user_light 					= marshal( user, model_user_out )
		user_light["_id"] 	= str(user["_id"])



		### update user info from data in pyaload



		return { 
							"msg" 					: "updating user {} ".format(user_oid), # DAO.update(id, api.payload)
							"field_updated"	: field_to_update,
							"data_sent"			: user_updated_data
					}