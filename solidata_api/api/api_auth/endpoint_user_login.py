# -*- encoding: utf-8 -*-

"""
endpoint_user_login.py  
"""

from solidata_api.api import *

log.debug(">>> api_auth ... creating api endpoints for USER_LOGIN")

### import mongo utils
from solidata_api._core.queries_db import mongo_users

### create namespace
ns = Namespace('login', description='User : login related endpoints')

### import models 
from solidata_api._models.models_user import LoginUser, User_infos, AnonymousUser
model_login_user  		= LoginUser(ns).model
model_user				= User_infos(ns)
model_user_access		= model_user.model_access
model_user_login_out	= model_user.model_login_out


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 

# @cross_origin()
@ns.route('/anonymous/')
class AnonymousLogin(Resource):

	@ns.doc('user_anonymous')
	@ns.doc(responses={200: 'success : anonymous user created with its access and refresh tokens'})
	def get(self):
		"""
		Login as anonymous user

		>
			--- needs   : nothing in particular
			>>> returns : msg, anonymous access_token + anonymous refresh_token with a short expiration date
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
		expires 					= app.config["JWT_ANONYMOUS_REFRESH_TOKEN_EXPIRES"]
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
	@anonymous_required
	@ns.doc(responses={200: 'success : user logged with its access and refresh tokens'})
	@ns.doc(responses={401: 'error client : incorrect login or no user'})
	def post(self):
		"""
		Log in an user given an email and a password 
		- checks if email exists in db 
		- check if salted pwd is equals to user's

		>
			--- needs   : an anonymous access_token (please use '.../login/anonymous/' first)
			>>> returns : msg, is_user_confirmed, preferences, access_token, refresh_tokens
		"""

		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )
		log.debug ("payload : \n{}".format(pformat(ns.payload)))

		### retrieve current user identity from refresh token
		claims 				= get_jwt_claims() 
		log.debug("claims : \n %s", pformat(claims) )
		
		### retrieve infos from form
		payload_email 				= ns.payload["email"]
		log.debug("payload_email  : %s", payload_email )

		payload_pwd   				= ns.payload["pwd"]
		log.debug("payload_pwd    : %s", payload_pwd )

		payload_renew_refr_token   	= ns.payload.get("renew_refresh_token", app.config["JWT_RENEW_REFRESH_TOKEN_AT_LOGIN"] )
		log.debug("payload_renew_refr_token    : %s", payload_renew_refr_token )

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
				# user_light 				= marshal( user , model_user_access)
				user_light 				= marshal( user , model_user_login_out)
				# user_light["_id"] 		= str(user["_id"])
				log.debug("user_light : \n %s", pformat(user_light) )

				### Use create_access_token() to create user's new access token 
				log.debug("... access_token")
				new_access_token 	= create_access_token(identity=user_light, fresh=False)

				### create a new refresh_token when logged
				log.debug("... refresh_token : create a new one...")
				if payload_renew_refr_token and user["auth"]["conf_usr"] == True :
					log.debug("... refresh_token")
					expires 					= app.config["JWT_REFRESH_TOKEN_EXPIRES"] 
					refresh_token 				= create_refresh_token( identity=user_light, expires_delta=expires )
					user["auth"]["refr_tok"] 	= refresh_token
				
				### retrieve existing refresh_token from db
				else :
					log.debug("... refresh_token : get existing one...")
					refresh_token 		= user["auth"]["refr_tok"]  

				### store tokens in dict
				tokens = {
						'access_token'	: new_access_token,
						'refresh_token' : refresh_token,
				}
				print()
				log.debug("user_light['_id'] : %s", user_light["_id"] )
				log.debug("user_light 		 : \n%s", user_light )
				log.debug("new_access_token  : \n%s", new_access_token )
				log.debug("refresh_token 	 : \n%s", refresh_token )
				print()

				### update user log in db
				# user = create_modif_log(doc=user, action="login")
				user["log"]["login_count"] += 1
				mongo_users.save(user)

				return {	
							"msg"				: "user '{}' is logged".format(payload_email),

							# "is_user_confirmed" : user["auth"]["conf_usr"],
							# "_id"				: str(user["_id"]),
							# "infos"				: user["infos"],
							# "profile"			: user["profile"],
							
							"data"				: user_light,
							"tokens"			: tokens

						}, 200

			else : 

				error_message = "wrong password"
				return { 
							"msg" 				: "incorrect login / {}".format(error_message) 
						}, 401



