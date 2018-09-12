# -*- encoding: utf-8 -*-

"""
endpoint_prj_create.py  
"""

from solidata_api.api import *

log.debug(">>> api_projects ... creating api endpoints for PROJ_CREATE")

from . import api, document_type

### create namespace
ns = Namespace('create', description='Projects : create a new project')

### import models 
from solidata_api._models.models_project import * 
model_form_new_prj  	= NewPrj(ns).model
mod_prj					= Prj_infos(ns)
model_project_in		= mod_prj.mod_complete_in
model_project_out		= mod_prj.mod_complete_out










### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 






@ns.doc(security='apikey')
@ns.route('/')
class PrjCreate(Resource):

	@ns.doc('prj_create')
	@guest_required
	@ns.expect(model_form_new_prj, validate=True)
	# @ns.marshal_with(model_prj_in) #, envelope="new_prj", code=201)
	def post(self):
		"""
		Create a new project in db

		>
			--- needs   : a valid access_token in the header
			>>> returns : msg, prj data 
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
		
		# user_id 		= get_jwt_identity() ### get the oid as str
		# log.debug('user_identity from jwt : \n%s', user_identity )  
		user_id 		= claims["_id"]
		user_oid		= ObjectId(user_id)
		# user_role 		= claims["auth"]["role"]
		log.debug('user_oid : %s', user_oid )  

		### get data from form and preload for marshalling
		new_prj_infos = { 
			"infos" 		: ns.payload,
			"public_auth" 	: ns.payload,
			"specs"			: {
				"doc_type" : "prj"
			},
		}
		### pre-marshall infos with prj complete model
		new_prj 	= marshal( new_prj_infos , model_project_in)
		log.debug('new_prj : \n%s', pformat(new_prj) )  

		### complete missing default fields
		new_prj_auto_fields = { 
			"log"			: { 
				"created_at"	: datetime.utcnow(),
				"created_by"	: user_oid,
				"is_running"	: False
			},
			"uses"			: {
				"by_usr"		: [ 
					{
						"used_by" : user_oid,
						"used_at" : [ 
							# { "at" : datetime.utcnow() } 
							datetime.utcnow() 
						]
					} 
				]
			},
			"team"			: [ 
				{
					'oid_usr'	: user_oid,
					'edit_auth'	: "owner",
					'added_at'  : datetime.utcnow(),
					'added_by'  : user_oid,
				}
			],
		}
		log.debug('new_prj_infos : \n%s', pformat(new_prj_infos) )  

		### update marshalled infos by concatenating with auto fields
		new_prj 	= { **new_prj, **new_prj_auto_fields }
		log.debug('new_prj : \n%s', pformat(new_prj) )  

		### save new_prj in db
		_id = mongo_projects.insert( new_prj )
		log.info("new_prj has being created and stored in DB ...")
		log.info("_id : \n%s", pformat(_id) )
		
		### add _id as string to data to mrashall out
		new_prj["_id"] = _id
		log.debug('new_prj : \n%s', pformat(new_prj) )  

		### marshall out the saved item as complete data
		new_prj_out = marshal( new_prj , model_project_out)
		log.debug('new_prj_out : \n%s', pformat(new_prj_out) )  

		return {
					"msg"	: "dear user, there is the prj you just created... ", 
					"data" 	: new_prj_out,
				}, 200