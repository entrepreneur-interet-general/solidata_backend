# -*- encoding: utf-8 -*-

"""
_models/models.py  
- provides the models for all api routes
"""

from flask_restplus import fields

### import data serializers
from solidata_api._serializers.schema_users import *  


### create models from serializers
# nested models : https://github.com/noirbizarre/flask-restplus/issues/8
# model_user_infos 	= ns.model( "User model", user_infos) #, mask="{name,surname,email}" )


class AnonymousUser : 
	"""
	Generic class t
	"""
	def __init__(	self, 
								_id					= None, 
								infos				= {	"email"			: "anonymous"}, 
								auth 				= {	"conf_usr"	: False, 
																"role" 			: "anonymous"
															},
								preferences = None
								) :
		log.debug( "ROUTE class : %s", self.__class__.__name__ )

		# self.data = {
		# 	"_id"					: None,
		# 	"infos" 			: ,
		# 	"auth"				: {"conf_usr" : False, "role" : "guest"},
		# 	"preferences"	:	None
		# }
		self._id 					= _id
		self.infos 				= infos
		self.auth	 				= auth
		self.preferences 	= preferences




class EmailUser : 
	"""
	Simple model to display one user's email
	"""

	def __init__(self, ns_):
		self.mod = ns_.model( "User_email", user_identity )
	
	@property
	def model(self): 
		return self.mod


class PasswordUser : 
	"""
	Simple model to display one user's password
	"""

	def __init__(self, ns_):
		self.mod = ns_.model( "User_password", user_pwd )
	
	@property
	def model(self): 
		return self.mod


class NewUser : 
	"""
	Model to display / marshal user Register form
	"""

	def __init__(self, ns_):
		self.mod = ns_.model( "User_register", user_register )
	
	@property
	def model(self): 
		return self.mod


class LoginUser : 
	"""
	Model to display / marshal user Login form
	"""

	def __init__(self, ns_):
		self.mod = ns_.model( "User_login", user_login )
	
	@property
	def model(self): 
		return self.mod


class User_infos : 
	"""
	Model to display / marshal 
	specific user's infos
	"""

	def __init__(self, ns_) :
		
		self.mod_complete  = ns_.model('User', {
				'infos': fields.Nested(
					ns_.model('User_public_data', user_basics )
				),
				'auth': fields.Nested(
					ns_.model('User_authorizations',  user_auth  )
				),
				'preferences': fields.Nested(
					ns_.model('User_preferences',  user_preferences_out  )
				),
				'datasets': fields.Nested(
					ns_.model('User_datasets',  user_datasets_out  )
				),
				'profile' : fields.Nested(
					ns_.model('User_profiles', user_profiles)
				),
				'professional' : fields.Nested(
					ns_.model('User_profesional', user_professional )
				),
		})

		self.mod_for_token = ns_.model('User_token', {
				'infos': fields.Nested(
					ns_.model('User_public_data', user_identity )
				),
				'auth': fields.Nested(
					ns_.model('User_authorizations',  user_auth_out  )
				),
				'preferences': fields.Nested(
					ns_.model('User_preferences',  user_preferences_out  )
				),
				'datasets': fields.Nested(
					ns_.model('User_datasets',  user_datasets_out  )
				),
		})

		self.mod_in        = ns_.model('User_in', {
				'infos': fields.Nested(
					ns_.model('User_public_data', user_basics )
				),
				'auth': fields.Nested(
					ns_.model('User_authorizations',  user_auth  )
				),
				'preferences': fields.Nested(
					ns_.model('User_preferences',  user_preferences_in  )
				),
				'datasets': fields.Nested(
					ns_.model('User_datasets',  user_datasets_in  )
				),
		})

		self.mod_update  = ns_.model('User_update', {
				'infos': fields.Nested(
					ns_.model('User_public_data', user_basics )
				),
				'profile' : fields.Nested(
					ns_.model('User_profiles', user_profiles)
				),
				'preferences': fields.Nested(
					ns_.model('User_preferences',  user_preferences_out  )
				),
				'professional' : fields.Nested(
					ns_.model('User_profesional', user_professional )
				),
		})

		self.mod_access  = ns_.model('User_access', {
				'infos': fields.Nested(
					ns_.model('User_public_data', user_basics )
				),
				'auth': fields.Nested(
					ns_.model('User_authorizations',  user_auth_out  )
				),
				'profile' : fields.Nested(
					ns_.model('User_profiles', user_profiles)
				),
				'preferences': fields.Nested(
					ns_.model('User_preferences',  user_preferences_out  )
				),
		})

	@property
	def model_complete(self): 
		return self.mod_complete

	@property
	def model_in(self): 
		return self.mod_in

	@property
	def model_for_token(self): 
		return self.mod_for_token

	@property
	def model_update(self): 
		return self.mod_update

	@property
	def model_access(self): 
		return self.mod_access

# class User_in : 

# 	def __init__(self, ns_) :

# 		self.mod        = ns_.model('User', {
# 				'infos': fields.Nested(
# 					ns_.model('User_public_data', user_basics )
# 				),
# 				'auth': fields.Nested(
# 					ns_.model('User_authorizations',  user_auth  )
# 				),
# 				'preferences': fields.Nested(
# 					ns_.model('User_preferences',  user_preferences_in  )
# 				),
# 				'datasets': fields.Nested(
# 					ns_.model('User_datasets',  user_datasets_in  )
# 				),
# 		})

# 	@property
# 	def model(self): 
# 		return self.mod