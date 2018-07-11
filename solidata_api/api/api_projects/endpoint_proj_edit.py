# -*- encoding: utf-8 -*-

"""
endpoint_proj_edit.py  
- provides the API endpoints for consuming and producing
	REST requests and responses
"""

from solidata_api.api import *

log.debug(">>> api_projects ... creating api endpoints for PROJ_EDIT")

### create namespace
ns = Namespace('edit', description='Edit a project : ... ')

### import models 
from solidata_api._models.models_projects import * 
model_project_in		= Project_infos(ns).mod_complete_in
model_project_out		= Project_infos(ns).mod_complete_out


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 

# cf : http://flask-jwt-extended.readthedocs.io/en/latest/refresh_tokens.html



@ns.route('/<string:project_oid>')
@ns.param('project_oid', 'The project unique identifier')
class Projects(Resource):
	"""

	"""
	
	@jwt_required
	def get(self):
		"""
		list of all projects in db
		"""
		return {
							"msg" : "nananana"
					}


	@jwt_required
	def put(self):
		"""
		Update a new projects in db
		"""
		return {
							"msg" : "nananana"
					}
	

	@jwt_required
	def delete(self):
		"""
		delete a project in db
		"""
		return {
							"msg" : "nananana"
					}