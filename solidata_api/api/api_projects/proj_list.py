# -*- encoding: utf-8 -*-

"""
proj_list.py
- provides the API endpoints for consuming and producing
	REST requests and responses
"""

from flask_restplus import Namespace, Resource, fields

from . import projects 

api = Namespace('projects_list', description='Projects list ')



### ROUTES
@api.route('/')
class ProjectsList(Resource):

	# @api.marshal_with(project_model, envelope="projects_list")
	def get(self):
		"""
		list of all projects in db
		"""
		return projects