# -*- encoding: utf-8 -*-

"""
_models/models_projects.py  
- provides the models for all api routes
"""

from log_config import log, pformat

log.debug("... loading models_projects.py ...")


from flask_restplus import fields

### import data serializers
from solidata_api._serializers.schema_logs			import *  
from solidata_api._serializers.schema_generic		import *  
from solidata_api._serializers.schema_projects	import *  

### import generic models functions
from solidata_api._models.models_generic import * 

### create models from serializers
# nested models : https://github.com/noirbizarre/flask-restplus/issues/8
# model_user_infos 	= ns.model( "User model", user_infos) #, mask="{name,surname,email}" )



class Dsi_infos : 
	"""
	Model to display / marshal 
	specific projects's infos
	"""

	def __init__(self, ns_) :
		
		### SELF MODULES
		self.basic_infos 			= create_model_basic_infos(ns_, model_name="Dsi_infos")
		self.public_auth			= create_model_public_auth(ns_, model_name="Dsi_public_auth")
		self.log						 	= create_model_log(ns_, 				model_name="Dsi_log",					include_is_running=True, include_is_loaded=True )
		self.modif_log				= create_model_modif_log(ns_, 	model_name="Dsi_modif_log")
		self.specs						= create_model_specs(ns_,				model_name="Dsi_specs", 			include_src_link=True)
		self.team 						= create_model_team(ns_,				model_name="Dsi_team")

		self.uses							= create_uses(ns_,							model_name="Dsi_uses", 				schema_list=["usr","prj"])
		self.datasets 				= create_model_datasets(ns_, 		model_name="Dsi_datasets", 		schema_list=["dsr","tag"])

		### IN / complete data to enter in DB
		self.mod_complete_in 	= ns_.model('Project_in', {

				'infos' 			: self.basic_infos,
				'public_auth' : self.public_auth,
				'specs'				: self.specs , 
				'log'					: self.log , 
				'modif_log'		: self.modif_log , 

				### uses of the document
				'uses'				: self.uses,
				
				### team and edition levels
				'team'			: self.team ,

				### datasets 
				'datasets'	: self.datasets,

		})


		### IN / complete data to enter in DB
		self.mod_minimum 	= ns_.model('Project_minimum', {

				'infos' 			: self.basic_infos,
				'public_auth' : self.public_auth,

		})

	@property
	def model_complete_in(self): 
		return self.mod_complete_in


	@property
	def model_minimum(self): 
		return self.mod_minimum

