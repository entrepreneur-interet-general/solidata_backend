# -*- encoding: utf-8 -*-

"""
endpoint_dmt.py  
- provides the API endpoints for consuming and producing
	REST requests and responses
"""

from solidata_api.api import *

log.debug(">>> api_datamodel_templates ... creating api endpoints for DMT")

### create namespace
ns = Namespace('list', description='Datamodel templates : dmt lists related endpoints ')

### import models 
from solidata_api._models.models_datamodel_template import *  
model_new_dmt  	= NewDmt(ns).model
model_dmt		= Dmt_infos(ns).model_complete_in
model_dmt_min	= Dmt_infos(ns).model_minimum


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 


@ns.doc(security='apikey')
@ns.route('/')
class DmtList(Resource):

	### TO DO  : pagination arguments
	@ns.doc('datamodel_templates_list')
	@ns.expect(pagination_arguments)
	@ns.marshal_list_with( model_dmt, skip_none=True) #, envelop="users_list" ) 
	def get(self):
		"""
		List of all dmts in db (without _id)

		>
			--- needs   : a valid access_token in the header
			>>> returns : msg, users data as a list
		"""
		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )
		log.debug ("payload : \n{}".format(pformat(ns.payload)))

		### get data from form
		new_dmt_infos = ns.payload

		### DEBUG check
		user_identity = get_jwt_identity()
		log.debug('user_identity from jwt : \n%s', user_identity )  


		return { 
					"msg"			: "dear admin, there is the users list... ", 
					"dmts_list" 	: [] 
				}, 200







