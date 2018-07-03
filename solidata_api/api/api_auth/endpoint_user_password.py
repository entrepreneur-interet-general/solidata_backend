# -*- encoding: utf-8 -*-

"""
endpoint_user_password.py  
- provides the API endpoints for consuming and producing
	REST requests and responses
"""

from log_config import log, pformat
log.debug(">>> api_auth ... creating api endpoints for USER_PASSWORD")

from  datetime import datetime, timedelta
from	bson import json_util
from	bson.objectid import ObjectId
from	bson.json_util import dumps

from . import api

from flask import request, current_app as app, render_template
from flask_restplus import Namespace, Resource, fields, marshal, reqparse
from 	werkzeug.security 	import 	generate_password_hash, check_password_hash

### import mailing utils
from solidata_api._core.emailing import send_email

### import JWT utils
import jwt
from flask_jwt_extended import (
		jwt_required, jwt_refresh_token_required, jwt_optional, fresh_jwt_required,
		create_access_token, create_refresh_token,
		get_jwt_identity, get_jwt_claims, get_raw_jwt,
)
from solidata_api._auth import admin_required, current_user_required, anonymous_required, renew_pwd_required # token_required

### import mongo utils
# from solidata_api.application import mongo
from solidata_api._core.queries_db import mongo_users


# ### import data serializers
from solidata_api._serializers._choices_user import bad_passwords

### create namespace
ns = Namespace('password', description='User : password related endpoints')

### import parsers
# from solidata_api._parsers.parser_pagination import pagination_arguments

### import models 
from solidata_api._models.models_user import EmailUser, PasswordUser, User_infos
model_email_user  	= EmailUser(ns).model
model_pwd_user			= PasswordUser(ns).model
model_user					= User_infos(ns).model_access

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 


@ns.route("/password_forgotten" )
@ns.response(404, 'user not found')
class PasswordForgotten(Resource):

	@ns.doc(security='apikey')
	@ns.doc('password_send_email')
	@ns.expect(model_email_user)
	@anonymous_required
	def post(self):
		"""
		Send an email to allow user to reset its password

		>
			--- needs   : a valid anonymous access_token
			>>> returns : msg, a fresh access_token sent by email inside a link
		"""

		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )
		log.debug ("payload : \n{}".format(pformat(ns.payload)))

		### retrieve infos from form
		payload_email = ns.payload["email"]
		log.info("...'{}' has forgotten its password...".format(payload_email) )

		### retrieve user from db
		user = mongo_users.find_one( {"infos.email" : payload_email } ) #, {"_id": 0 })
		log.debug("user : \n %s", pformat(user)) 

		if user is None and payload_email != "anonymous" : 

			return { 	
								"msg" : "email {} doesn't exists in db".format(payload_email) 
							}, 401

		if user :  
			
			### marshal user's info 
			user_light							= marshal( user , model_user)
			user_light["_id"]				= str(user["_id"])
			user_light["renew_pwd"] = True
			log.debug("user_light : \n %s", pformat(user_light)) 

			# Use create_refresh_token() to create user's new access token for n days
			expires 								= app.config["JWT_RESET_PWD_ACCESS_TOKEN_EXPIRES"]
			renew_pwd_access_token 	= create_access_token(identity=user_light, expires_delta=expires, fresh=True)
			# new_refresh_token = create_refresh_token(identity=user_light, expires_delta=expires)
			log.debug("renew_pwd_access_token : \n %s", renew_pwd_access_token)

			### send a confirmation email if not RUN_MODE not 'dev'
			if app.config["RUN_MODE"] in ["prod", "dev_email"] : 
				
				# create url for confirmation to send in the mail
				confirm_url = app.config["DOMAIN_NAME"] + api.url_for(PasswordReset, token=renew_pwd_access_token, external=True)
				log.info("confirm_url : \n %s", confirm_url)

				# generate html body of the email
				html = render_template('emails/reset_your_password.html', confirm_url=confirm_url)
				
				# send the mail
				send_email( "Reset your password", payload_email, template=html )
			
			return { 
								"msg" : "email sent to {} with a link containing the renew_pwd_access_token to refresh your password".format(payload_email)
							}, 200




