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



### MODEL / BASIC INFOS 
def create_model_basic_infos(ns_,	model_name,
																	schema=doc_basics, 
														) : 
				
	basic_infos		= fields.Nested(
					ns_.model( model_name , doc_basics )
				)
	return basic_infos



### MODEL TEAM 
def create_model_team(ns_, model_name="Collaborator"):
		
	collaborator = fields.Nested( 
			ns_.model( model_name, {
				'user_oid'	: oid,
				'auth_edit'	: edit_auth
			})
		)

	collaborators = fields.List( 
		collaborator,
		description = "List of collaborators on this document", 
		default 		= [] 
		) 

	return collaborators


### MODIFICATIONS LOG
def create_model_modif_log(ns_, model_name, 
																schema							= modification_full, 
																include_counts			= False, 
																counts_name					= "counts",
																include_created_by	= True,
																include_is_running	=	False,
													) :
	
	### create the list of modifications
	modifications = fields.List(
										fields.Nested(
												ns_.model('Modifications', schema )
										),
										description = "List of the modifications on this document", 
										default			= [] 
							)
	
	log_base = {
				'created_at'		: created_at,
				'modified_log'	: modifications
			}
	
	if include_created_by == True : 
		log_base['created_by']	= oid

	if include_counts == True :
		log_base[ counts_name ] = count

	if include_is_running == True :
		log_base[ "is_running" ] = is_running

	### compile the document's log
	doc_log = fields.Nested( 
			ns_.model( model_name, log_base )
		)

	return doc_log