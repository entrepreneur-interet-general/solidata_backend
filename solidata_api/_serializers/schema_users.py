# -*- encoding: utf-8 -*-

"""
schema_users.py  
- provides the model for USER definition in DB and Flask-Restplus
"""

from log_config import log, pformat

from flask_restplus import fields, marshal
import json

from ._choices_user import * 


name 						= fields.String(
										description="name of the user",
										attribute="name",
										example="Elinor",
										default='Anonymous User',
										required=False,
									)
surname 				= fields.String(
										description="surname of the user",
										attribute="surname",
										example="Ostrom",
										required=False,
									)
email 					= fields.String(
										description="email of the user",
										attribute="email",
										example="commons@come.on",
										required=False,
									)

### auth 
pwd				      = fields.String(
										description="password of the user",
										attribute="pwd",
										example="a-very-strong-password",
										required=True,
									)
role			      = fields.String(
										description="role / authorization level of the user",
										attribute="role",
										example="guest",
										enum=user_roles,
										default="guest",
									)
acc_tok					= fields.String(
										description="access token of user",
										attribute="acc_tok",
										example="a-json-web-access-token",
										default="no_access_token",
									)
refr_tok				= fields.String(
										description="refresh token of user",
										attribute="refr_tok",
										example="a-json-web-refresh-token",
										default="no_refresh_token",
									)

### preferences
language				= fields.String(
										description="language preference", 
										example="en",
										attribute="lang",	
										default="en",
									)

### profesional infos
structures			= fields.List(
										fields.String(
										description="structure / organisation the user"),
										example="my structure",
										default=[]
									)
structure_profile	= fields.List(
										fields.String(
										description="structure / organisation profile"),
										enum=user_profiles,
										example="public_state",
										default=[]
									)
profiles				= fields.List(
										fields.String(
										description="profile of the user"),
										enum=user_profiles,
										example="organizer",
										default=[]
									)

### datasets infos
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


### FOR GENERIC MODELS
user_identity = {
	"email" 			: email,
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

user_auth = {
	"pwd"		      : pwd,
	"role"	      : role,
	"acc_tok"			: acc_tok,
	"refr_tok"		: refr_tok,
}

user_auth_out = {
	# "pwd"		      : pwd,
	"role"	      : role,
	"acc_tok"			: acc_tok,
}

### FOR MODELS TO INSERT IN DB
user_datasets_in = {
	"proj_"	: proj_list,
	"dm_"		: dm_list,
	"dsi"		: dsi_list,
	"dso_"	: dso_list,
	"dc_"	  : dc_list,
	"rec_"	: rec_list,
}
user_preferences_in = {
	"lang"  : language
}

user_professional = {
	"struct_"   		: structures,
	"profiles" 			: profiles
}

### FOR MODELS TO EXPORT OUT OF DB
user_datasets_out = {
	"projects"							: proj_list,
	"datamodels"						: dm_list,
	"datasets_inputs"				: dsi_list,
	"datasets_outputs"			: dso_list,
	"correspondance_dicts"	: dc_list,
	"recipes"								: rec_list,
}

user_preferences_out = {
	"language" : language
}

user_professional = {
	"structures" 		: structures,
	"profiles" 			: profiles
}
