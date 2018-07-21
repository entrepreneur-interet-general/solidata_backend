# -*- encoding: utf-8 -*-

"""
endpoint_prj_create.py  
- provides the API endpoints for consuming and producing
	REST requests and responses
"""

from solidata_api.api import *

log.debug(">>> api_projects ... creating api endpoints for PROJ_CREATE")

### create namespace
ns = Namespace('create', description='Projects : request and list all projects')

### import models 
from solidata_api._models.models_project import * 
model_project_in		= Project_infos(ns).mod_complete_in
# model_project_out		= Project_infos(ns).mod_complete_out


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 

# cf : http://flask-jwt-extended.readthedocs.io/en/latest/refresh_tokens.html


### TO DO 

### ROUTES
@ns.route('/')
class ProjectCreate(Resource):

	# @api.marshal_with(project_model, envelope="projects_list")
	@jwt_required
	@ns.expect(model_project_in)
	def post(self):
		"""
		Create a new project in db
		"""
		return {
							"msg" : "nananana"
					}