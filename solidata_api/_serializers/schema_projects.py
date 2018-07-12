# -*- encoding: utf-8 -*-

"""
schema_projects.py  
- provides the model for PROJECT definition in DB and Flask-Restplus
"""

from log_config import log, pformat

log.debug("... loading schema_projects.py ...")

from flask_restplus import fields

from .schema_generic import *
from .schema_logs import *
from .schema_users import *



### FOR GENERIC MODELS
# project_data = {
# 	"data" 			: generic_data,
# }

is_running		= fields.Boolean(
										description	= "is the project currently running ?",
										attribute		= "is_running",
										example			= False,
										required		= True,
										default			= False,
									)


# project_collaborator = {
# 	"user_oid" 			: oid,
# 	"auth_level"		: None,
# }

# project_datasets = {
# 	"dm_" 					: None,
# }

# project_recipes = {
# 	"on_datamodel" 	: None,
# 	"on_datasets" 	: None,
# 	"on_corr_dict" 	: None,
# }

# project_outputs = {

# }








# projects = [
# 	{
# 		"id" : fields.String("Oid of the project"),

# 		"datamodel"					: fields.String("id of the project"), 	# datamodel id in DB
# 		"datasets_inputs"		: [],																		# list of datasets_input ids in DB
# 		"corr_dicts"				: [],																		# list of corr_dict ids in DB
		
# 		"recipes" 					: {
# 			"on_datamodel" 	: {},
# 			"on_datasets"		: {},
# 			"on_corr_dict"	: {}, 
# 		},

# 		"dataset_output"	: fields.String("title of the project"),	# unique dataset output id in DB

# 		"exports"					: [],						# description of exports settings
		
# 	}
# ]
