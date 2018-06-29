# -*- encoding: utf-8 -*-

"""
auth_decorator.py  
- creates a token_required decorator
"""

from log_config import log, pprint, pformat
log.debug ("... loading token_required ...")

from functools import wraps, partial, update_wrapper
from flask import request, current_app as app

# extended JWT 
# cf : http://flask-jwt-extended.readthedocs.io/en/latest/tokens_from_complex_object.html
# import jwt
from solidata_api.application import jwt_manager
from flask_jwt_extended import (
		verify_jwt_in_request, create_access_token,
		get_jwt_claims
)


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### AUTH DECORATORS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###


@jwt_manager.user_claims_loader
def add_claims_to_access_token(user):
		"""
		Create a function that will be called whenever create_access_token
		is used. It will take whatever object is passed into the
		create_access_token method, and lets us define what custom claims
		should be added to the access token.
		"""
		log.debug("user : \n%s", user)

		claims_to_store_into_jwt =  {
			'_id'				  : user["_id"],
			'infos'				: user["infos"],
			'auth'				: user["auth"],
			# 'datasets'		: user["datasets"],
			'preferences'	: user["preferences"],
		}

		log.debug("claims_to_store_into_jwt : \n%s", pformat(claims_to_store_into_jwt))

		return claims_to_store_into_jwt


@jwt_manager.user_identity_loader
def user_identity_lookup(user):
		"""
		Create a function that will be called whenever create_access_token
		is used. It will take whatever object is passed into the
		create_access_token method, and lets us define what the identity
		of the access token should be.
		"""
		log.debug("user : \n %s", pformat(user))
		
		### load email as identity in jwÒt
		try : 
			identity = user["infos"]["email"]
			# identity = str(user["_id"])
		except : 
			identity = None
			
		log.debug("identity : \n %s", identity)

		return identity





### custom decorators 

def admin_required(func):
	"""
	check if user has addmin level
	"""
	@wraps(func)
	def wrapper(*args, **kwargs):
		
		print()
		print("-+- "*40)

		verify_jwt_in_request()
		claims = get_jwt_claims()
		log.debug("claims : \n %s", pformat(claims) )
		
		if claims["auth"]["role"] != 'admin':
			return { "msg" : "Admins only !!! " }, 403
		else:
			return func(*args, **kwargs)
	
	return wrapper



### cf : https://stackoverflow.com/questions/13931633/how-can-a-flask-decorator-have-arguments/13932942#13932942
def current_user_required(func):
	"""
	check if user has addmin level
	"""
	
	@wraps(func)
	def wrapper(*args, **kwargs):

		print()
		print("-+- "*40)

		user_oid = kwargs["user_oid"] 
		log.debug( "user_oid : %s" , user_oid )

		verify_jwt_in_request()
		claims = get_jwt_claims()
		log.debug("claims : \n %s", pformat(claims) )
		
		if user_oid != claims["_id"]  : 

			if claims["auth"]["role"] == 'admin' :
				return func(*args, **kwargs)

			else : 
				return { "msg" : "Admins or user {} only  !!! ".format(user_oid) }, 403

		else:
			return func(*args, **kwargs)
	
	return wrapper


'''
class current_user_required(object) :
	
	def __init__(self, user_id) :
		"""
		If there are decorator arguments, the function
		to be decorated is not passed to the constructor!
		"""
		log.debug("Inside __init__()")
		self.user_id = user_id

	def __call__(self, fn):
		"""
		check if user has addmin level 
		or is really the current user 

		If there are decorator arguments, __call__() is only called
		once, as part of the decoration process! You can only give
		it a single argument, which is the function object.
		"""
		log.debug("Inside __call__()")

		def wrapped_f(*args, **kwargs):
			
			log.debug("Inside wrapper()")
			log.debug( "self.user_id : %s" , self.user_id)

			verify_jwt_in_request()
			claims = get_jwt_claims()
			log.debug("claims : \n %s ", pformat(claims) )

			if claims["auth"]["role"] != 'admin' or str(self.user_id) != claims["_id"] :
				return { "msg" : "Admins or real user only !!! " }, 403
			else:
				return fn(*args, **kwargs)

		return wrapped_f
'''



def token_required(f):
	"""
	basic JWT parser
	"""
	@wraps(f)
	def decorated(*args, **kwargs):
		
		token 			= None
		auth_level 	= "guest"

		invalid_msg = {
				'message': 'Invalid token. Registeration and / or authentication required',
				'authenticated': False
		}
		expired_msg = {
				'message': 'Expired token. Reauthentication required.',
				'authenticated': False
		}

		### authentication
		if "X-API-KEY" in request.headers : 

			token = request.headers["X-API-KEY"]

			### JWT decryption
			# try : 
			# 	data 	= jwt.decode(token, app.config['JWT_SECRET_KEY'])
			# 	email = data["sub"]
			# 	# get corresponding user

			# except jwt.ExpiredSignatureError:
			# 		return expired_msg, 401 # 401 is Unauthorized HTTP status code
			
			# except (jwt.InvalidTokenError, Exception) as e:
			# 		log.warning(e)
			# 		return invalid_msg, 401

		if not token :
			return {"message" : "token is missing"}, 401
		
		if token == False :
			return {"message" : "token is wrong..."}, 401 
		

		log.debug("token : {} / auth_level : {}".format(token, auth_level))

		return f(*args, **kwargs)

	return decorated