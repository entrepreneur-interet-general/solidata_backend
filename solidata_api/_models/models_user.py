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

class UserData : 
	"""
	Simple model to display an user data
	"""

	def __init__(self, ns_):
		self.mod = ns_.model( "User_data", user_data )
	
	@property
	def model(self): 
		return self.mod
		

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


class ExpiredRefreshToken : 
	"""
	Simple model to display an old refresh token
	"""

	def __init__(self, ns_):
		self.mod = ns_.model( "Old_refresh_token", old_refresh_token )
	
	@property
	def model(self): 
		return self.mod


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
		
		self.basic_infos		= fields.Nested(
					ns_.model('User_public_data', user_basics )
				)

		self.profiles 			= fields.Nested(
					ns_.model('User_profiles', 					user_profiles)
				)

		self.modifications 	=  fields.List(
					fields.Nested(
							ns_.model('Modifications', 			modification )
					),
					default			= [] 
		)
		self.user_log 			= fields.Nested( 
			ns_.model("User_log", {
				'created_at'		: created_at,
				'modified_log'	: self.modifications
			})
		)


		### IN / complete data to enter in DB
		self.mod_complete_in  = ns_.model('User_in', {

				'infos' 	: self.basic_infos,
				'profile' : self.profiles,
				'log' 		: self.user_log , 

				'auth': fields.Nested(
					ns_.model('User_authorizations',  	user_auth_in  )
				),
				'preferences': fields.Nested(
					ns_.model('User_preferences',  			user_preferences_in  )
				),
				'datasets': fields.Nested(
					ns_.model('User_datasets',  				user_datasets_in  )
				),
				'professional' 	: fields.Nested(
					ns_.model('User_profesional', 			user_professional_in )
				),
		})

		### OUT / complete data to enter in DB
		self.mod_complete_out  = ns_.model('User_out', {

				'infos' 	: self.basic_infos,
				'profile' : self.profiles,
				'log' 		: self.user_log , 

				'auth'		: fields.Nested(
					ns_.model('User_authorizations',  	user_auth_out  )
				),
				'preferences'		: fields.Nested(
					ns_.model('User_preferences',  			user_preferences_out  )
				),
				'datasets'			: fields.Nested(
					ns_.model('User_datasets', 					user_datasets_out  )
				),
				'professional' 	: fields.Nested(
					ns_.model('User_profesional', 			user_professional_out )
				),

			})


		### OUT / for access tokens
		self.mod_access  = ns_.model('User_access', {

				'infos' 	: self.basic_infos,
				# 'log' 		: self.user_log, 
				# 'profile' : self.profiles,

				'auth'		: fields.Nested(
					ns_.model('User_authorizations',  	user_auth_out  )
				),
				'preferences': fields.Nested(
					ns_.model('User_preferences',  			user_preferences_out  )
				),
			})


	@property
	def model_complete_in(self): 
		return self.mod_complete_in

	@property
	def model_complete_out(self): 
		return self.mod_complete_out

	# @property
	# def model_update(self): 
	# 	return self.mod_update

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