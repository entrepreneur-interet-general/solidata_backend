# -*- encoding: utf-8 -*-

"""
endpoint_prj_solidify.py  
"""

from solidata_api.api import *

log.debug(">>> api_prj ... creating api endpoints for PRJ_SOLIDIFY")

from . import api, document_type

### create namespace
ns = Namespace('solidify', description='Solidify and enrich docs of a prj : ... ')

### import models 
from solidata_api._models.models_solidify import *
from solidata_api._models.models_project import * 
mod_doc				= Prj_infos(ns)
model_doc_out		= mod_doc.mod_complete_out
model_doc_guest_out	= mod_doc.model_guest_out
model_doc_min		= mod_doc.model_minimum
models 				= {
	"model_doc_out" 		: model_doc_out ,
	"model_doc_guest_out" 	: model_doc_guest_out ,
	"model_doc_min" 		: model_doc_min ,
} 

model_solidify	= Solidify_run_params(ns, document_type).model_solidify_generic

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 

# cf : http://flask-jwt-extended.readthedocs.io/en/latest/refresh_tokens.html



@ns.doc(security='apikey')
@ns.route('/<string:doc_id>')
@ns.response(404, 'document not found')
class Prj_solidify(Resource):

	"""
	prj edition :
	PUT    - Updates document's infos
	"""

	@ns.doc('solidify_prj')
	@guest_required 
	@ns.expect([model_solidify])
	def put(self, doc_id):
		"""
		Solidify a  prj in db

		>
			--- needs   : a valid access_token in the header, field_to_update, field_value
			>>> returns : msg, doc data 
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

		### update doc in DB
		response, response_code	= Query_db_solidify (
			ns, 
			models,
			document_type,
			doc_id,
			claims,
			roles_for_complete = ["admin"],
			payload = ns.payload
		)

		# log.debug("response : \n%s ", pformat(response) )
		log.debug("the prj has been updated") 

		### return updated document
		# return {
		# 	"msg" : "updating doc...."
		# }, 200
		return response, response_code

