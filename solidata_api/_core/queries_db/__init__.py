# -*- encoding: utf-8 -*-

"""
query/__init__.py.py  
- provides the MONGO QUERIES for 
	REST requests
"""

from log_config import log, pformat
log.debug(">>> queries_db ... loading mongodb collections as global variables")

from flask import current_app as app

from solidata_api.application import mongo


### declaring collections as app variables

mongo_users 						= mongo.db[ app.config["MONGO_COLL_USERS"] ]
mongo_licences 					= mongo.db[ app.config["MONGO_COLL_LICENCES"] ]
mongo_projects 					= mongo.db[ app.config["MONGO_COLL_PROJECTS"] ]
mongo_datamodels 				= mongo.db[ app.config["MONGO_COLL_DATAMODELS"] ]
mongo_datamodels_fields = mongo.db[ app.config["MONGO_COLL_DATAMODELS_FIELDS"] ]
mongo_connectors	 			= mongo.db[ app.config["MONGO_COLL_CONNECTORS"] ]
mongo_datasets_inputs 	= mongo.db[ app.config["MONGO_COLL_DATASETS_INPUTS"] ]
mongo_datasets_outputs 	= mongo.db[ app.config["MONGO_COLL_DATASETS_OUTPUTS"] ]
mongo_recipes 					= mongo.db[ app.config["MONGO_COLL_RECIPES"] ]
mongo_corr_dicts 				= mongo.db[ app.config["MONGO_COLL_CORR_DICTS"] ]

db = {
					"mongo_users"							: mongo_users,
					"mongo_licences"					: mongo_licences,
					"mongo_projects"					: mongo_projects,
					"mongo_datamodels"				: mongo_datamodels,
					"mongo_datamodels_fields"	: mongo_datamodels_fields,
					"mongo_connectors"				: mongo_connectors,
					"mongo_datasets_inputs"		: mongo_datasets_inputs,
					"mongo_datasets_outputs"	: mongo_datasets_outputs,
					"mongo_recipes"						: mongo_recipes,
					"mongo_corr_dicts"				: mongo_corr_dicts,
			}

def select_collection(coll_name):
	coll = db[coll_name]
	return coll


