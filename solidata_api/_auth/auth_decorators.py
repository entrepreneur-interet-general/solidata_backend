# -*- encoding: utf-8 -*-

"""
auth_decorator.py  
- creates a token_required decorator
"""

from log_config import log, pprint, pformat
log.debug (">>> _auth ... loading auth_decorator ...")

from functools import wraps, partial, update_wrapper
from flask import request, current_app as app, jsonify

#### import extended JWT 
# cf : http://flask-jwt-extended.readthedocs.io/en/latest/tokens_from_complex_object.html
from solidata_api.application import jwt_manager
from flask_jwt_extended import (
		verify_jwt_in_request, create_access_token,
		get_jwt_claims, get_raw_jwt
)


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### AUTH DECORATORS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###


### CLAIMS LOADER INTO JWT - for access_token
### cf : https://flask-jwt-extended.readthedocs.io/en/latest/custom_decorators.html 
@jwt_manager.user_claims_loader 
def add_claims_to_access_token(user):
	"""
	Create a function that will be called whenever create_access_token
	is used. It will take whatever object is passed into the
	create_access_token method, and lets us define what custom claims
	should be added to the access token.

	> needs a 'model_user_out' or 'model_access' as 'user'
	"""
	log.debug("-@- claims loader")
	log.debug("user : \n %s", pformat(user))

	sent_token = get_raw_jwt()
	log.debug("sent_token : \n %s", pformat(sent_token))

	### common claims
	claims_to_store_into_jwt =  {
		'_id'				: user["_id"],
		'infos'				: user["infos"],
		'auth'				: user["auth"],
		# 'datasets'		: user["datasets"],
		# 'profile'			: user["profile"],
		# 'professional'	: user["professional"],
	}

	### specific claims
	if "renew_pwd" in user : 
		claims_to_store_into_jwt["renew_pwd"] 			= user["renew_pwd"]

	if "reset_pwd" in user : 
		claims_to_store_into_jwt["reset_pwd"] 			= user["reset_pwd"]

	if "confirm_email" in user : 
		claims_to_store_into_jwt["confirm_email"] 		= user["confirm_email"]

	if user["infos"]["email"] == "anonymous" : 
		claims_to_store_into_jwt["is_anonymous"] 		= True

	if "renew_refresh_token" in user : 
		claims_to_store_into_jwt["renew_refresh_token"] = True


	log.debug("claims_to_store_into_jwt : \n%s", pformat(claims_to_store_into_jwt))

	return claims_to_store_into_jwt


### IDENTITY LOADER - for access_token or refresh_token
### cf : http://flask-jwt-extended.readthedocs.io/en/latest/tokens_from_complex_object.html 
@jwt_manager.user_identity_loader
def user_identity_lookup(user):
	"""
	Create a function that will be called whenever create_access_token
	is used. It will take whatever object is passed into the
	create_access_token method, and lets us define what the identity
	of the access token should be.
	"""
	log.debug("-@- identity loader")
	log.debug("user : \n %s", pformat(user))
	
	try : 
		### load email as identity in the jwt
		# identity = user["infos"]["email"]
		### load _id as identity in the jwt
		# identity = str(user["_id"])
		identity = user["_id"]
	except : 
		identity = None
		
	log.debug("identity : \n %s", identity)

	return identity



### EXPIRED TOKENS
### cf : http://flask-jwt-extended.readthedocs.io/en/latest/changing_default_behavior.html 
@jwt_manager.expired_token_loader
def my_expired_token_callback():
	"""
	TO DO - Using the expired_token_loader decorator,
	we will now call this function whenever an expired
	token attempts to access an endpoint
	but otherwise valid access
	"""

	log.debug("-@- expired token checker")

	### if user is not confirmed, delete user from DB
	### otherwise return a link to refresh refresh_token

	return jsonify({
			'msg'		: 'The token has expired',
			'status'	: 401,
			'sub_status': 42,
	}), 401



### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### CUSTOM DECORATORS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
# cf : http://flask-jwt-extended.readthedocs.io/en/latest/custom_decorators.html 

def anonymous_required(func):
	"""
	Check if user is not logged yet in access_token 
	and has a 'anonymous' role
	"""
	@wraps(func)
	def wrapper(*args, **kwargs):
		
		log.debug("-@- anonymous checker")

		verify_jwt_in_request()
		claims = get_jwt_claims()
		log.debug("claims : \n %s", pformat(claims) )
		
		if claims["auth"]["role"] != 'anonymous' :
			return { "msg" : "Anonymous users only !!! " }, 403
		else :
			return func(*args, **kwargs)
	
	return wrapper


