# -*- encoding: utf-8 -*-

"""
_models/models_dataset_raw.py  
"""

from log_config import log, pformat

log.debug("... loading models_dataset_raw.py ...")


from flask_restplus import fields

### import data serializers
from solidata_api._serializers.schema_logs import *  
from solidata_api._serializers.schema_generic import *  
# from solidata_api._serializers.schema_projects import *  

### import generic models functions
from solidata_api._models.models_generic import * 

### create models from serializers
# nested models : https://github.com/noirbizarre/flask-restplus/issues/8
# model_user_infos 	= ns.model( "User model", user_infos) #, mask="{name,surname,email}" )



class Dsr_infos : 
	"""
	Model to display / marshal 
	dataset raw
	"""

	def __init__(self, ns_) :
		
		### SELF MODULES
		self.basic_infos 			= create_model_basic_infos(ns_, model_name="Dsr_infos")
		self.public_auth			= create_model_public_auth(ns_, model_name="Dsr_public_auth")
		self.log						 	= create_model_log(ns_, 				model_name="Dsr_log" )
		self.modif_log				= create_model_modif_log(ns_, 	model_name="Dsr_modif_log")
		self.specs						= create_model_specs(ns_,				model_name="Dsr_specs")

		self.uses							= create_uses(ns_,							model_name="Dsr_uses", 			schema_list=["dsi","dso"])


		### IN / complete data to enter in DB
		self.mod_complete_in 	= ns_.model('Dsr_in', {

				'infos' 			: self.basic_infos,
				'public_auth' : self.public_auth,
				'log'					: self.log , 
				'modif_log'		: self.modif_log , 
				'specs'				: self.specs , 

				### uses of the document
				'uses'				: self.uses,

		})

	
	@property
	def model_complete_in(self): 
		return self.mod_complete_in




