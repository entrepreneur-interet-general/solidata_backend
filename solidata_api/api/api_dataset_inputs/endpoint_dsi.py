# -*- encoding: utf-8 -*-

"""
endpoint_dsi.py  
- provides the API endpoints for consuming and producing
	REST requests and responses
"""

from solidata_api.api import *

log.debug(">>> api_projects ... creating api endpoints for DSI_LIST")

### create namespace
ns = Namespace('list', description='Dataset inputs : request and list all dataset inputs')

### import models 
from solidata_api._models.models_dataset_input import * 
model_dsi_in		= Dsi_infos(ns).mod_complete_in


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 

# cf : http://flask-jwt-extended.readthedocs.io/en/latest/refresh_tokens.html

### ROUTES
@ns.route('/')
class DsiList(Resource):

	# @api.marshal_with(project_model, envelope="projects_list")
	@jwt_required
	def get(self):
		"""
		list of all projects in db
		"""
    
		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )

		return {
							"msg" : "nananana"
					}