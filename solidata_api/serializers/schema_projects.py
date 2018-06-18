# -*- encoding: utf-8 -*-

"""
model_projects.py  
- provides the model for PROJECT definition in DB and Flask-Restplus
"""

from flask_restplus import fields


projects = [
	{
		"id" : fields.String("Oid of the project"),
		"proj_title"				: fields.String("title of the project"),
		"owner"							: fields.String("id of project's owner"),
		"collaborators"			: [],

		"datamodel"					: fields.String("id of the project"), 	# datamodel id in DB
		"datasets_inputs"		: [],																		# list of datasets_input ids in DB
		"corr_dicts"				: [],																		# list of corr_dict ids in DB
		
		"recipes" 					: {
			"on_datamodel" 	: {},
			"on_datasets"		: {},
			"on_corr_dict"	: {}, 
		},

		"dataset_output"	: fields.String("title of the project"),	# unique dataset output id in DB

		"exports"					: [],						# description of exports settings
		
	}
]


project_definition = {
	"name" 						: fields.String(attribute="name of the user"),
	"surname" 				: fields.String(attribute="surname of the user"),
	"email" 					: fields.String(attribute="email of the user"),
}