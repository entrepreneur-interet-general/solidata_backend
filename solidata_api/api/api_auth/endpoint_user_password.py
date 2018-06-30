# -*- encoding: utf-8 -*-

"""
endpoint_user_password.py  
- provides the API endpoints for consuming and producing
	REST requests and responses
"""

from log_config import log, pformat
log.debug(">>> api_users ... creating api endpoints for USER_PASSWORD")

from  datetime import datetime, timedelta
from	bson import json_util
from	bson.objectid import ObjectId
from	bson.json_util import dumps

from flask import request, current_app as app
from flask_restplus import Namespace, Resource, fields, marshal, reqparse
from 	werkzeug.security 	import 	generate_password_hash, check_password_hash

### import mailing utils
from flask_mail import Message

### import JWT utils
import jwt
from flask_jwt_extended import (
		jwt_required, jwt_optional, create_access_token, create_refresh_token,
		get_jwt_identity, get_jwt_claims
)
from solidata_api._auth import admin_required, current_user_required # token_required

### import mongo utils
# from solidata_api.application import mongo
from solidata_api._core.queries_db import mongo_users


# ### import data serializers
# from solidata_api._serializers.schema_users import *  

### create namespace
ns = Namespace('password', description='User password ')

### import parsers
# from solidata_api._parsers.parser_pagination import pagination_arguments

### import models 
# from .models import * # model_user, model_new_user
from solidata_api._models.models_user import *  
model_email_user  	= EmailUser(ns).model
model_user					= User_infos(ns).model_complete


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

# cf : response codes : https://restfulapi.net/http-status-codes/ 


# @ns.doc(security='apikey')
@ns.route("/pwd_forgot?token=<string:token>", defaults={'token' : None} )
@ns.route("/pwd_forgot/<string:user_oid>", defaults={'user_oid': None} )
@ns.response(404, 'user not found')
# @ns.param('user_oid', 'The user unique identifier')
class Password_forgot(Resource):

	# @current_user_required
	@ns.doc('password_send_email')
	@ns.expect(model_email_user)
	def post(self, token, user_oid):
		"""
		TO DO - send an email to allow user to reset its password
		"""

		### DEBUGGING
		print()		
		log.debug( "ROUTE class : %s", self.__class__.__name__ )
		log.debug ("payload : \n{}".format(pformat(ns.payload)))

		### retrieve infos from form
		payload_email = ns.payload["email"]
		log.debug("email 	: %s", payload_email )

		### retrieve user from db
		user = mongo_users.find_one( {"infos.email" : payload_email } ) #, {"_id": 0 })
		log.debug("user : \n %s", pformat(user)) 

		if user is None : 

			error_message = "no such user in db"
			return { "msg" : "email {} doesn't exists in db".format(error_message) }, 401

		if user :  
			
			### marshal user's info 
			user_light 				= marshal( user , model_user)
			user_light["_id"] = str(user["_id"])

			# Use create_refresh_token() to create user's new access token for n days
			expires 					= timedelta(days=2)
			new_refresh_token = create_refresh_token(identity=user_light, expires_delta=expires)
		

			### TO DO 

			### create link to send
			link_string = app.config["DOMAIN_NAME"] + "/api/auth/password/reset_password?" + app.config["JWT_QUERY_STRING_NAME"] + "=" + new_refresh_token
			log.debug("link_string : \n %s", link_string) 

			### send eamil containing link + message
			email_msg 	= Message( "Reset password emal", sender=app.config["ADMINS"][0], recipients=payload_email )



			
			
			return { 
								"msg" : "email sent to {} with a link to refresh your password" 
							}, 200


# @ns.doc(security='apikey')
@ns.route("/reset_password/<string:token>")
@ns.route("/reset_password?token=<string:token>")
@ns.response(404, 'error in the redirection to rest password')
@ns.param('token', 'The token sent by email to reset your password')
class Password_reset(Resource):

	# @current_user_required
	@ns.doc('password_reset')
	# @ns.expect(model_email_user)
	@jwt_required ### verify token from request args or header
	def get(self):
		"""
		TO DO - open a link to allow the user to reset its password
		"""
		pass

		return { 
							"msg" : "email sent to {} with a link to refresh your password" 
						}, 200