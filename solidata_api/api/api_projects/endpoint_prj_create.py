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
mod_prj							= Project_infos(ns)
# model_project_in		= Project_infos(ns).model_complete_in 
model_project_in		= mod_prj.mod_complete_in
# model_project_min		= Project_infos(ns).model_min 
model_project_min		= mod_prj.mod_minimum


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
	# @jwt_required
	@guest_required
	# @ns.expect(model_project_in)
	# @ns.expect(model_project_min)
	def post(self):
		"""
		Create a new project in db
		"""

		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )
		log.debug ("payload : \n{}".format(pformat(ns.payload)))

		### get data from form
		new_prj_infos = ns.payload

		### marshall infos with prj complete model
		# new_prj 	= marshal( new_prj_infos , model_project_in)

		### save new_prj in db
		# mongo_projects.insert(new_prj)


		
		return {
							"msg" : "nananana",

					}