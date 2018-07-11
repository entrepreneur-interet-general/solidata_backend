# -*- encoding: utf-8 -*-

"""
model_projects.py  
- provides the model for PROJECT definition in DB and Flask-Restplus
"""

from flask_restplus import fields

from .schema_generic import *
from .schema_logs import *
from .schema_users import *




### FOR GENERIC MODELS
project_data = {
	"data" 			: generic_data,
}

project_basics = {
	"title" 				: title,
	"owner" 				: oid,
	"dso"						: oid
}

project_team = {
	
}

project_datasets = {
	"dm_" 					: None,
}

project_recipes = {
	"on_datamodel" 	: None,
	"on_datasets" 	: None,
	"on_corr_dict" 	: None,
}

project_outputs = {

}








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
