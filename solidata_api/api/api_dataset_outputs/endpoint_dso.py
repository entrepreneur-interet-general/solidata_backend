# -*- encoding: utf-8 -*-

"""
endpoint_dso.py  
"""

from solidata_api.api import *

log.debug(">>> api_dataset_outputs ... creating api endpoints for DSO")

from . import api, document_type

### create namespace
ns = Namespace('infos', description='Dataset outputs : request and list all dso infos')

### import models 
from solidata_api._models.models_dataset_output import * 
mod_doc				= Dso_infos(ns)
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





@ns.route("/get_one/<string:doc_id>")
class Dso_infos_(Resource):
	
	"""
	PRJ infos
	GET    - Shows a document's infos 
	"""

	@ns.doc('dso_infos')
	# @ns.expect(query_arguments)
	@jwt_optional
	def get(self, doc_id):
		"""
		get infos of a specific dso in db

		>
			--- needs   : project's oid <doc_id>
			--- optional : request arguments (pagination|query), json web token in headers...  (cf : solidata_api._parsers.parser_classes)
			>>> returns : project data

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
		query_args				= query_data_arguments.parse_args(request)
		page_args				= pagination_arguments.parse_args(request)
		results, response_code	= Query_db_doc (
			ns, 
			models,
			document_type,
			doc_id,
			claims,
			page_args,
			query_args,
			roles_for_complete = ["admin"],
		)

		log.debug("results have been retrieved ... " )
		# log.debug("results : \n%s ", pformat(results) )


		return results, response_code


@ns.route('/list')
class Dso_List(Resource):

	@ns.doc('dso_list')
	@ns.expect(query_pag_args)
	@jwt_optional
	# @anonymous_required
	def get(self):
		"""
		list of all dso in db

		>
			--- needs   : nothing - optionnal args : pagination, list of oid_prj, list of tags, query
			>>> returns : prj data as a list

		"""

		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )
		log.debug( "request : \n%s", pformat(request.__dict__) )


		### DEBUG check
		log.debug ("payload : \n{}".format(pformat(ns.payload)))


		### check client identity and claims
		claims 				= get_jwt_claims() 
		log.debug("claims : \n %s", pformat(claims) )

		# log.debug("request.args : %s ", request.args)
		# args_type = type(request.__dict__["args"])
		# log.debug("args_type : %s ", args_type)

		### query db from generic function 		
		query_args				= query_arguments.parse_args(request)
		page_args				= pagination_arguments.parse_args(request)
		log.debug ("page_args : \n{}".format(page_args))

		results, response_code	= Query_db_list (
			ns, 
			models,
			document_type,
			claims,
			page_args,
			query_args,
			roles_for_complete = ["admin"],
		)

		log.debug("results have been retrieved ... " )
		# log.debug("results : \n%s ", pformat(results) )
		
		return results, response_code


