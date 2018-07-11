# -*- encoding: utf-8 -*-

"""
_models/models_projects.py  
- provides the models for all api routes
"""

from log_config import log, pformat

log.debug("... loading models_projects.py ...")


from flask_restplus import fields

### import data serializers
from solidata_api._serializers.schema_logs import *  
from solidata_api._serializers.schema_generic import *  
from solidata_api._serializers.schema_projects import *  


### create models from serializers
# nested models : https://github.com/noirbizarre/flask-restplus/issues/8
# model_user_infos 	= ns.model( "User model", user_infos) #, mask="{name,surname,email}" )



class Project_infos : 
	"""
	Model to display / marshal 
	specific projects's infos
	"""

	def __init__(self, ns_) :
		
    ### SELF MODULES
		self.basic_infos		= fields.Nested(
					ns_.model('Project_public_data', project_basics )
				)

		self.modifications 	=  fields.List(
					fields.Nested(
							ns_.model('Modifications', 			modification )
					),
					default			= [] 
		)
		self.project_log 			= fields.Nested( 
			ns_.model('Project_log', {
				'created_at'		: created_at,
				# 'login_count'		: count,
				'modified_log'	: self.modifications
			})
		)


		### IN / complete data to enter in DB
		self.mod_complete_in  = ns_.model('Project_in', {

				'infos' 	: self.basic_infos,
				'log' 		: self.project_log , 


		})

		### OUT / complete data to enter in DB
		self.mod_complete_out  = ns_.model('Project_out', {

				'infos' 	: self.basic_infos,
				'log' 		: self.project_log , 


			})


	@property
	def model_complete_in(self): 
		return self.mod_complete_in

	@property
	def model_complete_out(self): 
		return self.mod_complete_out


