# -*- encoding: utf-8 -*-

"""
endpoint_login.py  
- provides the API endpoints for consuming and producing
	REST requests and responses
"""

from log_config import log, pformat
log.debug(">>> api_users ... creating api endpoints for USER_REGISTER")

from	bson import json_util
from	bson.objectid import ObjectId
from	bson.json_util import dumps

from flask import current_app, request
from flask_restplus import Namespace, Resource, fields, marshal, reqparse
from 	werkzeug.security 	import 	generate_password_hash #, check_password_hash

### import JWT utils
import jwt
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required

### import mongo utils
from solidata_api.application import mongo
from solidata_api._core.queries_db import mongo_users

### import auth utils
# from solidata_api._auth import token_required

# ### import data serializers
from solidata_api._serializers.schema_users import *  

### create namespace
ns = Namespace('register', description='User register ')

### import parsers
from solidata_api._parsers.parser_pagination import pagination_arguments

### import models 
from .models import * # model_user, model_new_user
model_register_user			= NewUser(ns).model
model_register_user_out	= User_out(ns).model_for_token
model_user							= User_in(ns).model


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

# cf : response codes : https://restfulapi.net/http-status-codes/ 

"""
{
	"name": "Julien",
	"surname": "Paris",
	"email": "jul.paris@gmail.com",
	"pwd": "my_password"
}
"""


@ns.route('/')
class Register(Resource):
	@ns.doc('create_user')
	@ns.expect(model_register_user, validate=True)
	# @ns.marshal_with(model_register_user_out, envelope="new_user", code=201)
	def post(self):
		"""
		create / register a new user
		just needs an email, a name, a surname and and a password
		"""
		print()
		log.debug( self.__class__.__name__ )
		log.debug ("payload : \n{}".format(pformat(ns.payload)))

		### retrieve infos from form 
		payload_email = ns.payload["email"]
		payload_pwd 	= ns.payload["pwd"]
		log.debug("email : %s", payload_email )
		log.debug("password : %s", payload_pwd )

		### chek if user already exists in db
		existing_user = mongo_users.find_one({"infos.email" : payload_email})
		log.debug("existing_user : ", existing_user)

		if existing_user is None or payload_pwd not in ['test', 'password'] :

			# create hashpassword
			hashpass = generate_password_hash(payload_pwd, method='sha256')
			log.debug("hashpass : %s", hashpass)

			# create user dict
			new_user_infos 					= {"infos" : ns.payload, "auth" : ns.payload }
			new_user 								= marshal( new_user_infos , model_user)
			new_user["auth"]["pwd"] = hashpass
			log.info("new user is being created : \n%s", pformat(new_user))

			# create JWT : access and refresh token
			print()
			log.debug("... create_access_token")
			access_token 	= create_access_token(identity=new_user)
			print()
			log.debug("... refresh_token")
			refresh_token = create_refresh_token(identity=new_user)
			tokens = {
					'access_token'	: access_token,
					'refresh_token'	: refresh_token
			}

			log.info("tokens : \n%s", pformat(tokens))

			new_user["auth"]["acc_tok"] 	= access_token
			new_user["auth"]["refr_tok"] 	= refresh_token


			# save new user in db
			mongo_users.insert( new_user )

			log.info("new user is created : \n%s", pformat(new_user))

			# return marshal(new_user, model_register_user_out), 200
			return { 
								"message"		: "new user has been created",
								# "new_user" 	: new_user,
								"tokens"		: tokens
							}, 200

		else :
			
			return {"message" : "this email is already taken "}, 401