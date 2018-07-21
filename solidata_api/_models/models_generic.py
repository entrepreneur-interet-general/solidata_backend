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
def create_model_basic_infos(ns_,	model_name 		= "Basic_infos",
																	schema				= doc_basics,
																	is_user_infos	= False, 
																	include_tags 	= True,
														) : 
	""" 
	"""

	schema = doc_basics

	if is_user_infos == True : 
		schema = user_basics 

	if include_tags == True :
		schema["tags_list"] = tags_list

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
				'email'			: email,
				'edit_auth'	: edit_auth,
				'added_at'  : added_at,
				'added_by'  : added_by,
			})
		)

	collaborators = fields.List( 
		collaborator,
		description = "List of {}s on this document".format(model_name), 
		default 		= [] 
	) 

	return collaborators



### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### MODEL / professional infos 
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
def create_professional_infos(ns_, model_name="Structures"):
		
	"""
	"""
	
	structure_infos = fields.Nested( 
			ns_.model( model_name, user_struct )
		)

	structures_list = fields.List( 
		structure_infos,
		description = "Structure informations", 
		default 		= [] 
	) 

	return structures_list


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### MODEL / USES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
def create_uses(ns_, 	model_name			= "Uses", 
											include_used_as = False,
											used_as					= "tax",
											schema_list			= ["prj", "dmt", "dmf", "dsi", "usr","rec"], 
							):
		
	"""
	"""
	
	uses_dict = {}

	for schema in schema_list : 

		doc_uses 		= {
			"used_by" : used_by,
			"used_at"	: used_at,
		}

		if include_used_as == True and schema == "prj" :
			doc_uses["used_as"] = used_as

		uses_infos = fields.Nested( 
				ns_.model( "Used_by_"+schema, doc_uses )
			)

		uses_list = fields.List( 
			uses_infos,
			description = "Uses informations", 
			default 		= [] 
		) 
	
		uses_dict["by_"+schema] = uses_list

	uses = fields.Nested( 
			ns_.model( model_name, uses_dict )
		)

	return uses


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
					schema+"_oid"	: oid_dict[schema]["field"],
					'added_at'  	: added_at,
					'added_by'  	: added_by,
				}
		
		if include_fav == True : 
			model_dataset["is_fav"] = is_fav
		
		dataset		= fields.Nested(
				ns_.model( schema.title()+"_ref", model_dataset )
			)

		dataset_list = fields.List( 
			dataset,
			description = "List of {}s on this document".format(oid_dict[schema]["fullname"]), 
			default 		= [] 
		) 

		datasets_dict[schema+"_list"] = dataset_list

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
### MODEL / MODIFICATIONS LOG
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
def create_model_log(ns_, model_name 								= "Log", 
													include_counts						= False, 
													counts_name								= "counts",
													include_is_running				=	False,
													include_is_loaded					=	False,
													include_src_link					= False,
													include_is_linked_to_dmt	= False,
										) :

	""" 
	"""

	log_base = {
				'created_at'		: created_at,
				'created_by'		: created_by,
			}

	if include_counts == True :
  		log_base[ counts_name ] = count

	if include_is_running == True :
  		log_base[ "is_running" ] = is_running

	if include_is_loaded == True :
  		log_base[ "is_loaded" ] = is_loaded

	### create the log
	logs = fields.Nested(
									ns_.model( model_name, log_base ),
									description = "{}s concerning this document".format(model_name), 
					)

	return logs



### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### MODEL / SPECS 
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
def create_model_specs(ns_, model_name 								= "Specs", 
														include_src_link					= False,
														include_inherit_from_dmt	= False,
														include_child_of_tag			= False,
													) :
	""" 
	"""
	
	specs_base = {
				'doc_type'			: doc_type,
			}
	
	if include_src_link == True : 
		specs_base['src_link']	= src_link
		specs_base['src_type']	= src_type

	if include_inherit_from_dmt == True :
		pass

	if include_child_of_tag == True :
  		pass

	### compile the document's log
	doc_specs = fields.Nested( 
			ns_.model( model_name, specs_base )
		)

	return doc_specs