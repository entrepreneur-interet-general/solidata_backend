# -*- encoding: utf-8 -*-

"""
endpoint_rec_create.py  
"""

from solidata_api.api import *

log.debug(">>> api_recipes ... creating api endpoints for REC_CREATE")

from . import api, document_type

### create namespace
ns = Namespace('create', description='Recipes : create a new recipe')

### import models 
from solidata_api._models.models_recipe import * 
model_form_new_rec  	= NewRec(ns).model
mod_rec					= Rec_infos(ns)
model_recipe_in			= mod_rec.mod_complete_in
model_recipe_out		= mod_rec.mod_complete_out

models 			= {
	"model_doc_in" 			: model_recipe_in ,
	"model_doc_out" 		: model_recipe_out 
} 


### CREATE DEFAULT TAGS FROM config_default_docs
### import default documents 
from solidata_api.config_default_docs import default_recipes_list
for dft_rec in default_recipes_list : 
	
	log.debug ("dft_rec : \n{}".format(pformat(dft_rec)))
	
	# Query_db_insert(
	# 	ns, 
	# 	models,
	# 	document_type,

	# 	dft_rec,

	# 	value_to_check 	= dft_rec["infos"]["title"],
	# 	field_to_check	= "infos.title",

	# 	user_role   	= "system"
	# )







### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 






@ns.doc(security='apikey')
@ns.route('/')
class RecCreate(Resource):

	@ns.doc('rec_create')
	@guest_required
	@ns.expect(model_form_new_rec, validate=True)
	# @ns.marshal_with(model_rec_in) #, envelope="new_rec", code=201)
	def post(self):
		"""
		Create a new recipe in db

		>
			--- needs   : a valid access_token in the header
			>>> returns : msg, rec data 
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
		new_rec_infos = { 
			"infos" 		: ns.payload,
			"public_auth" 	: ns.payload,
			"specs"			: {
				"doc_type" : "rec"
			},
		}
		### pre-marshall infos with prj complete model
		new_rec 	= marshal( new_rec_infos , model_recipe_in)
		log.debug('new_rec : \n%s', pformat(new_rec) )  

		### complete missing default fields
		new_rec_auto_fields = { 
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
		log.debug('new_rec_infos : \n%s', pformat(new_rec_infos) )  

		### update marshalled infos by concatenating with auto fields
		new_rec 	= { **new_rec, **new_rec_auto_fields }
		log.debug('new_rec : \n%s', pformat(new_rec) )  

		### save new_rec in db
		_id = mongo_recipes.insert( new_rec )
		log.info("new_rec has being created and stored in DB ...")
		log.info("_id : \n%s", pformat(_id) )
		
		### add _id as string to data to mrashall out
		new_rec["_id"] = _id
		log.debug('new_rec : \n%s', pformat(new_rec) )  

		### marshall out the saved item as complete data
		new_rec_out = marshal( new_rec , model_recipe_out )
		log.debug('new_rec_out : \n%s', pformat(new_rec_out) )  

		return {
					"msg"	: "dear user, there is the rec you just created... ", 
					"data" 	: new_rec_out,
				}, 200