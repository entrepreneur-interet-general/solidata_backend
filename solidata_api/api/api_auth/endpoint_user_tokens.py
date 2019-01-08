# -*- encoding: utf-8 -*-

"""
endpoint_user_tokens.py  
"""

from solidata_api.api import *

# from log_config import log, pformat
log.debug(">>> api_auth ... creating api endpoints for USER_TOKENS")

### create namespace
ns = Namespace('tokens', description='User : tokens freshening related endpoints')

### import models 
from solidata_api._models.models_user import * #User_infos, AnonymousUser
model_user				= User_infos(ns)
model_user_access		= model_user.model_access
model_user_login_out	= model_user.model_login_out
model_old_refresh_token = ExpiredRefreshToken(ns).model


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 

# cf : http://flask-jwt-extended.readthedocs.io/en/latest/refresh_tokens.html
"""
RESPONSE CODES 
cf : https://restfulapi.net/http-status-codes/

	200 (OK)
	201 (Created)
	202 (Accepted)
	204 (No Content)
	301 (Moved Permanently)
	302 (Found)
	303 (See Other)
	304 (Not Modified)
	307 (Temporary Redirect)
	400 (Bad Request)
	401 (Unauthorized)
	403 (Forbidden)
	404 (Not Found)
	405 (Method Not Allowed)
	406 (Not Acceptable)
	412 (Precondition Failed)
	415 (Unsupported Media Type)
	500 (Internal Server Error)
	501 (Not Implemented)

"""

@ns.doc(security='apikey')
@ns.route('/confirm_access')
class ConfirmAccessToken(Resource) :

	# @jwt_required
	@guest_required
	def get(self) : 
		"""
		Confirm access_token given

		>
			--- needs   : a valid access_token in the header 
			>>> returns : msg, a new_access_token
		"""

		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )
		# log.debug ("payload : \n{}".format(pformat(ns.payload)))

		### retrieve current user identity from refresh token
		claims 				= get_jwt_claims() 
		log.debug("claims : \n %s", pformat(claims) )

		user_id = claims["_id"]

		if user_id == None :
			return {
						"msg" 	: "user not found " , 
					}, 401
		
		else : 
			return {
						"msg" 	: "user found " , 
						"data"	: claims ,
					}, 200


@ns.doc(security='apikey')
@ns.route('/new_access_token')
class NewAccessToken(Resource) :

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
		user_identity = get_jwt_identity()
		log.debug("user_identity : \n %s", user_identity)

		### retrieve user from db to get all infos
		# user = mongo_users.find_one( {"infos.email" : user_email } )
		user = mongo_users.find_one( {"_id" : ObjectId(user_identity) } )
		log.debug("user : \n %s", pformat(user)) 

		# if user or user_email == "anonymous":
		if user : 
				
			if user : 
				# user_light 	= marshal( user , model_user_access)
				# user_light["_id"] 	= str(user["_id"])
				user_light 			= marshal( user , model_user_login_out)

			# elif user_email == "anonymous" :
			# 	anon_user_class 	= AnonymousUser()
			# 	user_light 			= anon_user_class.__dict__

			### create new access token
			new_access_token = create_access_token(identity=user_light, fresh=False)
			log.debug("new_access_token : \n %s ", new_access_token)

			### store tokens
			token = {
					'access_token'	: new_access_token,
					'salt_token' 	: public_key_str,
			}

			return {	
						"msg" 		: "new access token for user : {} ".format(user_identity) , 
						"data"		: user_light,
						"tokens"	: token
					}, 200 		### indicates to redirect to other URL
	
		else : 
			return {
						"msg" 		: "user not found or is anonymous" , 
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
			user_light 			= marshal( user , model_user_access)
			user_light["_id"] 	= str(user["_id"])

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
		# decoded_token 			= decode_token(raw_jwt)
		decoded_token 			= jwt.decode(raw_jwt, app.config.get('JWT_SECRET_KEY'), options={'verify_exp': False})
		log.debug("decoded_token : \n %s", pformat(decoded_token))

		### check jwt and user's identity from old refresh_token
		jwt_type			= decoded_token["type"]
		jwt_identity 		= decoded_token["jti"]
		log.debug('jwt_type : {} / jwt_identity : {}'.format(jwt_type, jwt_identity) )
		user_identity 		= decoded_token["identity"]
		log.debug('user_identity from old refresh_token : \n%s', user_identity )


		# if user_identity != "anonymous" and jwt_type == "refresh" : 
		if user_identity and jwt_type == "refresh" : 

			### find user  in db
			user = mongo_users.find_one( {"_id" : ObjectId(user_identity) } ) 
			# user = mongo_users.find_one( {"infos.email" : user_identity } ) 
			log.debug("user : \n %s", pformat(user)) 

			if user :

				### check if there is something wrong : user's email not confirmed | user blacklisted
				if user["auth"]["conf_usr"] and user["auth"]["is_blacklisted"] == False : 

					### marshal user's info 
					user_light 				= marshal( user , model_user_login_out)
					# user_light["_id"] 		= str(user["_id"])
					log.debug("user_light : \n %s", pformat(user_light)) 

					# create a new refresh_token 
					new_refresh_token 		= create_refresh_token(identity=user_light)

					# and save it into user's data in DB
					user["auth"]["refr_tok"] = new_refresh_token
					mongo_users.save(user)
					log.debug("new_refresh_token is saved in user's data : %s", new_refresh_token ) 

					# create user's new_access_token 
					new_access_token 		= create_access_token(identity=user_light)

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
