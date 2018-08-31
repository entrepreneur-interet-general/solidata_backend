# -*- encoding: utf-8 -*-

"""
endpoint_rec.py  
"""

from solidata_api.api import *

log.debug(">>> api_recipes ... creating api endpoints for REC")



### create namespace
ns = Namespace('infos', description='Recipes : request and list all rec infos')

### import models 
from solidata_api._models.models_recipe import * 
mod_doc				= Rec_infos(ns)
model_doc_out		= mod_doc.mod_complete_out
model_doc_guest_out	= mod_doc.model_guest_out
model_doc_min		= mod_doc.model_minimum
document_type		= "rec"
models 				= {
	"model_doc_out" 		: model_doc_out ,
	"model_doc_guest_out" 	: model_doc_guest_out ,
	"model_doc_min" 		: model_doc_min ,
} 


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### SERIALIZERS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

@ns.marshal_with(model_doc_out)
def marshal_as_complete(results_list):
	return results_list

@ns.marshal_with(model_doc_guest_out)
def marshal_as_guest(results_list):
	return results_list

@ns.marshal_with(model_doc_min)
def marshal_as_min(results_list):
	return results_list


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 


@ns.route("/get_one/<string:doc_id>/")
class Rec_infos(Resource):
	
	@ns.doc('rec_infos')
	# @ns.expect(query_arguments)
	@jwt_optional
	def get(self, doc_id):
		"""
		get infos of a specific rec in db

		>
			--- needs   : rec's oid <doc_id>
			>>> returns : rec data

		"""

		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )

		### DEBUG check
		# log.debug ("payload : \n{}".format(pformat(ns.payload)))

		db_collection		= db_dict_by_type[document_type]
		document_type_full 	= doc_type_dict[document_type]
		user_id = user_oid	= None
		user_role			= "anonymous"
		document_out		= None
		message 			= None

		### check client identity and claims
		claims 				= get_jwt_claims() 
		log.debug("claims : \n %s", pformat(claims) )
		
		# user_id 	= get_jwt_identity() ### get the oid as str
		if claims or claims!={}  :
			user_role 		= claims["auth"]["role"]
			user_id	 		= claims["_id"] ### get the oid as str
			if user_role != "anonymous" : 
				user_oid 		= ObjectId(user_id)
				log.debug("user_oid : %s", user_oid )

		### retrieve from db
		if ObjectId.is_valid(doc_id) : 
			document 		= db_collection.find_one( {"_id": ObjectId(doc_id) })
			log.debug( "document : \n%s", pformat(document) )
		else :
			document		= None

		query_resume = {
			"document_type"		: document_type,	
			"doc_id" 			: doc_id,
			"user_id" 			: user_id,
			"user_role"			: user_role,
			"is_member_of_team" : False
		}

		if document : 

			### check doc's specs : public_auth, team...
			doc_open_level_show = document["public_auth"]["open_level_show"]
			log.debug( "doc_open_level_show : %s", doc_open_level_show )
			
			### get doc's team infos
			if "team" in document : 
				team_oids = [ t["oid_usr"] for t in document["team"] ]
				log.debug( "team_oids : \n%s", pformat(team_oids) )


			### marshal out results given user's claims / doc's public_auth / doc's team ... 
			# for admin or members of the team --> complete infos model
			if user_role in ["admin","staff"] or user_oid in team_oids : 
				
				document_out = marshal( document, model_doc_out )

				# flag as member of doc's team
				if user_oid in team_oids :
					query_resume["is_member_of_team"] = True
			
				message = "dear user, there is the complete {} you requested ".format(document_type_full)

			# for other users
			else :

				if doc_open_level_show in ["commons", "open_data"] : 
				
					# for anonymous users --> minimum infos model
					if user_id == None or user_role == "anonymous" : 
						document_out = marshal( document, model_doc_min )
					
					# for registred users (guests) --> guest infos model
					else :
						document_out = marshal( document, model_doc_guest_out )

					log.debug( "document_out : \n %s", pformat(document_out) )
					message = "dear user, there is the {} you requested given your credentials".format(document_type_full)

				else : 
					### unvalid credentials / empty response
					message = "dear user, you don't have the credentials to access/see this {} with this oid : {}".format(document_type_full, doc_id) 

		else : 
			### no document / empty response
			message = "dear user, there is no {} with this oid : {}".format(document_type_full, doc_id) 

		### return response
		return {
					"msg" 	: message ,
					"data"	: document_out,
					"query"	: query_resume,
				}, 200

@ns.route('/list')
class Rec_List(Resource):

	@ns.doc('rec_list')
	@ns.expect(pagination_arguments)
	@ns.expect(query_arguments)
	@jwt_optional
	# @anonymous_required
	def get(self):
		"""
		list of all rec in db

		>
			--- needs   : nothing - optionnal args : pagination, list of oid_rec, list of tags, query
			>>> returns : rec data as a list

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
		query_args		= query_arguments.parse_args(request)
		page_args		= pagination_arguments.parse_args(request)
		results 		= Query_db_list (
			ns, 
			models,
			document_type,
			claims,
			page_args,
			query_args,
			roles_for_complete = ["admin","staff"],
		)

		log.debug("results : \n%s ", pformat(results) )
		
		return results, 200