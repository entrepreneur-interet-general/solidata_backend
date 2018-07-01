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

from . import api

from flask import current_app as app, request, render_template
from flask_restplus import Namespace, Resource, fields, marshal, reqparse
from 	werkzeug.security 	import 	generate_password_hash #, check_password_hash

### import mailing utils
# from solidata_api.application import mail
# from flask_mail import Message
from solidata_api._core.emailing import send_email

### import JWT utils
import jwt
from datetime import datetime, timedelta
from flask_jwt_extended import (
			create_access_token, create_refresh_token, 
			jwt_required, jwt_refresh_token_required, current_user,
			get_jwt_claims, get_jwt_identity
)

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
# from .models import * # model_user, model_new_user
from solidata_api._models.models_user import *  
model_register_user			= NewUser(ns).model
model_register_user_out	= User_infos(ns).model_for_token
model_user							= User_infos(ns).model_in
model_user_complete			= User_infos(ns).model_complete
model_user_access				= User_infos(ns).model_access #model_complete


bad_passwords = [ 'test', 'password', '12345' ]

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

# cf : response codes : https://restfulapi.net/http-status-codes/ 

"""
example form from client : 
{
	"name": "Elinor",
	"surname": "Ostrom",
	"email": "elinor.ostrom@emailna.co",
	"pwd": "a-very-common-password"
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
		log.debug( "ROUTE class : %s", self.__class__.__name__ )
		log.debug ("payload : \n{}".format(pformat(ns.payload)))

		### retrieve infos from form 
		payload_email = ns.payload["email"]
		payload_pwd 	= ns.payload["pwd"]
		log.debug("email : %s", payload_email )
		log.debug("password : %s", payload_pwd )

		### chek if user already exists in db
		existing_user = mongo_users.find_one({"infos.email" : payload_email})
		log.debug("existing_user : %s ", pformat(existing_user))

		if existing_user is None and payload_pwd not in bad_passwords :

			# create hashpassword
			hashpass = generate_password_hash(payload_pwd, method='sha256')
			log.debug("hashpass : %s", hashpass)

			# create user dict from form's data
			new_user_infos 					= {"infos" : ns.payload, "auth" : ns.payload }
			new_user 								= marshal( new_user_infos , model_user_complete)
			new_user["auth"]["pwd"] = hashpass
		
			# temporary save new user in db 
			mongo_users.insert( new_user )
			log.info("new user is being created : \n%s", pformat(new_user))

			# get back user from db to add its 
			user_created = mongo_users.find_one({"infos.email" : payload_email})
			new_user["_id"] = str(user_created["_id"])

			# create access and refresh tokens
			log.debug("... create_access_token")
			access_token 	= create_access_token(identity=new_user)
			
			log.debug("... refresh_token")
			### just create refresh token once / so it could be blacklisted
			# refresh_token = create_refresh_token(identity=new_user)
			expires 			= app.config["JWT_CONFIRM_EMAIL_REFRESH_TOKEN_EXPIRES"] # timedelta(days=7)
			refresh_token = create_refresh_token(identity=new_user, expires_delta=expires)

			tokens = {
					'access_token'	: access_token,
					'refresh_token'	: refresh_token
			}
			log.info("tokens : \n%s", pformat(tokens))

			# update new user in db
			# new_user["auth"]["refr_tok"] 	= refresh_token
			new_user["auth"]["refr_tok"] 	= user_created["auth"]["refr_tok"] 	= refresh_token
			mongo_users.save(user_created)

			log.info("new user is updated with its tokens : \n%s", pformat(new_user))

			new_user_out = marshal(new_user, model_register_user_out)



			### TO DO 
			### send a confirmation email if not RUN_MODE not 'dev'
			if app.config["RUN_MODE"] in ["prod", "dev_email"] : 
				
				# create url for confirmation to send in the mail
				confirm_url = app.config["DOMAIN_NAME"] + api.url_for(Confirm_email, token=refresh_token, external=True)
				log.info("confirm_url : \n %s", confirm_url)

				# generate html body of the email
				html = render_template('emails/confirm_email.html', confirm_url=confirm_url)
				
				# send the mail
				send_email( "Confirm your emal", payload_email, template=html )



			return { 
								"msg"			: "new user has been created and a confirmation link has been sent,  you have {} days to confirm your email...".format(expires),
								"data"		: new_user_out,
								"tokens"	: tokens
							}, 200

		else :
			
			return {"msg" : "this email is already taken "}, 401



@ns.route("/confirm_email")
@ns.response(404, 'error in the redirection to confirm email')
@ns.param('token', 'The token sent by email when registering to confirm your email')
class Confirm_email(Resource):

	# The config  query paramater where the JWT is looked for is `token`,
	# The default query paramater where the JWT is looked for is `jwt`,
	# and can be changed with the JWT_QUERY_STRING_NAME option.
	# Making a request to this endpoint would look like:
	# /confirm?token=<REFRESH_TOKEN>
	@ns.doc('confirm_email')
	# @jwt_required 
	@jwt_refresh_token_required ### verify refresh_token from request args or header
	def get(self):
		"""
		URL to confirm email sent once registered or when change email
		needs a refresh_token as URL argument like : 
		.../api/users/register/confirm?token=<REFRESH_TOKEN>
		"""
		print()
		log.debug( "ROUTE class : %s", self.__class__.__name__ )

		user_email 	= get_jwt_identity()
		log.debug( "user_email : \n %s", user_email ) 

		### !!! only works with access_token
		# claims = get_jwt_claims() 
		# log.debug(" claims : \n %s ", pformat(claims) )
		### retrieve and read token to get user's email
		# user_oid 		= claims["_id"]

		### find user created in db 
		# user_to_confirm 	= mongo_users.find_one({"_id" : ObjectId(user_oid)})
		user_to_confirm 	= mongo_users.find_one({"infos.email" : user_email })

		### marshal user infos
		user_light 				= marshal( user_to_confirm , model_user_access)
		user_light["_id"] = str(user_to_confirm["_id"])

		### renew the existing refresh token
		refresh_token 		= create_refresh_token(identity=user_light)

		### confirm user's email and create a real refresh_token
		user_to_confirm["auth"]["refr_tok"] = refresh_token
		user_to_confirm["auth"]["conf_usr"] = True
		mongo_users.save(user_to_confirm)

		### create a new access token
		access_token = create_access_token(identity=user_light)
		tokens = {
				'access_token'	: access_token,
				'refresh_token'	: refresh_token
		}
		log.info("tokens : \n%s", pformat(tokens))

		return { 
							"msg" : "email {} confirmed, new refresh token created...".format(user_email),
							"tokens"	: tokens
						}, 200