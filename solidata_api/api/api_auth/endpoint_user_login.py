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

# from flask import request, current_app
from flask_restplus import Namespace, Resource, fields, marshal, reqparse
from 	werkzeug.security 	import 	generate_password_hash, check_password_hash

### import JWT utils
import jwt
from flask_jwt_extended import (
		jwt_required, jwt_optional, create_access_token, create_refresh_token,
		get_jwt_identity, get_jwt_claims
)

### import mongo utils
# from solidata_api.application import mongo
from solidata_api._core.queries_db import mongo_users

### import auth utils
# from solidata_api._auth import token_required

# ### import data serializers
# from solidata_api._serializers.schema_users import *  

### create namespace
ns = Namespace('login', description='User login ')

### import parsers
# from solidata_api._parsers.parser_pagination import pagination_arguments

### import models 
from .models import * # model_user, model_new_user
model_login_user  	= LoginUser(ns).model
model_user					= User_out(ns).model


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
		login user with POST request
		checks if email exists in db 
		check if salted pwd is equals to user's
		return jwt : access token and refresh token
		"""

		### DEBUGGING
		print()		
		log.debug( self.__class__.__name__ )
		log.debug ("payload : \n{}".format(pformat(ns.payload)))

		token = None 
		error_message = None

		### retrieve infos from form
		payload_email = ns.payload["email"]
		payload_pwd   = ns.payload["pwd"]
		log.debug("email 	: %s", payload_email )
		log.debug("pwd 		: %s", payload_pwd )

		### retrieve user from db
		user = mongo_users.find_one( {"infos.email" : payload_email }, {"_id": 0 })
		log.debug("user : \n %s", pformat(user)) 

		if user is None : 

			error_message = "no such user in db"
			return {"message" : "incorrect login / {}".format(error_message) }, 401

		if user :  
			
			### check password
			pwd = user["auth"]["pwd"]
			if check_password_hash(pwd, payload_pwd) :

				### create JWT tokens
				# token = jwt.encode({
				# 		'sub'	: user["infos"]["email"],
				# 		'iat'	:	datetime.utcnow(),
				# 		'exp'	: datetime.utcnow() + timedelta(minutes=30)},
				# 		current_app.config['JWT_SECRET_KEY'])

				user_light 								= marshal( user , model_user)

				# Use create_access_token() and create_refresh_token() to create our
				# access and refresh tokens
				tokens = {
						'access_token'	: create_access_token(identity=user_light, fresh=True),
						'refresh_token'	: create_refresh_token(identity=user_light)
				}

				### update user log in db
				### TO DO 

				return {	
									"message" : "user {} is logged".format(payload_email) , 
									"tokens"	:  tokens
							}, 200

			else : 

				error_message = "wrong password"
				return {"message" : "incorrect login / {}".format(error_message) }, 401