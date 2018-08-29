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
mod_prj					= Prj_infos(ns)
model_project_out		= mod_prj.mod_complete_out
model_project_min		= mod_prj.model_minimum



### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### SERIALIZERS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

@ns.marshal_with(model_project_out)
def marshal_projects(results_list):
	return results_list

@ns.marshal_with(model_project_min)
def marshal_projects_min(results_list):
	return results_list


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 


@ns.route('/')
class Prj_List(Resource):

	### TO DO  : pagination arguments
	@ns.doc('prj_list')
	@ns.expect(pagination_arguments)
	@ns.expect(query_arguments)
	@jwt_optional
	# @anonymous_required
	# @ns.marshal_with(model_project_out, envelope="data")
	def get(self):
		"""
		list of all projects in db

		>
			--- needs   : nothing - optionnal args : pagination, list of oid_prj, list of tags, query
			>>> returns : projects data as a list

		"""

		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )

		### DEBUG check
		log.debug ("payload : \n{}".format(pformat(ns.payload)))

		### check client identity and claims
		claims 			= get_jwt_claims() 
		log.debug("claims : \n %s", pformat(claims) )

		user_id 		= get_jwt_identity() ### get the oid as str
		if user_id : 
			log.debug('user_identity from jwt : \n%s', user_identity["email"].__dict__ )  
			log.debug('user_identity["email"] from jwt : \n%s', user_identity["email"] )  
			# user_id 		= claims["_id"]
			user_oid		= ObjectId(user_id)
			log.debug('user_oid : %s', user_oid )  
			user_role 		= claims["auth"]["role"]

		### get pagination arguments
		page_args		= pagination_arguments.parse_args(request)
		log.debug('page_args : \n%s', pformat(page_args) )  
		page 			= page_args.get('page', 1)
		per_page 		= page_args.get('per_page', 10)

		### get query arguments
		query_args		= query_arguments.parse_args(request)
		log.debug('query_args : \n%s', pformat(query_args) )  



		### retrieve from db
		cursor 		= mongo_projects.find({})
		projects	= list(cursor)
		log.debug( "projects : \n %s", pformat(projects) )

		### TO DO 
		### filter results given user's role



		### marshal out results
		projects_out = marshal_projects( projects )
		log.debug( "projects_out : \n %s", pformat(projects_out) )


		# return projects
		return {
					"msg" 			: "dear user, there is the list of projects you can access given your credentials",
					"page_args"		: page_args,
					"query_args"	: query_args,
					"data"			: projects_out 
				}


