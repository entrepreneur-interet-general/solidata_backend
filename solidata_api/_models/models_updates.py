# -*- encoding: utf-8 -*-

"""
_models/models_updates.py  
"""

from log_config import log, pformat

log.debug("... loading models_tag.py ...")


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


class Update_infos : 
	"""
	Model to display / marshal 
	updates
	"""

	def __init__(self, ns_, document_type ) :

		### SELF MODULES
		self.generic_update = create_model_field_update(	
			ns_, model_name=document_type+"_update"
		)


	@property
	def model_update_generic(self): 
		return self.generic_update




