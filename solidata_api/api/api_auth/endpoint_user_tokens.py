# -*- encoding: utf-8 -*-

"""
endpoint_user_tokens.py  
- provides the API endpoints for consuming and producing
	REST requests and responses
"""

from log_config import log, pformat
log.debug(">>> api_auth ... creating api endpoints for USER_TOKENS")


# from  datetime import datetime, timedelta
# from	bson import json_util
# from	bson.objectid import ObjectId
# from	bson.json_util import dumps

from flask import current_app, request
from flask_restplus import Namespace, Resource, marshal #, fields, reqparse
# from 	werkzeug.security 	import 	generate_password_hash, check_password_hash

### import JWT utils
# import jwt
from flask_jwt_extended import (
		jwt_refresh_token_required, jwt_optional,
		create_access_token, create_refresh_token,
		get_jwt_identity, get_raw_jwt, decode_token
)

### import mongo utils
# from solidata_api.application import mongo
from solidata_api._core.queries_db import mongo_users

# ### import data serializers
# from solidata_api._serializers.schema_users import *  

### create namespace
ns = Namespace('tokens', description='User : tokens freshening related endpoints')

### import parsers
# from solidata_api._parsers.parser_pagination import pagination_arguments

### import models 
from solidata_api._models.models_user import * #User_infos, AnonymousUser
model_user_access				= User_infos(ns).model_access
model_old_refresh_token = ExpiredRefreshToken(ns).model

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 

# cf : http://flask-jwt-extended.readthedocs.io/en/latest/refresh_tokens.html


@ns.doc(security='apikey')
@ns.route('/')
@ns.route('/access_token')
class RefreshAccessToken(Resource) :

	# The jwt_refresh_token_required decorator insures a valid refresh
	# token is present in the request before calling this endpoint. We
	# can use the get_jwt_identity() function to get the identity of
	# the refresh token, and use the create_access_token() function again
	# to make a new access token for this identity.
	@jwt_refresh_token_required
	def get(self) : 
		"""
		Refresh the access_token given a valid refresh_token

		>
			--- needs   : a valid refresh_token in the header 
			>>> returns : msg, a new_access_token
		"""

		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )
		# log.debug ("payload : \n{}".format(pformat(ns.payload)))

		### retrieve current user identity from refresh token
		user_email = get_jwt_identity()
		log.debug("user_email : \n %s", user_email)

		### retrieve user from db to get all infos
		user = mongo_users.find_one( {"infos.email" : user_email } )
		log.debug("user : \n %s", pformat(user)) 

		if user or user_email == "anonymous":
			
			if user : 
				user_light 	= marshal( user , model_user_access)
				user_light["_id"] = str(user["_id"])

			elif user_email == "anonymous" :
				anon_user_class 						= AnonymousUser()
				user_light 									= anon_user_class.__dict__

			### create new access token
			new_access_token = create_access_token(identity=user_light, fresh=False)
			log.debug("new_access_token : \n %s ", new_access_token)

			### store tokens
			token = {
					'access_token': new_access_token
			}

			return {	
								"msg" 		: "new access token for user : {} ".format(user_email) , 
								"tokens"	:  token
						}, 302 ### indicates to redirect to other URL
	
		else : 
			return {
								"msg" 		: "user '{}' not found ".format(user_email) , 
			}, 401



@ns.doc(security='apikey')
@ns.route("/fresh_access_token")
class FreshAccessToken(Resource):
	
	@ns.doc('user_fresh_token')
	@jwt_refresh_token_required
	def get(self):
		"""
		Create a fresh access_token 

		>
			--- needs   : valid refresh_token in the header
			>>> returns : msg, fresh access_token, is_user_confirmed
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
								"msg" 							: "fresh access_token created for user '{}' ".format(user_identity) , 
								"is_user_confirmed" : user["auth"]["conf_usr"],
								"tokens"						: tokens
						}, 200
		
		else : 

			return {
								"msg" 		: "incorrect user" , 
						}, 401


# @ns.route('/new_refresh_token' )
# @ns.route('/new_refresh_token/', defaults={ 'old_refresh_token':'your_old_refresh_token' } )
@ns.route('/new_refresh_token/<string:old_refresh_token>' )
@ns.param('old_refresh_token', 'The expired refresh_token')
class NewRefreshToken(Resource) :

	# def post(self, old_refresh_token="your_old_refresh_token") : 
	def post(self, old_refresh_token) : 
		"""
		Refresh the refresh_token given when POST an old refresh_token (in URL or in header) ...
		From old_refresh_token check if : 
		- user exists in DB
		- if user's email is confirmed and not anonymous
		- if user is blacklisted

		>
			--- needs   : an old refresh_token in the header or in the URL 
			>>> returns : msg, a new_refresh_token
		"""

		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )
		log.debug ("payload : \n{}".format(pformat(ns.payload)))

		### retrieve jwt
		# raw_jwt 				= ns.payload["old_refresh_token"]
		raw_jwt 				= old_refresh_token
		log.debug("raw_jwt : \n %s", pformat(raw_jwt))

		### decode jwt
		decoded_token 	= decode_token(raw_jwt)
		log.debug("decoded_token : \n %s", pformat(decoded_token))

		### check jwt and user's identity from old refresh_token
		jwt_type			= decoded_token["type"]
		jwt_identity 	= decoded_token["jti"]
		log.debug('jwt_type : {} / jwt_identity : {}'.format(jwt_type, jwt_identity) )
		user_identity = decoded_token["identity"]
		log.debug('user_identity from old refresh_token : \n%s', user_identity )


		if user_identity != "anonymous" and jwt_type == "refresh" : 

			### find user  in db
			user = mongo_users.find_one( {"infos.email" : user_identity } ) 
			log.debug("user : \n %s", pformat(user)) 

			if user :

				### check if there is something wrong : user's email not confirmed | user blacklisted
				if user["auth"]["conf_usr"] and user["auth"]["blklst_usr"] == False : 

					### marshal user's info 
					user_light 				= marshal( user , model_user_access)
					user_light["_id"] = str(user["_id"])

					# create a new refresh_token 
					new_refresh_token 				= create_refresh_token(identity=user_light)

					# and save it into user's data in DB
					user["auth"]["refr_tok"] 	= new_refresh_token
					mongo_users.save(user)

					# create user's new_access_token 
					new_access_token 	= create_access_token(identity=user_light)

					tokens = {
						"access_token" 	: new_access_token,
						"refresh_token" : new_refresh_token
					}
					
					### return new tokens 
					return {	
										"msg" 		: "new refresh_token created for user '{}' ".format(user_identity) , 
										"tokens"	: tokens
								}, 200

				### user's email not confirmed or blacklisted
				else : 
					return {
										"msg" : "you need to confirm your email '{}' first before...".format(user_identity)
								}, 401
			
			### user not in DB
			else : 
				return {
									"msg" : "no such user in DB"
							}, 401

		### user is anonymous | wrong jwt
		else : 
			return {
								"msg" : "anonyous users can't renew their refresh_token OR wrong jwt type..."
						}, 401
