# -*- encoding: utf-8 -*-

"""
endpoint_dsi.py  
"""

from solidata_api.api import *

log.debug(">>> api_dataset_inputs ... creating api endpoints for DSI")

from . import api, document_type

### create namespace
ns = Namespace('infos', description='Dataset inputs : request and list all dsi infos')

### import models 
from solidata_api._models.models_dataset_input import * 
mod_doc				= Dsi_infos(ns)
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
class Dsi_infos_(Resource):
	
	@ns.doc('dsi_infos')
	# @ns.expect(query_arguments)
	@jwt_optional
	def get(self, doc_id):
		"""
		get infos of a specific dsi in db

		>
			--- needs   : dsi's oid <doc_id>
			--- pagination args : page / per_page 
			--- query args : q_value_str / q_value_int / q_in_field / only_stats
			>>> returns : dsi data

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
class Dsi_List(Resource):

	@ns.doc('dsi_list')
	@ns.expect(query_pag_args)
	@jwt_optional
	# @anonymous_required
	def get(self):
		"""
		list of all tags in db

		>
			--- needs   : nothing - 
			--- pagination args : page / per_page 
			--- query args : q_title / q_description / tags / oids / only_stats
			>>> returns : projects data as a list

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

		log.debug("results have been retrieved ... " )
		# log.debug("results : \n%s ", pformat(results) )
		
		return results, response_code