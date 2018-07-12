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

### import generic models functions
from solidata_api._models.models_generic import *

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
		# self.basic_infos		= fields.Nested(
		# 			ns_.model('Project_infos', doc_basics )
		# 		)
		self.basic_infos = create_model_basic_infos(ns_, "Project_infos")

		# self.modifications 	=  fields.List(
		# 			fields.Nested(
		# 					ns_.model('Modifications_by', 			modification_full )
		# 			),
		# 			default			= [] 
		# )
		# self.project_log 			= fields.Nested( 
		# 	ns_.model('Project_log', {
		# 		'created_at'		: created_at,
		# 		'modified_log'	: self.modifications
		# 	})
		# )

		self.project_log = create_model_modif_log(ns_, "Project_log", include_is_running=True)

		# self.collaborator = fields.Nested( 
		# 	ns_.model('Collaborator', {
		# 		'user_oid'	: oid,
		# 		'auth_edit'	: edit_auth
		# 	})
		# )
		self.collaborators = create_model_team(ns_)


		### IN / complete data to enter in DB
		self.mod_complete_in  = ns_.model('Project_in', {

				'infos' 	: self.basic_infos,
				'log' 		: self.project_log , 

				### team and edition levels
				# 'proj_team'		: fields.List(self.collaborator) ,
				'proj_team'		: self.collaborators ,

				### datasets 
				'dm_t' 		: oid,
				'ds_i' 		: fields.List(oid),
				'dc_' 		: fields.List(oid),
				'rec_' 		: fields.List(oid),
		})

		### OUT / complete data to enter in DB
		# self.mod_complete_out  = ns_.model('Project_out', {

		# 		'infos' 	: self.basic_infos,
		# 		'log' 		: self.project_log , 
				
		# 		### team and edition levels
		# 		# 'project_team'					: fields.List(self.collaborator) ,
		# 		'proj_team'		: self.collaborators ,

		# 		### datasets 
		# 		'datamodel' 						: oid,
		# 		'dataset_inputs' 				: fields.List(oid),
		# 		'correspondance_dicts' 	: fields.List(oid),
		# 		'recipes' 							: fields.List(oid),

		# 	})


	@property
	def model_complete_in(self): 
		return self.mod_complete_in

	@property
	def model_complete_out(self): 
		return self.mod_complete_out


