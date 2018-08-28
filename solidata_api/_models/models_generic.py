# -*- encoding: utf-8 -*-

"""
_models/models_generic.py  
- provides the models for all api routes
"""

from log_config import log, pformat

log.debug("... loading models_generic.py ...")


from flask_restplus import fields

### import data serializers
from solidata_api._serializers.schema_logs 		import *  
from solidata_api._serializers.schema_generic 	import *  
from solidata_api._serializers.schema_users 	import *  


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### MODEL / BASIC INFOS 
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
def create_model_basic_infos( 	ns_, 
								model_name 		= "Basic_infos",
								schema			= doc_basics,
								is_user_infos	= False, 
								need_licence	= False,
							) : 
	""" 
	Basic infos model
	"""

	# schema = doc_basics

	if is_user_infos == True : 
		schema = user_basics 
	
	if need_licence == True : 
		schema = doc_basics_licence 

	basic_infos		= fields.Nested(
		ns_.model( model_name , schema ),
		description = "basic infos about the document"
	)
	return basic_infos


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### MODEL / PUBLIC AUTH 
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
def create_model_public_auth(	ns_, 
								model_name = "Public_auth" 
							):
	
	"""
	Public auth model
	"""
	
	public_authorizations = fields.Nested( 
		ns_.model( model_name, public_auth ),
		description = "public authorization levels on this document"
	)

	return public_authorizations


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### MODEL / MULTILANGUAGE 
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
def create_model_translations(	ns_, 
								model_name = "Translations"
							):
	
	"""
	Translations model
	"""
	
	translation = fields.Nested( 
		ns_.model( model_name, {
			'locale'					: locale,
			'field_to_translate'	  	: field_to_translate,
			'translation'  				: text_translated,
		})
	)

	translations = fields.List( 
		translation,
		description = "List of {}s on this document".format(model_name), 
		default 		= [] 
	) 

	return translations


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### MODEL / TEAM 
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
def create_model_team(	ns_, 
						model_name = "Collaborator"
					):
	
	"""
	Team model
	"""
	
	collaborator = fields.Nested( 
		ns_.model( model_name, {
			'oid_usr'	: oid_usr,
			# 'email'		: email,
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
### MODEL / about the user
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
def create_model_profile(	ns_, 
							model_name = "User_profile" 
						):
	
	"""
	Profile of an user
	"""

	profile = fields.Nested( 
			ns_.model(model_name, usr_profile_ )
		)

	return profile


def create_model_auth(	ns_, 
						model_name = "User_authorizations",
						schema		= user_auth_in
					):
	
	"""
	Authorizations of an user
	"""

	auth = fields.Nested( 
			ns_.model(model_name, schema )
		)

	return auth


def create_professional_infos(	ns_, 
								model_name = "Structures"
							):
		
	"""
	Professional infos model	
	"""
	
	structure_infos = fields.Nested( 
		ns_.model( model_name, user_struct )
	)

	structures_list = fields.List( 
		structure_infos,
		description 	= "Structure informations", 
		default 		= [] 
	) 

	return structures_list


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### MODEL / USES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
def create_model_uses(	ns_, 	
					model_name		= "Uses", 
					include_used_as = False,
					used_as			= "tax",
					schema_list		= ["prj","dmt","dmf","dsi","dsr","usr","rec"], 
				):

	"""
	Uses model
	"""
	
	uses_dict = {}

	for schema in schema_list : 

		doc_uses 		= {
			"used_by" : used_by,
		}

		if include_used_as == True and schema == "prj" :
			doc_uses["used_as"] = used_as

		uses_dates = fields.List (
			# used_at ,
			at ,
			description = "Uses dates", 
			default 	= [] 
		)

		doc_uses["used_at"] = uses_dates

		uses_infos = fields.Nested( 
			ns_.model( "Used_by_"+schema, doc_uses )
		)

		uses_list = fields.List( 
			uses_infos,
			description = "Uses informations", 
			default 	= [] 
		) 
	
		uses_dict["by_"+schema] = uses_list

	uses = fields.Nested( 
		ns_.model( model_name, uses_dict )
	)

	return uses


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### MODEL / DATASETS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
def create_model_dataset(	ns_,		
							model_name				= "Datasets" ,
							include_fav				= False,
							include_dmf_open_level 	= False ,
							display_fullname 		= False ,
							schema					= "prj", 
						) : 
	"""
	Dataset model (one)
	"""
	
	model_dataset = {
					"oid_"+schema 	: oid_dict[schema]["field"],
					'added_at'		: added_at,
					'added_by'		: added_by,
					}
		
	if include_fav == True : 
		model_dataset["is_fav"] = is_fav

	if include_dmf_open_level == True and schema in ["dmf","dsr"] :
		model_dataset["open_level"] = open_level
	
	dataset		= fields.Nested(
		ns_.model( schema.title()+"_ref", model_dataset )
	)
	
	return dataset


def create_model_datasets(	ns_,	
							model_name				= "Datasets" ,
							include_fav				= False,
							include_dmf_open_level 	= False ,
							display_fullname 		= False ,
							schema_list				= ["prj","dmt","dmf","dsi","dsr","rec","dso","tag","func"], 
					) : 
	"""
	Datasets model (nested)
	"""

	datasets_dict = {}

	for schema in schema_list : 
	
		dataset = create_model_dataset(	ns_, 
										model_name				= model_name, 
										include_fav				= include_fav, 
										include_dmf_open_level	= include_dmf_open_level,
										display_fullname		= display_fullname,
										schema					= schema
									)

		dataset_list = fields.List( 
			dataset,
			description 	= "List of {}s on this document".format(oid_dict[schema]["fullname"]), 
			default 		= [] 
		) 

		datasets_dict[schema+"_list"] = dataset_list

	datasets = fields.Nested( 
		ns_.model( model_name, datasets_dict )
	)

	return datasets


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### MODEL / MAPPING
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
def create_model_mappings(	ns_,	
							model_name	= "Mapping" ,
							schema_list	= ["dsi_to_dmt", "rec_to_func", "rec_to_dmt"], 
						) : 
	"""
	Mapping model
	mapping the relation between a document and another
	"""

	mapping_dict = {}

	for schema in schema_list : 
		
		### TO DO
		
		model_mapping 				= mapping_oid_dict[schema]
		model_mapping['added_at'] 	= added_at
		model_mapping['added_by'] 	= added_by
		
		if schema == "dsi_to_dmf" : 
			model_mapping['visible_dmf_list'] = fields.List(
				oid_dmf,
				description = "visible dmf list"
			)

		mapping		= fields.Nested(
				ns_.model( schema.title(), model_mapping ),
				description = "mapping between {}".format(schema),
			)

		mapping_list = fields.List( 
			mapping,
			description = "List of {}s on this document".format(schema), 
			default 		= [] 
		) 

		mapping_dict[schema] = mapping_list

	mappings = fields.Nested( 
		ns_.model( model_name, mapping_dict )
	)

	return mappings


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### MODEL / MODIFICATIONS LOG
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
def create_model_modif_log(		ns_, 
								model_name 	= "Modification", 
								schema		= modification_full, 
							) :

	""" 
	Modif log model
	"""
	
	### compile the list of modifications
	modifications = fields.List(
		fields.Nested(
				ns_.model( model_name, schema )
		),
		description = "List of the {}s on this document".format(model_name), 
		default			= [] 
	)

	return modifications


def create_model_log(	ns_, 
						model_name 					= "Log", 
						include_counts				= False, 
						counts_name					= "counts",
						include_is_running			= False,
						include_is_loaded			= False,
						include_src_link			= False,
						include_is_linked_to_dmt	= False,
					) :

	""" 
	Log model
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

	### compile the log
	logs = fields.Nested(
		ns_.model( model_name, log_base ),
		description = "{}s concerning this document".format(model_name), 
	)

	return logs


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### MODEL / SPECS 
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
def create_model_specs(	ns_, 
						model_name 					= "Specs", 
						include_src_link			= False,
						include_inherit_from_dmt	= False,
						include_child_of_tag		= False,
					) :
	"""
	Specs model 
	"""
	
	specs_base = {
					'doc_type'	: doc_type,
				}

	if include_src_link == True : 
		specs_base['src_link']		= src_link
		specs_base['src_type']		= src_type

	### TO DO 
	if include_inherit_from_dmt == True :
		pass

	if include_child_of_tag == True :
		pass

	### compile the document's specs
	doc_specs = fields.Nested( 
		ns_.model( model_name, specs_base )
	)

	return doc_specs


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### MODEL / DATA RAW  
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
def create_model_data_raw( 	ns_, 
							model_name 		= "Data_raw",
							schema			= "tag",
						) : 
	""" 
	data_raw_fields model
	"""

	if schema in ["dmf", "tag"] : 

		if schema == "tag" : 
			schema_	= f_basics_tag

		if schema == "dmf" : 
			schema_	= f_basics_dmf

		data_raw_fields		= fields.Nested(
			ns_.model( model_name , schema_ ),
			description = "Data_raw"
		)

	if schema == "dsr" : 
		data_raw_fields = fields.List(
			RawData ,	
			description = "List of the {}s on this document".format(model_name), 
			default		= [] 
		)

	
	return data_raw_fields

