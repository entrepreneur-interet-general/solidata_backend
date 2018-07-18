# -*- encoding: utf-8 -*-

"""
_core/queries_db/__init__.py  
- provides the MONGO QUERIES for 
	REST requests
"""

from log_config import log, pformat
print()
log.debug(">>> _core.queries_db.__init__.py ..." )
log.debug(">>> queries_db ... loading mongodb collections as global variables")

from flask import current_app as app

from solidata_api.application import mongo


### declaring collections as app variables

mongo_users 								= mongo.db[ app.config["MONGO_COLL_USERS"] ]
mongo_projects 							= mongo.db[ app.config["MONGO_COLL_PROJECTS"] ]
mongo_datamodels_templates 	= mongo.db[ app.config["MONGO_COLL_DATAMODELS_TEMPLATES"] ]
mongo_datamodels_fields 		= mongo.db[ app.config["MONGO_COLL_DATAMODELS_FIELDS"] ]
# mongo_connectors	 					= mongo.db[ app.config["MONGO_COLL_CONNECTORS"] ]
mongo_datasets_inputs 			= mongo.db[ app.config["MONGO_COLL_DATASETS_INPUTS"] ]
mongo_recipes 							= mongo.db[ app.config["MONGO_COLL_RECIPES"] ]
# mongo_corr_dicts 						= mongo.db[ app.config["MONGO_COLL_CORR_DICTS"] ]
mongo_datasets_outputs 			= mongo.db[ app.config["MONGO_COLL_DATASETS_OUTPUTS"] ]

mongo_jwt_blacklist 				= mongo.db[ app.config["MONGO_COLL_JWT_BLACKLIST"] ]


# mongo_licences 							= mongo.db[ app.config["MONGO_COLL_LICENCES"] ]


db = {
					"mongo_users"									: mongo_users,
					"mongo_projects"							: mongo_projects,
					"mongo_datamodels_templates"	: mongo_datamodels_templates,
					"mongo_datamodels_fields"			: mongo_datamodels_fields,
					# "mongo_connectors"						: mongo_connectors,
					"mongo_datasets_inputs"				: mongo_datasets_inputs,
					"mongo_recipes"								: mongo_recipes,
					# "mongo_corr_dicts"						: mongo_corr_dicts,

					"mongo_datasets_outputs"			: mongo_datasets_outputs,
					# "mongo_licences"							: mongo_licences,
					"mongo_jwt_blacklist"					: mongo_jwt_blacklist,
			}

def select_collection(coll_name):
	coll = db[coll_name]
	return coll


