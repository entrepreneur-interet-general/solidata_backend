# -*- encoding: utf-8 -*-

"""
endpoint_dmf.py  
"""

from solidata_api.api import *

log.debug(">>> api_datamodel_fields ... creating api endpoints for DMF")

from . import api, document_type

### create namespace
ns = Namespace('infos', description='Datamodel_fields : request and list all dmf infos')

### import models 
from solidata_api._models.models_datamodel_field import * 
mod_doc				= Dmf_infos(ns)
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
class Dmf_infos_(Resource):
	
	@ns.doc('dmf_infos')
	# @ns.expect(query_arguments)
	@jwt_optional
	@ns.doc(params={'doc_id': 'the dmf oid'})
	def get(self, doc_id):
		"""
		get infos of a specifidmf in db

		>
			--- needs   dmf's oid <doc_id>
			>>> returns dmf data

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
class Dmf_List(Resource):

	@ns.doc('dmf_list')
	@ns.expect(query_pag_args)
	@jwt_optional
	# @anonymous_required
	def get(self):
		"""
		list of all dmf in db

		>
			--- needs   : nothing - optionnal args : pagination, list of oid_dmf, list of tags, query
			>>> returns : dmf data as a list

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
		# log.debug("query_args : \n%s ", pformat(query_args) )
		page_args				= pagination_arguments.parse_args(request)
		results, response_code	= Query_db_list (
			ns, 
			models,
			document_type,
			claims,
			page_args,
			query_args,
			roles_for_complete = ["admin","staff"],
		)

		log.debug("results have been retrieved ... " )
		# log.debug("results : \n%s ", pformat(results) )
		
		return results, response_code