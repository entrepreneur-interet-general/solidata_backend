# -*- encoding: utf-8 -*-

"""
endpoint_prj.py  
- provides the API endpoints for consuming and producing
	REST requests and responses
"""

from solidata_api.api import *

log.debug(">>> api_projects ... creating api endpoints for PROJ_LIST")

### create namespace
ns = Namespace('list', description='Projects : request and list all projects')

### import models 
from solidata_api._models.models_project import * 
model_project_in		= Project_infos(ns).mod_complete_in
# model_project_out		= Project_infos(ns).mod_complete_out


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 

# cf : http://flask-jwt-extended.readthedocs.io/en/latest/refresh_tokens.html

### ROUTES
@ns.route('/')
class ProjectsList(Resource):

	# @api.marshal_with(project_model, envelope="projects_list")
	@jwt_required
	def get(self):
		"""
		list of all projects in db
		"""
		return {
					"msg" : "nananana"
				}