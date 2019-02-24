# -*- encoding: utf-8 -*-

"""
_models/models_users.py  
"""

from log_config import log, pformat

log.debug("... loading models_users.py ...")


from flask_restplus import fields
from solidata_api.api import app

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
					_id			= None, 
					infos		= {	"email"		: "anonymous"}, 
					auth 		= {	
									"conf_usr"	: False, 
									"role" 		: "anonymous"
								},
					profile		= { "lang" 		: "en" } ,
					preferences = None
		) :
		log.debug( "ROUTE class : %s", self.__class__.__name__ )

		# self.data = {
		# 	"_id"					: None,
		# 	"infos" 			: ,
		# 	"auth"				: {"conf_usr" : False, "role" : "guest"},
		# 	"preferences"	:	None
		# }
		self._id 			= _id
		self.infos			= infos
		self.auth			= auth
		self.profile		= profile
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

		# self.mod = ns_.model( "User_register", user_register )
		if app.config["RSA_MODE"] == "yes" : 
			self.mod = ns_.model( "User_register", user_register )
		else : 
			self.mod = ns_.model( "User_register", user_register_nosalt )


	@property
	def model(self): 
		return self.mod


class LoginUser : 
	"""
	Model to display / marshal user Login form
	"""

	def __init__(self, ns_):

		# self.mod = ns_.model( "User_login", user_login )
		if app.config["RSA_MODE"] == "yes" : 
			self.mod = ns_.model( "User_login", user_login )
		else : 
			self.mod = ns_.model( "User_login", user_login_nosalt )

	@property
	def model(self): 
		return self.mod



class User_infos : 
	"""
	Model to display / marshal 
	user's infos
	"""

	def __init__(self, ns_) :
		
		model_type 					= "Usr"

		### SELF MODULES
		self._id 								= oid_field
		self.basic_infos 				= create_model_basic_infos(	ns_,	model_name=model_type+"_infos", 	is_user_infos=True)
		self.basic_infos_light	= create_model_basic_infos(	ns_,	model_name=model_type+"_infos", 	is_user_infos=True, is_user_light=True)
		self.public_auth				= create_model_public_auth(	ns_,	model_name=model_type+"_public_auth")
		self.specs							= create_model_specs(				ns_,	model_name=model_type+"_specs")
		self.log								= create_model_log(					ns_,	model_name=model_type+"_log", 		include_counts=True, counts_name="login_count")
		self.modif_log					= create_model_modif_log(		ns_,	model_name=model_type+"_modif_log")
		
		self.datasets 					= create_model_datasets(		ns_, 	model_name=model_type+"_datasets", 	include_fav=True, 	schema_list=["prj","dmt", "dmf","dsi","rec","tag"])
		self.datasets_light			= create_model_datasets(		ns_, 	model_name=model_type+"_datasets", 	include_fav=True, 	schema_list=["prj","dmt", "dmf","dsi","rec","tag"], is_light=True )
		
		self.team 							= create_model_team( 				ns_,	model_name=model_type+"_team")
		self.team_light 				= create_model_team(				ns_,	model_name=model_type+"_team", 		is_light=True)
		
		self.profile 							= create_model_profile( 	ns_,	model_name=model_type+"_profile")
		self.professional_infos 	= create_professional_infos(ns_, 	model_name=model_type+"_professionnal_infos")

		self.auth_in						= create_model_auth(				ns_,	model_type+"_authorizations", 	schema=user_auth_in)
		# self.auth_in				= fields.Nested(
		# 			ns_.model(model_type+"_authorizations",  	user_auth_in  )
		# 		)
		self.auth_out						= create_model_auth(				ns_,	model_type+"_authorizations", 	schema=user_auth_out)
		# self.auth_out				= fields.Nested(
		# 			ns_.model(model_type+"_authorizations",  	user_auth_out  )
		# 		)


		self.model_id = {
			'_id' 					: self._id,
		}		
		self.model_infos = {
			'infos' 				: self.basic_infos,
		}
		self.model_infos_light = {
			'infos' 				: self.basic_infos_light,
		}
		self.profile_alone = {
			'profile' 				: self.profile,
		}
		self.model_in = {
			'modif_log'				: self.modif_log , 
			"datasets"				: self.datasets ,
			'profile' 				: self.profile,
			'professional_infos' 	: self.professional_infos,		
		}
		self.spec_auth_log = {
			'public_auth' 	: self.public_auth,
			'specs'					: self.specs , 
			'log'						: self.log , 
		}
		self.model_min = { 
				**self.model_infos , 
				**self.spec_auth_log
		}
		self.model_min_light = { 
				**self.model_infos_light , 
				# **self.spec_auth_log
		}
		self.model_auth_in = {  
			"auth" 				: self.auth_in 
		}
		self.model_auth_out = { 
			"auth" 				: self.auth_out 
		}
		self.model_team_full = {
			'team'				: self.team ,
		}
		self.model_team_light = {
			'team'				: self.team_light,
		}
		self.model_datasets_light = {
			'datasets'			: self.datasets_light,
		}

		### IN / complete data to enter in DB
		self.mod_complete_in  	= ns_.model(model_type+"_in", 
			{ 	
				**self.model_min, 
				**self.model_in, 
				**self.model_auth_in  
			} 
		)

		### OUT / complete data to enter in DB
		self.mod_complete_out	= ns_.model(model_type+"_out", 
			{ 
				**self.model_min, 
				**self.model_in, 
				**self.model_auth_out,
				**self.model_id 
			} 
		)

		### OUT GUEST / complete data to get out of DB
		self.mod_guest_out 		= ns_.model(model_type+"_guest_out",
			{ 
				**self.model_min, 
				**self.model_in, 
				**self.model_id, 
				**self.model_team_light 
			} 
		)

		### MIN / minimum data to marshall out 
		self.mod_minimum 		= ns_.model(model_type+"_minimum",
			{ 
				**self.model_min_light, 
				**self.model_id, 
				**self.model_datasets_light 
			}
		)


		### OUT ACCESS / for access tokens
		self.mod_access  		= ns_.model(model_type+"_access", 
			{ 
				**self.model_infos, 
				**self.model_id, 
				**self.model_auth_out
			}
		)

		### OUT LOGIN / for login tokens
		self.mod_login_out  		= ns_.model(model_type+"_login", 
			{ 
				**self.model_infos, 
				**self.model_id, 
				**self.model_auth_out,
				**self.profile_alone
			}
		)


	@property
	def model_complete_in(self): 
		return self.mod_complete_in

	@property
	def model_complete_out(self): 
		return self.mod_complete_out

	@property
	def model_guest_out(self): 
		return self.mod_guest_out

	@property
	def model_minimum(self): 
		return self.mod_minimum
		
	@property
	def model_access(self): 
		return self.mod_access

	@property
	def model_login_out(self): 
		return self.mod_login_out