# The config  query paramater where the JWT is looked for is `token`,
# The default query paramater where the JWT is looked for is `jwt`,
# and can be changed with the JWT_QUERY_STRING_NAME option.
# Making a request to this endpoint would look like:
# /reset_password?token=<REFRESH_TOKEN>
# /reset_password + in <REFRESH_TOKEN> in header

@ns.doc(security='apikey')
@ns.route("/reset_password")
@ns.response(404, 'error in the redirection to rest password')
@ns.param('token', 'the refresh_token sent by email to allow you to post your new password')
class PasswordReset(Resource):

	@ns.doc('password_reset')
	@fresh_jwt_required
	@renew_pwd_required
	def get(self):
		"""
		Open a link (GET) to allow the user to reset its password

		>
			--- needs   : a valid fresh renew_pwd_access_token (f.e. received by email, with a short expiration date)
			>>> returns : msg, a new renew_pwd_access_token
		"""
		
		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )

		### retrieve user's email from jwt
		user_email 	= get_jwt_identity()
		log.info( "...'{}' is renewing its password...".format(user_email) ) 

		### retrieve sent token 
		sent_token = get_raw_jwt()
		log.debug( "sent_token : \n %s", sent_token ) 

		### find user in DB
		user = mongo_users.find_one({"infos.email" : user_email })
		
		### marshall infos
		user_light							= marshal( user , model_user)
		user_light["_id"] 			= str(user["_id"])
		user_light["renew_pwd"] = True

		### create a new and temporary refresh_token 
		expires 								= app.config["JWT_RESET_PWD_ACCESS_TOKEN_EXPIRES"]
		renew_pwd_access_token 	= create_access_token(identity=user_light, expires_delta=expires, fresh=True)
		# refresh_token	= user["auth"]["refr_tok"]
		# refresh_token = create_refresh_token(identity=user_light, expires_delta=expires) # sent_token

		### store tokens
		tokens = {
				'access_token'	: renew_pwd_access_token,
				# 'refresh_token'	: refresh_token
		}
		log.info("tokens : \n %s", pformat(tokens))

		return { 
							"msg" 		: "you are now allowed to enter/POST your new password with the renew_pwd_access_token sent, you have {} to renew your password".format(expires), 
							"tokens" 	: tokens
						}, 200

	
	@fresh_jwt_required
	@renew_pwd_required
	@ns.expect(model_pwd_user)
	def post(self):
		"""
		Update user's password with the new password : hash it, then save it in DB in corresponding user's data

		>
			--- needs   : a valid fresh renew_pwd_access_token (received by opening reset_password[GET], with a short expiration date)
			>>> returns : msg, a new refresh_token + a new access_token
		"""
		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )

		### retrieve user's email
		user_email 	= get_jwt_identity()
		log.info( "...'{}' has posted its new password...".format(user_email) ) 

		### retrieve infos from form 
		payload_pwd 	= ns.payload["pwd"]
		log.debug("payload_pwd : %s", payload_pwd )

		### validate password
		if payload_pwd not in bad_passwords : 

			### create hashpassword
			hashpass = generate_password_hash(payload_pwd, method='sha256')
			log.debug("hashpass : %s", hashpass)

			### find user in DB
			user = mongo_users.find_one({"infos.email" : user_email })

			### save new hashed password into user in DB
			user["auth"]["pwd"] = hashpass
			mongo_users.save(user)

			### marshall infos
			user_light = marshal( user , model_user)
			user_light["_id"] = str(user["_id"])

			### generate and store tokens as if it were a login
			access_token 	= create_access_token(identity=user_light)
			# refresh_token = create_refresh_token(identity=user_light)
			refresh_token = user["auth"]["refr_tok"]
			tokens = {
					'access_token'	: access_token,
					'refresh_token'	: refresh_token
			}

			return {
								"msg" 		: "your password is now updated with your new one", 
								"tokens" 	: tokens
						}, 200

		### password is very bad
		else :
			return {
								"msg" 		: "your password is very bad mate !!!", 
						}, 401