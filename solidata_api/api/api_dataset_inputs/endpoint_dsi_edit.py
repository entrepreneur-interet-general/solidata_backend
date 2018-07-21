# -*- encoding: utf-8 -*-

"""
endpoint_proj_edit.py  
- provides the API endpoints for consuming and producing
	REST requests and responses
"""

from solidata_api.api import *

log.debug(">>> api_projects ... creating api endpoints for DSI_EDIT")

### create namespace
ns = Namespace('edit', description='Edit a dsi : ... ')

### import models 
from solidata_api._models.models_dataset_input import * 
model_dsi_in		= Dsi_infos(ns).mod_complete_in


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 

# cf : http://flask-jwt-extended.readthedocs.io/en/latest/refresh_tokens.html



@ns.route('/<string:dsi_oid>')
@ns.param('dsi_oid', 'The dsi unique identifier')
class DsiEdit(Resource):
	"""

	"""
	
	@jwt_required
	@ns.expect(model_dsi_in)
	def get(self):
		"""
		list of all dsi in db
		"""

		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )

		return {
							"msg" : "nananana"
					}


	@jwt_required
	def put(self):
		"""
		Update a new dsi in db
		"""

		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )

		return {
							"msg" : "nananana"
					}
	

	@jwt_required
	def delete(self):
		"""
		delete a dsi in db
		"""

		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )

		return {
							"msg" : "nananana"
					}