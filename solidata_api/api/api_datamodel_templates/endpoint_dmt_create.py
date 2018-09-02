# -*- encoding: utf-8 -*-

"""
endpoint_dmt_create.py  
"""

from solidata_api.api import *

log.debug(">>> api_datamodel_templates ... creating api endpoints for DMT_CREATE")

from . import api, document_type

### create namespace
ns = Namespace('create', description='Dmt : create a new datamodel_template ')

### import models 
from solidata_api._models.models_datamodel_template import *  
model_new_dmt  	= NewDmt(ns).model
model_dmt		= Dmt_infos(ns)
model_dmt_in	= model_dmt.model_complete_in










### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 






@ns.doc(security='apikey')
@ns.route('/')
class DmtCreate(Resource):

	@ns.doc('dmt_create')
	@guest_required 
	@ns.expect(model_new_dmt, validate=True)
	# @ns.marshal_with(model_dmt_in) #, envelope="new_dmt", code=201)
	def post(self):
		"""
		Create a new dmt in db

		>
			--- needs   : a valid access_token in the header
			>>> returns : msg, dmt data 
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

		### get data from form and preload for marshalling
		new_dmt_infos = { 
			"infos" 		: ns.payload,
			"public_auth" 	: ns.payload,
			"specs"			: {
				"doc_type" : "dmt"
			},
		}

		### marshall infos with dmt complete model
		new_dmt 		= marshal( new_dmt_infos , model_dmt_in)
		log.debug('new_dmt : \n%s', pformat(new_dmt) )  
		
		### complete missing default fields
		new_dmt_auto_fields = { 
			"log"			: { 
				"created_at"	: datetime.utcnow(),
				"created_by"	: user_oid,
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
		log.debug('new_dmt_infos : \n%s', pformat(new_dmt_infos) )  

		### update marshalled infos by concatenating with auto fields
		new_dmt 	= { **new_dmt, **new_dmt_auto_fields }
		log.debug('new_dmt : \n%s', pformat(new_dmt) )  

		### save new_dmt in db 
		_id = mongo_datamodels_templates.insert( new_dmt )
		log.info("new_dmt has being created and stored in DB ...")
		log.info("_id : \n%s", pformat(_id) )

		### add _id as string to data
		new_dmt["_id"] = str(_id)
		log.debug('new_dmt : \n%s', pformat(new_dmt) )  

		### marshall out the saved item as complete data
		new_dmt_out = marshal( new_dmt , model_dmt_in)

		return { 
					"msg"	: "dear user, there is the dmt you just created... ", 
					"data" 	: new_dmt_out
				}, 200







