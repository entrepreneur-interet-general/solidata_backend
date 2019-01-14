# -*- encoding: utf-8 -*-

"""
_models/models_solidify.py  
"""

from log_config import log, pformat

log.debug("... loading models_solidify.py ...")


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


class Solidify_run_params : 
	"""
	Model to display / marshal 
	solidify run params
	"""

	def __init__(self, ns_, document_type ) :

		### SELF MODULES
		self.generic_solidify = create_model_solidify_run_params(	
			ns_, model_name=document_type+"_solidify"
		)

	@property
	def model_solidify_generic(self): 
		return self.generic_solidify