def anonymous_or_guest_required(func):
	"""
	Check if user is not logged yet in access_token 
	and has a 'guest' or 'anonymous' role
	"""
	@wraps(func)
	def wrapper(*args, **kwargs):
		
		log.debug("-@- anonymous checker")

		verify_jwt_in_request()
		claims = get_jwt_claims()
		log.debug("claims : \n %s", pformat(claims) )
		
		if claims["auth"]["role"] not in  ['guest', 'anonymous'] :
			return { "msg" : "Anonymous users or guests only !!! " }, 403
		else:
			return func(*args, **kwargs)
	
	return wrapper



def guest_required(func):
	"""
	Check if user is not logged yet in access_token 
	and has a 'guest' or 'anonymous' role
	"""
	@wraps(func)
	def wrapper(*args, **kwargs):
		
		log.debug("-@- anonymous checker")

		verify_jwt_in_request()
		claims = get_jwt_claims()
		log.debug("claims : \n %s", pformat(claims) )
		
		if claims["auth"]["role"] not in  ['admin', 'guest', 'registred', "staff" ] :
			return { "msg" : "Registred users only !!! " }, 403
		else:
			return func(*args, **kwargs)
	
	return wrapper


def admin_required(func):
	"""
	Check if user has admin level in access_token
	"""
	@wraps(func)
	def wrapper(*args, **kwargs):
		
		log.debug("-@- admin checker")

		verify_jwt_in_request()
		claims = get_jwt_claims()
		log.debug("claims : \n %s", pformat(claims) )
		
		if claims["auth"]["role"] != 'admin':
			return { "msg" : "Admins only !!! " }, 403
		else:
			return func(*args, **kwargs)
	
	return wrapper


def renew_pwd_required(func):
	"""
	Check if access_token has a claim 'renew_pwd' == True
	"""
	@wraps(func)
	def wrapper(*args, **kwargs):
		
		log.debug("-@- renew_pwd checker")

		verify_jwt_in_request()
		claims = get_jwt_claims()
		log.debug("claims : \n %s", pformat(claims) )
		
		try :
			if claims["renew_pwd"] == True:
				return func(*args, **kwargs)
		except :
			return { "msg" : "'renew_pwd' token expected !!! " }, 403
	
	return wrapper


def reset_pwd_required(func):
	"""
	Check if access_token has a claim 'reset_pwd' == True
	"""
	@wraps(func)
	def wrapper(*args, **kwargs):
		
		log.debug("-@- reset_pwd checker")

		verify_jwt_in_request()
		claims = get_jwt_claims()
		log.debug("claims : \n %s", pformat(claims) )
		
		try :  
			if claims["reset_pwd"] == True:
				return func(*args, **kwargs)
		except :
			return { "msg" : "'reset_pwd' token expected !!! " }, 403
	
	return wrapper


def confirm_email_required(func):
	"""
	Check if access_token has a claim 'confirm_email' == True
	"""
	@wraps(func)
	def wrapper(*args, **kwargs):
		
		log.debug("-@- confirm_email checker")

		verify_jwt_in_request()
		claims = get_jwt_claims()
		log.debug("claims : \n %s", pformat(claims) )
		
		if claims["confirm_email"] != True:
			return { "msg" : "'confirm_email' token expected !!! " }, 403
		else:
			return func(*args, **kwargs)
	
	return wrapper


### cf : https://stackoverflow.com/questions/13931633/how-can-a-flask-decorator-have-arguments/13932942#13932942
def current_user_required(func):
	"""
	Check in access_token + user_oid if user eihter : 
	- is who he claims to be 
	- if he has admin level 
	"""
	
	@wraps(func)
	def wrapper(*args, **kwargs):

		log.debug("-@- current_user checker")

		### check in kwargs
		user_oid = kwargs["user_oid"] 
		log.debug( "user_oid : %s" , user_oid )

		verify_jwt_in_request()
		claims = get_jwt_claims()
		log.debug("claims : \n %s", pformat(claims) )
		
		### check if oid sent is the same as the claim "_id"
		if user_oid != claims["_id"]  : 
			
			### authorize if user is an admin
			if claims["auth"]["role"] == 'admin' :
				return func(*args, **kwargs)

			### stops if user is neither an admin nor the current user
			else : 
				return { "msg" : "Admins or your own user only  !!! ".format(user_oid) }, 403

		else:
			return func(*args, **kwargs)
	
	return wrapper
