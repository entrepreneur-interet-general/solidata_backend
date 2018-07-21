# -*- encoding: utf-8 -*-

"""
_models/models_users.py  
- provides the models for all api routes
"""

from log_config import log, pformat

log.debug("... loading models_users.py ...")


from flask_restplus import fields

### import data serializers
from solidata_api._serializers.schema_logs import *  
from solidata_api._serializers.schema_generic import *  
from solidata_api._serializers.schema_users import *  

### import generic models functions
from solidata_api._models.models_generic import *

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
		

		### SELF MODULES

		### basic infos
		self.basic_infos 				= create_model_basic_infos(ns_,		model_name="User_infos", is_user_infos=True)
		self.log						  	= create_model_log(ns_, 					model_name="User_log", include_counts=True, counts_name="login_count")
		self.modif_log					= create_model_modif_log(ns_,			model_name="User_modif_log")
		self.datasets 					= create_model_datasets(ns_, 			model_name="User_datasets", include_fav=True, schema_list=["prj","dmt", "dmf","dsi","rec"])
		self.specs							= create_model_specs(ns_, 				model_name="User_specs")
		self.professional_infos = create_professional_infos(ns_, 	model_name="User_professionnal_infos")
		self.team 							= create_model_team(ns_,					model_name="User_team")

		### profile
		self.profile 			= fields.Nested( 
			ns_.model("User_profile", usr_profile_ )
		)


		### IN / complete data to enter in DB
		self.mod_complete_in  = ns_.model('User_in', {

				'infos' 							: self.basic_infos,
				'profile' 						: self.profile,
				'log'			          	: self.log , 
				'specs' 							: self.specs , 
				'modif_log' 					: self.modif_log , 
				"datasets"						: self.datasets ,
				'professional_infos' 	: self.professional_infos,
				'team'								: self.team ,

				'auth': fields.Nested(
					ns_.model('User_authorizations',  	user_auth_in  )
				),

		})

		### OUT / complete data to enter in DB
		self.mod_complete_out  = ns_.model('User_out', {

				'infos' 							: self.basic_infos,
				'profile' 						: self.profile,
				'specs' 							: self.specs , 
				'log'				          : self.log , 
				'modif_log' 					: self.modif_log , 
				"datasets"						: self.datasets ,
				'professional_infos' 	: self.professional_infos,
				'team'								: self.team ,

				'auth'		: fields.Nested(
					ns_.model('User_authorizations',  	user_auth_out  )
				),

			})


		### OUT / for access tokens
		self.mod_access  = ns_.model('User_access', {

				'infos' 			: self.basic_infos,
				# 'log' 			: self.user_log, 
				# 'profile' 	: self.profiles,
				# 'favorites'	: self.favorites,

				'auth'		: fields.Nested(
					ns_.model('User_authorizations',  	user_auth_out  )
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

