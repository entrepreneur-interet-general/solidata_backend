# -*- encoding: utf-8 -*-

"""
schema_users.py  
- provides the model for USER definition in DB and Flask-Restplus
"""

from log_config import log, pformat

log.debug("... loading schema_users.py ...")

from flask_restplus import fields 

from ._choices_user import * 
from .schema_generic import *
from .schema_logs import *



# ### generic info for update
# generic_data 		= fields.String(
# 										description	= "data about the user",
# 										attribute		= "data",
# 										example			= "example",
# 										default			= 'a new data',
# 										required		= True,
# 									)

### basic informations about a user
name 						= fields.String(
										description	= "name of the user",
										attribute		= "name",
										example			= "Elinor",
										default			= 'Anonymous User',
										required		= False,
									)
surname 				= fields.String(
										description = "surname of the user",
										attribute		= "surname",
										example			= "Ostrom",
										required 		= False,
									)
email 					= fields.String(
										description = "email of the user",
										attribute		= "email",
										example			= "elinor.ostrom@emailna.co", ### uses https://www.mohmal.com for temporary emails
										required		= True,
									)

### auth 
pwd							= fields.String(
										description = "password of the user",
										attribute		= "pwd",
										example			= "a-very-common-password",
										required		= True,
									)
confirmed_usr		= fields.Boolean(
										description	= "user has confirmed its account from his email",
										attribute		= "conf_usr",
										example			= False,
										required		= False,
										default			= False,
									)
blacklisted_usr		= fields.Boolean(
										description	= "user has confirmed its account from his email",
										attribute		= "blklst_usr",
										example			= False,
										required		= False,
										default			= False,
									)
role						= fields.String(
										description = "role / authorization level of the user",
										attribute		= "role",
										example			= "guest",
										enum				= user_roles,
										default			= "guest",
									)
acc_tok					= fields.String(
										description = "access token of user",
										attribute		= "acc_tok",
										example			= "a-json-web-access-token",
										default			= "no_access_token",
									)
refr_tok				= fields.String(
										description	= "refresh token of user",
										attribute		= "refr_tok",
										example			= "a-json-web-refresh-token",
										default			= "no_refresh_token",
									)
old_refr_tok		= fields.String(
										description	= "expired refresh token of user",
										attribute		= "old_refr_tok",
										example			= "an-old-json-web-refresh-token",
										default			= "no_old_refresh_token",
										required		= False,
									)
edit_auth				= fields.List(
										fields.String(
											description = "edit auth of an user",
											enum				= user_actions_proj,
										),
										attribute		= "edit_auth", 
										default			= [] 
									)

### preferences
language				= fields.String(
										description = "language preference", 
										example 		= "en",
										attribute		= "lang",	
										default			= "en",
									)
# fav_list				= fields.List(
# 										fields.String(
# 											description = "ids of the favorites projects created by the user"
# 										),
# 										attribute		= "fav_list", 
# 										default			= [] 
# 									)
is_fav					= fields.Boolean(
										description	= "is the document a favorite ?",
										attribute		= "is_fav",
										example			= False,
										required		= True,
										default			= False,
									)

### profesional infos
structure			= fields.String(
											description	= "structures / organisations the user"
										)
										# example			= ["my structure A", "my structure B"],
										# attribute		= "struct",	
										# default			= []
struct_profile	= fields.String(
											description	= "structures / organisations profile",
											example			= "public_state",
											enum				= user_structure,
										)
										# attribute		= "struct_profiles",	
										# default			= []
usr_profile				= fields.String(
											description	= "profiles of the user",
											enum				= user_profiles,
										)
usr_profiles				= fields.List(
										usr_profile,
										# enum				= user_profiles,
										example			= ["organizer"],
										attribute		= "profiles",	
										default			= []
									)


### FOR GENERIC MODELS
user_data = {
	"data" 			: generic_data,
}

user_identity = {
	"email" 			: email,
}

user_pwd = {
	"pwd"		      : pwd,
}

user_login = {
	"email" 			: email,
	"pwd"		      : pwd,
}

user_basics = {
	"name" 				: name,
	"surname" 		: surname,
	"email" 			: email,
}

user_register = {
	"name" 				: name,
	"surname" 		: surname,
	"email" 			: email,
	"pwd"		      : pwd,
}

old_refresh_token = {
	"old_refresh_token" : old_refr_tok,
}


### FOR MODELS TO INSERT IN DB
user_auth_in = {
	"pwd"		      : pwd,
	"conf_usr"		: confirmed_usr,
	"role"	      : role,
	# "acc_tok"			: acc_tok,
	"refr_tok"		: refr_tok,
	"blklst_usr"  : blacklisted_usr,
}

# user_preferences_in = {
# 	"lang"  		: language,
# 	# "fav_list" 	: fav_list
# }

# user_professional_in = {
# 	"struct" 					: structure,
# 	"struct_profiles" : struct_profile,
# }

usr_profile_ = {
	"lang"  				: language,
	"usr_profiles"  : usr_profiles,
}

### FOR MODELS TO EXPORT OUT OF DB
user_auth_out = {
	# "pwd"		      : pwd,
	"role"	      : role,
	"conf_usr"		: confirmed_usr,
	# "acc_tok"			: acc_tok,
}

# user_preferences_out = {
# 	"language" 	: language,
# 	# "favorites"	: fav_list
# }

# user_professional_out = {
# 	"structures" 					: structures,
# 	"structures_profiles" : struct_profiles,
# }
