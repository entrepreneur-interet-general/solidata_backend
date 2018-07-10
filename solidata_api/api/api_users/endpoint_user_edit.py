# -*- encoding: utf-8 -*-

"""
endpoint_user_edit.py  
- provides the API endpoints for consuming and producing
	REST requests and responses
"""

from log_config import log
log.debug(">>> api_users ... creating api endpoints for USER_EDITION")

from	copy import copy, deepcopy
from	datetime import datetime, timedelta
from	bson import json_util
from	bson.objectid import ObjectId
from	bson.json_util import dumps

from . import api

from flask import current_app, request
from flask_restplus import Namespace, Resource, fields, marshal, reqparse
from 	werkzeug.security 	import 	generate_password_hash, check_password_hash

### import mailing utils
from solidata_api._core.emailing import send_email

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
model_data						= UserData(ns).model


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
	GET    - Shows a single user item infos 
	PUT    - Updates user infos
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
				### marshall all infos for admin
				user_out = marshal( user, model_user_out_admin )

			else :
				### marchall authorized visible info for user
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
	@ns.doc(responses={204: 'success : user was deleted'})
	@ns.doc(responses={401: 'error client : wrong user oid'})
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

		try :  
			### delete user from db
			mongo_users.delete_one({"_id" : ObjectId(user_oid)})

			### TO DO - delete user info from all projects and other datasets 
			### TO DO - OR choice to keep at least email / or / delete all data

			return {
								"msg"		: "user deleted (oid) : {} ".format(user_oid),
						}, 204
		
		except : 

			return {
								"msg"		: "error trying to delete oid : {} ".format(user_oid),
						}, 401



@ns.doc(security='apikey')
@ns.route("/<string:user_oid>/<field_to_update>")
# @ns.response(404, 'user not found')
@ns.doc(responses={401: 'error client : incorrect values'})
@ns.doc(responses={404: 'error client : user not found'})
# @ns.expect(model_data)
@ns.param('user_oid', 'The user unique identifier in DB')
class User_update(Resource) :
		
	### TO DO 
	@ns.doc('update_user_infos')
	@ns.expect(model_data)
	@current_user_required
	def put(self, user_oid, field_to_update=None) : #, data_oid=None):
		"""
		TO DO - Update an user given its _id / for client use
		only update fields one by one
		only takes the following client infos : 
		- in URL     : oid, field_to_update
		- in payload : the new value to put into the field

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

		### check if client is an admin or if is the current user
		claims 	= get_jwt_claims() 
		log.debug("claims : \n %s", pformat(claims) )
		is_client_admin = claims["auth"]["role"]


		### retrieve user's data from payload
		user_updated_data = copy(ns.payload["data"])
		log.debug("user_updated_data : \n %s", pformat(user_updated_data) ) 

		### retrieve personnal infos from user in db
		user = mongo_users.find_one({"_id" : ObjectId(user_oid)})
		log.debug("user : \n %s", pformat(user))


		if user : 

			### update user info from data in pyaload
			if field_to_update in user_fields_admin_can_update_list : 
				
				log.debug("field_to_update in admin authorized fields : %s", field_to_update )

				### stop from updating not authorized field if client is not admin
				if is_client_admin == False and field_to_update not in user_fields_client_can_update_list : 
					return {
							"msg"		  : "you are not authorized to update the field '{}'".format(field_to_update),
					}, 401


				else : 

					field_root 			= user_fields_dict[field_to_update]["field"]
					original_data		= user[field_root][field_to_update]
					if user_updated_data != original_data : 

						### marshall user in order to make tokens
						user_light 					= marshal( user, model_user_out )
						user_light["_id"] 	= str(user["_id"])

						### special function for user's email update
						if field_to_update == "email" :
								
							### add confirm_email claim
							user_light["confirm_email"]	= True
							expires 										= app.config["JWT_CONFIRM_EMAIL_REFRESH_TOKEN_EXPIRES"] # timedelta(days=7)
							access_token_confirm_email 	= create_access_token(identity=user_light, expires_delta=expires)

							### send a confirmation email if not RUN_MODE not 'dev'
							if app.config["RUN_MODE"] in ["prod", "dev_email"] : 
								
								# create url for confirmation to send in the mail
								confirm_url = app.config["DOMAIN_NAME"] + api.url_for(Confirm_email, token=access_token_confirm_email, external=True)
								log.info("confirm_url : \n %s", confirm_url)

								# generate html body of the email
								html = render_template('emails/confirm_email.html', confirm_url=confirm_url)
								
								# send the mail
								send_email( "Confirm your email", payload_email, template=html )
						
							### flag user's email as not confirmed
							user["auth"]["conf_usr"] = False


						### special function for user's pwd update 
						### --> only admin can access and create new password for users...
						if field_to_update == "pwd" :
								### create new hashpassword
								user_updated_data = generate_password_hash(user_updated_data, method='sha256')
								log.debug("hashpass : %s", hashpass)


						### update data in DB
						user[ field_root ][field_to_update] = user_updated_data
						mongo_users.save(user)


						return { 
											"msg" 					: "updating user {} ".format(user_oid), # DAO.update(id, api.payload)
											"field_updated"	: field_to_update,
											# "data_sent"			: user_updated_data
									}, 200


					else : {
									"msg"		  : "no difference between previous and sent data for field '{}'".format(field_to_update),
							}, 201
	
			else : 
				return {
						"msg"		  : "impossible to update the field '{}'".format(field_to_update),
				}, 401


		else : 
			return {
					"msg"		  : "user oid '{}' not found".format(user_oid),
			}, 401





