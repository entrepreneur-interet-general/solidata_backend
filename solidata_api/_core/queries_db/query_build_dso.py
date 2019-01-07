# -*- encoding: utf-8 -*-

"""
_core/queries_db/query_build_dso.py  
"""

from log_config import log, pformat
log.debug("... _core.queries_db.query_build_dso.py ..." )

from  	datetime import datetime, timedelta
from	bson.objectid 	import ObjectId
from 	flask_restplus 	import  marshal

from 	. 	import db_dict_by_type, Marshaller
from 	solidata_api._choices._choices_docs import doc_type_dict


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### GLOBAL FUNCTION TO BUILD A DSO FROM A PRJ DOC FROM DB
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 

def Query_db_build_dso (
		ns, 
		models,
		doc_id,
		claims,
		roles_for_complete 	= ["admin"],
		payload				= {}
	):

	print()
	print("-+- "*40)
	log.debug("... _core.queries_db.query_build_doc.py ... %s" )

	### default values
	prj_collection		= db_dict_by_type['prj']
	dmt_collection		= db_dict_by_type['dmt']
	dmf_collection		= db_dict_by_type['dmf']
	dso_collection		= db_dict_by_type['dso']

	prj_type_full 		= doc_type_dict['prj']
	dso_type_full 		= doc_type_dict['dso']

	user_id = user_oid	= None
	user_role			= "anonymous"
	document_out		= None
	message 			= None
	response_code		= 200


	if claims or claims!={}  :
		user_role 		= claims["auth"]["role"]
		user_id	 		= claims["_id"] ### get the oid as str
		if user_role != "anonymous" : 
			user_oid 	= ObjectId(user_id)
			log.debug("user_oid : %s", user_oid )

	### retrieve PRJ from db
	if ObjectId.is_valid(doc_id) : 
		doc_oid			= ObjectId(doc_id)
		document 		= prj_collection.find_one( {"_id": doc_oid } )
		log.debug( "document : \n%s", pformat(document) )
	else :
		response_code	= 400
		document		= None

	### sum up all query arguments
	query_resume = {
		"document_type"		: 'prj',	
		"doc_id" 			: doc_id,
		"user_id" 			: user_id,
		"user_role"			: user_role,
		"is_member_of_team" : False,
		"payload" 			: payload
	}

	if document : 

		### check PRJ doc's specs : public_auth, team...
		doc_open_level_show = document["public_auth"]["open_level_show"]
		doc_open_level_edit = document["public_auth"]["open_level_edit"]
		log.debug( "doc_open_level_show : %s", doc_open_level_show )

		### get doc's team infos
		if "team" in document : 
			team_oids = [ t["oid_usr"] for t in document["team"] ]
			log.debug( "team_oids : \n%s", pformat(team_oids) )

		# for admin or members of the team --> complete infos model
		if user_role in roles_for_complete or user_oid in team_oids : 

			## get payload's args 
			log.debug( "payload : \n%s", pformat(payload) )

			log.debug( "...and now let's build this DSO mate ! ..." )
		
			dso_in = marshal( {} , models["model_doc_in"])

			### copy main infos from PRJ
			dso_in['_id'] 			= doc_oid
			dso_in['infos'] 		= document["infos"]
			dso_in['public_auth']	= document["public_auth"]
			dso_in['datasets'] 		= document["datasets"]
			dso_in['team'] 			= document["team"]

			### update auto_fields 
			dso_auto_fields = { 
				"log"			: { 
					"created_at"	: datetime.utcnow(),
					"created_by"	: user_oid,
				},
				"uses"			: {
					"by_prj"		: [ 
						{
							"used_by" : doc_oid,
							"used_at" : [ 
								datetime.utcnow() 
							]
						} 
					]
				},
			}
			dso_in = { **dso_in, **dso_auto_fields }


			### get all DMF from PRJ's DMT



			### get all DSI from PRJ's dataset


			log.debug( "dso_in : \n%s", pformat(dso_in) )


			### replace / upsert DSO built 
			_id = dso_collection.replace_one( {"_id" : doc_oid }, dso_in, upsert=True )
			log.info("dso_in has being created and stored in DB ...")
			log.info("_id : \n%s", pformat(str(_id) ) )

			document_out 		= marshal( dso_in, models["model_doc_out"] )






		# TO DO 
		# for other users
		else :

			if doc_open_level_show in ["commons", "open_data"] : 
			
				# for anonymous users --> minimum infos model
				if user_id == None or user_role == "anonymous" : 
					document_out = marshal( document, models["model_doc_min"] )
				
				# for registred users (guests) --> guest infos model
				else :
					document_out = marshal( document, models["model_doc_guest_out"] )

				log.debug( "document_out : \n %s", pformat(document_out) )
				message = "dear user, there is the {} you requested given your credentials".format(prj_type_full)

			else : 
				response_code	= 401
				### unvalid credentials / empty response
				message = "dear user, you don't have the credentials to build a dso from this {} with this oid : {}".format(prj_type_full, doc_id) 


	else : 
		### no document / empty response
		response_code	= 404
		message 		= "dear user, there is no {} with this oid : {}".format(prj_type_full, doc_id) 

	### return response
	return {
				"msg" 	: message ,
				"data"	: document_out,
				"query"	: query_resume,
			}, response_code