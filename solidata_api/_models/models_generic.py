# -*- encoding: utf-8 -*-

"""
_models/models_generic.py  
- provides the models for all api routes
"""

from log_config import log, pformat

log.debug("... loading models_generic.py ...")


from flask_restplus import fields

### import data serializers
from solidata_api._serializers.schema_logs import *  
from solidata_api._serializers.schema_generic import *  
from solidata_api._serializers.schema_projects import *  



### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### MODEL / BASIC INFOS 
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
def create_model_basic_infos(ns_,	model_name,
																	schema				= doc_basics,
																	is_user_infos	= False, 
														) : 
	""" 
	"""
	
	schema = doc_basics

	if is_user_infos == True : 
		schema = user_basics 

	basic_infos		= fields.Nested(
					ns_.model( model_name , schema )
				)
	return basic_infos



### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### MODEL / TEAM 
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
def create_model_team(ns_, model_name="Collaborator"):
	
	"""
	"""
	
	collaborator = fields.Nested( 
			ns_.model( model_name, {
				'oid_usr'		: oid_usr,
				'edit_auth'	: edit_auth,
				'added_at'  : added_at,
				'added_by'  : oid_usr,
			})
		)

	collaborators = fields.List( 
		collaborator,
		description = "List of {}s on this document".format(model_name), 
		default 		= [] 
	) 

	return collaborators



### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### MODEL / DATASETS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
def create_model_datasets(ns_,	model_name				= "Datasets" ,
																include_fav				=	False,
																display_fullname 	= False ,
																schema_list				= ["prj", "dmt", "dmf", "dsi", "rec", "dso"], 
														) : 
	"""
	"""

	datasets_dict = {}

	for schema in schema_list : 
		
		model_dataset = {
					'oid_usr'		: oid_dict[schema]["field"],
					'added_at'  : added_at,
					'added_by'  : oid_usr,
				}
		
		if include_fav == True : 
			model_dataset["is_fav"] = is_fav
		
		dataset		= fields.Nested(
				ns_.model( schema.title(), model_dataset )
			)

		dataset_list = fields.List( 
			dataset,
			description = "List of {}s on this document".format(oid_dict[schema]["fullname"]), 
			default 		= [] 
		) 

		datasets_dict[schema] = dataset_list

	datasets = fields.Nested( 
			ns_.model( model_name, datasets_dict )
		)

	return datasets



### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### MODEL / MODIFICATIONS LOG
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
def create_model_modif_log(ns_, model_name = "Modification", 
																schema			= modification_full, 
													) :

	""" 
	"""
	
	### create the list of modifications
	modifications = fields.List(
										fields.Nested(
												ns_.model( model_name, schema )
										),
										description = "List of the {}s on this document".format(model_name), 
										default			= [] 
							)

	return modifications


	### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### MODEL / SPECS 
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
def create_model_specs(ns_, model_name 					= "Specs", 
														include_counts			= False, 
														counts_name					= "counts",
														include_created_by	= True,
														include_is_running	=	False,
														include_is_loaded		=	False,
													) :
	""" 
	"""
	
	specs_base = {
				'created_at'		: created_at,
			}
	
	if include_created_by == True : 
		specs_base['created_by']	= oid_usr

	if include_counts == True :
		specs_base[ counts_name ] = count

	if include_is_running == True :
		specs_base[ "is_running" ] = is_running

	### compile the document's log
	doc_specs = fields.Nested( 
			ns_.model( model_name, specs_base )
		)

	return doc_specs