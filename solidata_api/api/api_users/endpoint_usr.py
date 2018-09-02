# -*- encoding: utf-8 -*-

"""
endpoint_usr.py  
- provides the API endpoints for consuming and producing
	REST requests and responses
"""

from solidata_api.api import *

log.debug(">>> api_users ... creating api endpoints for USERS")

### create namespace
ns = Namespace('infos', description='Users : users lists related endpoints ')

### import models 
from solidata_api._models.models_user import *  
model_new_user  = NewUser(ns).model
model_user 		= User_infos(ns)
model_user_in	= model_user.model_complete_in
model_user_out	= model_user.model_complete_out

mod_doc				= User_infos(ns)
model_doc_out		= mod_doc.mod_complete_out
model_doc_guest_out	= mod_doc.model_guest_out
model_doc_min		= mod_doc.model_minimum
models 				= {
	"model_doc_out" 		: model_doc_out ,
	"model_doc_guest_out" 	: model_doc_guest_out ,
	"model_doc_min" 		: model_doc_min ,
} 



### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 


@ns.route("/get_one/<string:doc_id>/")
class Usr_infos(Resource):
	
	@ns.doc('usr_infos')
	# @ns.expect(query_arguments)
	@jwt_optional
	def get(self, doc_id):
		"""
		get infos of a specific usr in db

		>
			--- needs   : user's oid <doc_id>
			>>> returns : user data

		"""
		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )

		### DEBUG check
		# log.debug ("payload : \n{}".format(pformat(ns.payload)))

		### check client identity and claims
		claims 				= get_jwt_claims() 
		log.debug("claims : \n %s", pformat(claims) )


		### query db from generic function 		
		results, response_code	= Query_db_doc (
			ns, 
			models,
			document_type,
			doc_id,
			claims,
			roles_for_complete = ["admin"],
		)

		log.debug("results : \n%s ", pformat(results) )


		return results, response_code


@ns.route('/list')
class Usr_List(Resource):

	@ns.doc('usr_list')
	@ns.expect(query_pag_args)
	@jwt_optional
	# @anonymous_required
	def get(self):
		"""
		list of all usr in db

		>
			--- needs   : nothing - optionnal args : pagination, list of oid_usr, list of tags, query
			>>> returns : usr data as a list

		"""

		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )

		### DEBUG check
		log.debug ("payload : \n{}".format(pformat(ns.payload)))


		### check client identity and claims
		claims 				= get_jwt_claims() 
		log.debug("claims : \n %s", pformat(claims) )


		### query db from generic function 		
		query_args				= query_arguments.parse_args(request)
		page_args				= pagination_arguments.parse_args(request)
		results, response_code	= Query_db_list (
			ns, 
			models,
			document_type,
			claims,
			page_args,
			query_args,
			roles_for_complete = ["admin"],
		)

		log.debug("results : \n%s ", pformat(results) )
		
		return results, response_code





