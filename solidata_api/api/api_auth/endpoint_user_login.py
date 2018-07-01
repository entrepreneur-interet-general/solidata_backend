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

from flask import current_app as app #, request
from flask_restplus import Namespace, Resource, fields, marshal, reqparse
from 	werkzeug.security 	import 	generate_password_hash, check_password_hash

### DEBUGGING CONFIRMAITON EMAIL 
# from solidata_api._auth import generate_confirmation_token

### import JWT utils
import jwt
from flask_jwt_extended import (
		jwt_required, jwt_optional, create_access_token, create_refresh_token,
		get_jwt_identity, get_jwt_claims
)

### import mongo utils
# from solidata_api.application import mongo
from solidata_api._core.queries_db import mongo_users

# ### import data serializers
# from solidata_api._serializers.schema_users import *  

### create namespace
ns = Namespace('login', description='User login ')

### import parsers
# from solidata_api._parsers.parser_pagination import pagination_arguments

### import models 
# from .models import * # model_user, model_new_user
from solidata_api._models.models_user import *  
model_login_user  	= LoginUser(ns).model
model_user_access		= User_infos(ns).model_access #model_complete


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

# cf : response codes : https://restfulapi.net/http-status-codes/ 

@ns.route('/')
class Login(Resource):

	@ns.doc('user_login')
	@ns.expect(model_login_user)
	def post(self):
		"""
		login user 
		checks if email exists in db 
		check if salted pwd is equals to user's
		return jwt : access token and refresh token
		"""

		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )
		log.debug ("payload : \n{}".format(pformat(ns.payload)))

		token = None 
		error_message = None

		### retrieve infos from form
		payload_email = ns.payload["email"]
		payload_pwd   = ns.payload["pwd"]
		log.debug("email 	: %s", payload_email )
		log.debug("pwd 		: %s", payload_pwd )

		### retrieve user from db
		user = mongo_users.find_one( {"infos.email" : payload_email } ) #, {"_id": 0 })
		log.debug("user : \n %s", pformat(user)) 

		if user is None : 

			error_message = "no such user in db"
			return {"msg" : "incorrect login / {}".format(error_message) }, 401

		if user : # and user["auth"]["conf_usr"] == True :
			
			### check password
			pwd = user["auth"]["pwd"]
			if check_password_hash(pwd, payload_pwd) :

				### create JWT tokens
				# token = jwt.encode({
				# 		'sub'	: user["infos"]["email"],
				# 		'iat'	:	datetime.utcnow(),
				# 		'exp'	: datetime.utcnow() + timedelta(minutes=30)},
				# 		current_app.config['JWT_SECRET_KEY'])

				### marshal user's info 
				user_light 				= marshal( user , model_user_access)
				user_light["_id"] = str(user["_id"])
				log.debug("user_light : \n %s", pformat(user_light) )

				# Use create_access_token() to create user's new access token for n minutes
				new_access_token 	= create_access_token(identity=user_light, fresh=True)
				
				# only update refresh token if user is confirmed
				if user["auth"]["conf_usr"] == False : 
					refresh_token 		= user["auth"]["refr_tok"]  
				else : 
					refresh_token			= create_refresh_token(identity=user_light)

				tokens = {
						'access_token'	: new_access_token,
						'refresh_token' : refresh_token,
				}
				print()
				log.debug("user_light['_id'] : %s", user_light["_id"] )
				log.debug("new_access_token  : %s", new_access_token )
				log.debug("refresh_token 		 : %s", refresh_token )
				log.debug("new_refresh_token : %s", new_refresh_token )
				print()

				### save new refresh token in user db
				user["auth"]["refr_tok"] 	= refresh_token
				mongo_users.save(user)
				
				### update user log in db
				### TO DO 

				### DEBUGGING CONFIRMATION EMAIL
				# confirm_email_token = generate_confirmation_token(payload_email)
				# log.debug("confirm_email_token : %s", confirm_email_token)

				return {	
									"msg" 		: "user -{}- is logged".format(payload_email) , 
									"tokens"	:  tokens
							}, 200

			else : 

				error_message = "wrong password"
				return { 
									"msg" : "incorrect login / {}".format(error_message) 
							}, 401