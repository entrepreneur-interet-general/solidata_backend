# -*- encoding: utf-8 -*-

"""
api_projects/__init__.py
- provides the API endpoints for consuming and producing
	REST requests and responses
"""

from flask import Blueprint
from flask_restplus import Api

### create blueprint and api wrapper
blueprint = Blueprint( 'api_projects', __name__)
api = Api( 	blueprint,
						title="SOLIDATA - PROJECTS API",
						version="0.1",
						description="create, list, delete, edit... projects",
						doc='/documentation',
						default='projects_list'
					)

### import data schemas
### TO DO 

### mocking a project definition
projects = [
	{
		"id" : 1,
		"proj_title"				: "my project",
		"owner"							: "email",
		"collaborators"			: [],

		"datamodel"					: "dfghjkl", 	# datamodel id in DB
		"datasets_inputs"		: [],					# list of datasets_input ids in DB
		"corr_dicts"				: [],					# list of corr_dict ids in DB
		
		"recipes" 					: {
			"on_datamodel" 	: {},
			"on_datasets"		: {},
			"on_corr_dict"	: {}, 
		},

		"dataset_output"	: "",						# unique dataset output id in DB

		"exports"					: [],						# description of exports settings
		
	}
]


### import api namespaces
from .proj_list import api as api_proj_list

### add namespaces to api wrapper
api.add_namespace(api_proj_list)