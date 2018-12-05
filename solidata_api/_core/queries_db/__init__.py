# -*- encoding: utf-8 -*-

"""
_core/queries_db/__init__.py  
"""

from log_config import log, pformat
print()
log.debug(">>> _core.queries_db.__init__.py ..." )
log.debug(">>> queries_db ... loading mongodb collections as global variables")

from flask import current_app as app

from solidata_api.application import mongo

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### GLOBAL VARIABLES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

### declaring collections as app variables

mongo_tags 					= mongo.db[ app.config["MONGO_COLL_TAGS"] ]
mongo_users 				= mongo.db[ app.config["MONGO_COLL_USERS"] ]
mongo_projects 				= mongo.db[ app.config["MONGO_COLL_PROJECTS"] ]
mongo_datamodels_templates 	= mongo.db[ app.config["MONGO_COLL_DATAMODELS_TEMPLATES"] ]
mongo_datamodels_fields 	= mongo.db[ app.config["MONGO_COLL_DATAMODELS_FIELDS"] ]
# mongo_connectors	 		= mongo.db[ app.config["MONGO_COLL_CONNECTORS"] ]
mongo_datasets_inputs 		= mongo.db[ app.config["MONGO_COLL_DATASETS_INPUTS"] ]
mongo_datasets_raws 		= mongo.db[ app.config["MONGO_COLL_DATASETS_RAWS"] ]
mongo_recipes 				= mongo.db[ app.config["MONGO_COLL_RECIPES"] ]
# mongo_corr_dicts 			= mongo.db[ app.config["MONGO_COLL_CORR_DICTS"] ]
mongo_datasets_outputs 		= mongo.db[ app.config["MONGO_COLL_DATASETS_OUTPUTS"] ]

mongo_licences 				= mongo.db[ app.config["MONGO_COLL_LICENCES"] ]
mongo_jwt_blacklist 		= mongo.db[ app.config["MONGO_COLL_JWT_BLACKLIST"] ]



db_dict = {
					"mongo_tags"					: mongo_tags,
					"mongo_users"					: mongo_users,
					"mongo_projects"				: mongo_projects,
					"mongo_datamodels_templates"	: mongo_datamodels_templates,
					"mongo_datamodels_fields"		: mongo_datamodels_fields,
					# "mongo_connectors"			: mongo_connectors,
					"mongo_datasets_inputs"			: mongo_datasets_inputs,
					"mongo_datasets_raws"			: mongo_datasets_raws,
					"mongo_recipes"					: mongo_recipes,
					# "mongo_corr_dicts"			: mongo_corr_dicts,

					"mongo_datasets_outputs"		: mongo_datasets_outputs,

					"mongo_licences"				: mongo_licences,
					"mongo_jwt_blacklist"			: mongo_jwt_blacklist,
			}
db_dict_by_type = {
					"tag"				: mongo_tags,
					"usr"				: mongo_users,
					"prj"				: mongo_projects,
					"dmt"				: mongo_datamodels_templates,
					"dmf"				: mongo_datamodels_fields,
					"dsi"				: mongo_datasets_inputs,
					"dsr"				: mongo_datasets_raws,
					"rec"				: mongo_recipes,

					"dso"				: mongo_datasets_outputs,

					"lic"				: mongo_licences,
					"jwt_blacklist"		: mongo_jwt_blacklist,
			}

def select_collection(coll_name):
	coll = db_dict[coll_name]
	return coll


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### SERIALIZERS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
class Marshaller :

	def __init__( self, ns, models ):
		
		self.ns 					= ns
		self.model_doc_out 			= models["model_doc_out"]
		self.model_doc_guest_out 	= models["model_doc_guest_out"]
		self.model_doc_min		 	= models["model_doc_min"]

		self.results_list			= None 

	def marshal_as_complete (self, results_list ) :

		ns 					= self.ns
		self.results_list 	= results_list
		log.debug('results_list : \n%s', pformat(results_list[:1]) )  
		
		@ns.marshal_with(self.model_doc_out)
		def get_results():
			return results_list
		return get_results()

	def marshal_as_guest (self, results_list ) :
	
		ns 					= self.ns
		self.results_list 	= results_list
		log.debug('results_list : \n%s', pformat(results_list) )  
		
		@ns.marshal_with(self.model_doc_guest_out)
		def get_results():
			return results_list
		return get_results()

	def marshal_as_min (self, results_list ) :
	
		ns 					= self.ns
		self.results_list 	= results_list
		log.debug('results_list : \n%s', pformat(results_list) )  
		
		@ns.marshal_with(self.model_doc_min)
		def get_results():
			return results_list
		return get_results()


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### FINAL IMPORTS FOR QUERIES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

from .query_doc import *
from .query_list import *
from .query_delete import *
from .query_update import *

print()




"""
RESPONSE CODES 
cf : https://restfulapi.net/http-status-codes/

	200 (OK)
	201 (Created)
	202 (Accepted)
	204 (No Content)
	301 (Moved Permanently)
	302 (Found)
	303 (See Other)
	304 (Not Modified)
	307 (Temporary Redirect)
	400 (Bad Request)
	401 (Unauthorized)
	403 (Forbidden)
	404 (Not Found)
	405 (Method Not Allowed)
	406 (Not Acceptable)
	412 (Precondition Failed)
	415 (Unsupported Media Type)
	500 (Internal Server Error)
	501 (Not Implemented)

"""