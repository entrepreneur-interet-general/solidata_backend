# -*- encoding: utf-8 -*-

"""
schema_users.py  
- provides the model for USER definition in DB and Flask-Restplus
"""

from log_config import log, pformat

from flask_restplus import fields, marshal
import json

user_auth_levels = [
	"admin", "staff", "collective", "registred", "guest"
]

name 						= fields.String(
										description="name of the user",
										attribute="name",
										default='Anonymous User',
										required=False,
									)
surname 				= fields.String(
										description="surname of the user",
										attribute="surname",
										required=False,
									)
email 					= fields.String(
										description="email of the user",
										attribute="email",
										required=False,
									)


password				= fields.String(
										description="password of the user",
										attribute="pwd",
										required=True,
									)
auth_level			= fields.String(
										description="authorization level of the user",
										attribute="auth_level",
										default="guest",
									)
token						= fields.String(
										description="public token of user",
										attribute="token",
										default="no_token",
									)


language				= fields.String(
										description="language preference", 
										attribute="lang",	
										default="en",
									)


structures			= fields.List(
										fields.String(
										description="structure / organisation the user"),
										default=[]
									)
profiles				= fields.List(
										fields.String(
										description="profile of the user"),
										default=[]
									)


proj_list				= fields.List(
										fields.String(
										description="ids of the projects created by the user"),
										attribute="proj_list", 
										default=[] 
									)
dm_list					= fields.List(
										fields.String(
										description="ids of the datamodels created by the user"),
										attribute="dm_list",
										default=[] 
									)
dsi_list				= fields.List(
										fields.String(
										description="ids of the datasets_in imported by the user"),
										attribute="dsi_list",
										default=[] 
									)
dso_list				= fields.List(
										fields.String(
										description="ids of the datasets_out exported by the user"), 
										attribute="dso_list",
										default=[] 
									)
dc_list					= fields.List(
										fields.String(
										description="ids of the correspondance_dicts created by the user"), 
										attribute="dc_list",
										default=[] 
									)
rec_list				= fields.List(
										fields.String(
										description="ids of the recipes created by the user"),
										attribute="rec_list",
										default=[] 
									)


user_basics = {
	"name" 				: name,
	"surname" 		: surname,
	"email" 			: email,
}

user_register = {
	"name" 				: name,
	"surname" 		: surname,
	"email" 			: email,
	"password"		: password,
}

user_preferences = {
	"language" : language
}

user_professional = {
	"structures" 		: structures,
	"profiles" 			: profiles
}

user_auth = {
	"password"		: password,
	"auth_level"	: auth_level,
	"token"				: token,
}

user_datasets = {
	"projects"							: proj_list,
	"datamodels"						: dm_list,
	"datasets_inputs"				: dsi_list,
	"datasets_outputs"			: dso_list,
	"correspondance_dicts"	: dc_list,
	"recipes"								: rec_list,
}





# user_infos = {
	
# 	"name" 				: name,
# 	"surname" 		: surname,
# 	"email" 			: email,

# 	"language"		: language,

# 	"auth_level"	: auth_level,
# 	"token"				: token,
	
# 	"projects"							: proj_list,
# 	"datamodels"						: dm_list,
# 	"datasets_inputs"				: dsi_list,
# 	"datasets_inputs"				: dso_list,
# 	"correspondance_dicts"	: dc_list,
# 	"recipes"								: rec_list,

# }

# ### ---------------------------------
# fake_user = {
# 	# "_id" : ObjectId("5b2173a00415489360a99f0d"),
# 	"name" : "Julien",
# 	"surname" : "Paris",
# 	"email" : "julien@cget.gouv.fr",
# 	"auth_level" : "admin",
# 	"proj_list" : [ 
# 			"001", 
# 			"00Z"
# 	]
# }

# user_nested 								= {}
# user_nested['infos'] 				= fields.Nested(user_basics)
# user_nested['preferences'] 	= fields.Nested(user_basics)
# user_nested['auth'] 				= fields.Nested(user_auth)
# user_nested['datasets']			= fields.Nested(user_datasets)

# user_nest 					= {}
# user_nest['infos'] 	= user_basics
# log.debug("test on fake_user : \n %s", pformat(marshal(fake_user, user_nest)) )
