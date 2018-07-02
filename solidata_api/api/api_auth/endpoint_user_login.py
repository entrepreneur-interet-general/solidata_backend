# -*- encoding: utf-8 -*-

"""
endpoint_user_login.py  
- provides the API endpoints for consuming and producing
	REST requests and responses
"""

from log_config import log, pformat
log.debug(">>> api_users ... creating api endpoints for USER_LOGIN")

from  datetime import datetime, timedelta
from	bson import json_util
from	bson.objectid import ObjectId
from	bson.json_util import dumps

from flask import current_app as app, url_for #, request
from flask_restplus import Namespace, Resource, fields, marshal, reqparse
from 	werkzeug.security 	import 	generate_password_hash, check_password_hash

### DEBUGGING CONFIRMAITON EMAIL 
# from solidata_api._auth import generate_confirmation_token

### import JWT utils
import jwt
from flask_jwt_extended import (
		jwt_required, jwt_optional, jwt_refresh_token_required, 
		create_access_token, create_refresh_token,
		get_jwt_identity, get_jwt_claims
)
from solidata_api._auth import admin_required, current_user_required, anonymous_required # token_required

### import mongo utils
# from solidata_api.application import mongo
from solidata_api._core.queries_db import mongo_users

# ### import data serializers
# from solidata_api._serializers.schema_users import *  

### create namespace
ns = Namespace('login', description='User : login related endpoints')

### import parsers
# from solidata_api._parsers.parser_pagination import pagination_arguments

### import models 
# from .models import * # model_user, model_new_user
from solidata_api._models.models_user import LoginUser, User_infos, AnonymousUser
model_login_user  	= LoginUser(ns).model
model_user_access		= User_infos(ns).model_access #model_complete


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

# cf : response codes : https://restfulapi.net/http-status-codes/ 


@ns.route('/anonymous/')
class AnonymousLogin(Resource):

	@ns.doc('user_anonymous')
	def get(self):
		"""
		Login as anonymous user
			--- needs		: nothing particular
			>>> returns	: anonymous access_token + anonymous refresh_token with a short expiration date
		"""

		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )

		### create a fake user 
		anon_user_class = AnonymousUser()
		anonymous_user 	= anon_user_class.__dict__

		### create corresponding access token
		anonymous_access_token		= create_access_token(identity=anonymous_user) #, expires_delta=expires)

		### create corresponding refresh token
		expires 									= app.config["JWT_ANONYMOUS_REFRESH_TOKEN_EXPIRES"]
		anonymous_refresh_token		= create_refresh_token(identity=anonymous_user, expires_delta=expires)

		log.debug("anonymous_access_token 	: \n %s", anonymous_access_token )
		log.debug("anonymous_refresh_token 	: \n %s", anonymous_refresh_token )

		### store tokens in dict
		tokens = {
				'access_token' 	: anonymous_access_token,
				'refresh_token' : anonymous_refresh_token,
		}

		return {	
							"msg" 		: "anonymous user - an anonymous access_token has been created + a valid refresh_token for {} hours".format(expires) , 
							"tokens"	:  tokens
					}, 200



@ns.route('/')
class Login(Resource):

	@ns.doc('user_login')
	@ns.doc(security='apikey')
	@ns.expect(model_login_user)
	# @jwt_required
	@anonymous_required
	def post(self):
		"""
		Log in an user given an email and a password 
		- checks if email exists in db 
		- check if salted pwd is equals to user's
			--- needs : an anonymous access_token (please use '.../login/anonymous/' first)
			>>> returns : msg, access_token, refresh_tokens
		"""

		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )
		log.debug ("payload : \n{}".format(pformat(ns.payload)))

		# token 				= None 
		# error_message = None

		### retrieve infos from form
		payload_email = ns.payload["email"]
		payload_pwd   = ns.payload["pwd"]
		log.debug("email  : %s", payload_email )
		log.debug("pwd    : %s", payload_pwd )

		### retrieve user from db
		user = mongo_users.find_one( {"infos.email" : payload_email } ) #, {"_id": 0 })
		log.debug("user : \n %s", pformat(user)) 

		if user is None : 

			error_message = "no such user in db"
			return {	
								"msg" : "incorrect login / {}".format(error_message) 
							}, 401

		if user : 
			
			### check password
			pwd = user["auth"]["pwd"]
			if check_password_hash(pwd, payload_pwd) :

				### marshal user's info 
				user_light 				= marshal( user , model_user_access)
				user_light["_id"] = str(user["_id"])
				log.debug("user_light : \n %s", pformat(user_light) )

				### Use create_access_token() to create user's new access token 
				new_access_token 	= create_access_token(identity=user_light, fresh=False)
				
				# only update refresh token if user is confirmed
				# if user["auth"]["conf_usr"] == False : 
				# 	refresh_token 		= user["auth"]["refr_tok"]  
				# else : 
				# 	refresh_token			= create_refresh_token(identity=user_light)

				### retrieve existing refresh_token from db
				refresh_token 		= user["auth"]["refr_tok"]  

				tokens = {
						'access_token'	: new_access_token,
						'refresh_token' : refresh_token,
				}
				print()
				log.debug("user_light['_id'] : %s", user_light["_id"] )
				log.debug("new_access_token  : %s", new_access_token )
				log.debug("refresh_token 		 : %s", refresh_token )
				print()

				### save new refresh token in user db
				user["auth"]["refr_tok"] 	= refresh_token
				mongo_users.save(user)
				
				### update user log in db
				### TO DO 

				return {	
									"msg" 							: "user '{}' is logged".format(payload_email),
									"is_user_confirmed" : user["auth"]["conf_usr"],
									"tokens"						: tokens
							}, 200

			else : 

				error_message = "wrong password"
				return { 
									"msg" : "incorrect login / {}".format(error_message) 
							}, 401


@ns.route("/fresh")
class FreshLogin(Resource):
	
	@ns.doc('user_fresh_login')
	@ns.doc(security='apikey')
	# @current_user_required
	@jwt_refresh_token_required
	def get(self):
		"""
		Create a fresh access_token 
			--- needs 	: valid refresh_token in the header
			>>> returns : fresh access_token
		"""

		### DEBUGGING 
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )
		
		### check identity
		user_identity = get_jwt_identity()
		log.debug('useremail from jwt : \n%s', user_identity )

		### find user
		user = mongo_users.find_one( {"infos.email" : user_identity } ) 
		log.debug("user : \n %s", pformat(user)) 

		if user :

			### marshal user's info 
			user_light 				= marshal( user , model_user_access)
			user_light["_id"] = str(user["_id"])

			# Use create_access_token() to create user's fresh access token 
			fresh_access_token 	= create_access_token(identity=user_light, fresh=True)

			tokens = {
				"access_token" : fresh_access_token,
			}

			return {	
								"msg" 							: "fresh access_token created for user '{}' ".format(payload_email) , 
								"is_user_confirmed" : user["auth"]["conf_usr"],
								"tokens"						: tokens
						}, 200
		
		else : 

			return {
								"msg" 		: "incorrect user" , 
						}, 401

