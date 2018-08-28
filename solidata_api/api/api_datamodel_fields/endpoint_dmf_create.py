# -*- encoding: utf-8 -*-

"""
endpoint_dmf_create.py  
"""

from solidata_api.api import *

log.debug(">>> api_datamodel_fields ... creating api endpoints for DMF_CREATE")

### create namespace
ns = Namespace('create', description='dmf : create a new datamodel_field ')

### import models 
from solidata_api._models.models_datamodel_field import *  
model_new_dmf  	= NewDmf(ns).model
model_dmf		= Dmf_infos(ns)
model_dmf_in	= model_dmf.model_complete_in






### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 


@ns.doc(security='apikey')
@ns.route('/')
class DmfCreate(Resource):

	@ns.doc('datamodel_fields_list')
	@guest_required 
	@ns.expect(model_new_dmf, validate=True)
	# @ns.marshal_with(model_dmf_in) #, envelope="new_dmf", code=201)
	def post(self):
		"""
		Create a new dmf in db

		>
			--- needs   : a valid access_token in the header
			>>> returns : msg, dmf data 
		"""
		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )

		### DEBUG check
		log.debug ("payload : \n{}".format(pformat(ns.payload)))

		### check client identity and claims
		claims 			= get_jwt_claims() 
		user_id 		= get_jwt_identity() ### get the oid as str
		log.debug('user_identity from jwt : \n%s', user_identity )  
		# user_id 		= claims["_id"]
		log.debug("claims : \n %s", pformat(claims) )
		# user_role 		= claims["auth"]["role"]

		### get data from form and preload for marshalling
		new_dmf_infos = { 
			"infos" 		: ns.payload,
			"data_raw" 		: ns.payload,
			"public_auth" 	: {
				"open_level" : "open_data"
			},
			"specs"			: {
				"doc_type" : "dmf"
			},
		}
		log.debug('new_dmf_infos : \n%s', pformat(new_dmf_infos) )  

		### marshall infos with dmf complete model
		new_dmf 		= marshal( new_dmf_infos , model_dmf_in)
		log.debug('new_dmf : \n%s', pformat(new_dmf) )  
		
		### complete missing default fields
		new_dmf_auto_fields = { 
			"log"			: { 
				"created_at"	: datetime.utcnow(),
				"created_by"	: ObjectId(user_id),
			},
			"uses"			: {
				"by_usr"		: [ 
					{
						"used_by" : ObjectId(user_id),
						"used_at" : [ 
							# { "at" : datetime.utcnow() } 
							datetime.utcnow() 
						]
					} 
				]
			},
			"team"			: [ 
				{
					'oid_usr'	: ObjectId(user_id),
					'edit_auth'	: "owner",
					'added_at'  : datetime.utcnow(),
					'added_by'  : user_id,
				}
			],
		}
		log.debug('new_dmf_infos : \n%s', pformat(new_dmf_infos) )  

		### update marshalled infos by concatenating with auto fields
		new_dmf 	= { **new_dmf, **new_dmf_auto_fields }
		log.debug('new_dmf : \n%s', pformat(new_dmf) )  

		### save new_dmf in db 
		_id = mongo_datamodels_fields.insert( new_dmf )
		log.info("new_dmf has being created and stored in DB ...")
		log.info("_id : \n%s", pformat(_id) )

		### add _id as string to data
		new_dmf["_id"] = str(_id)
		log.debug('new_dmf : \n%s', pformat(new_dmf) )  

		### marshall out the saved item as complete data
		new_dmf_out = marshal( new_dmf , model_dmf_in)

		return { 
					"msg"	: "dear user, there is the dmf you just created... ", 
					"data" 	: new_dmf_out
				}, 200







