# -*- encoding: utf-8 -*-

"""
_core/queries_db/query_delete.py  
"""

from log_config import log, pformat
log.debug("... _core.queries_db.query_delete.py ..." )

from	bson.objectid import ObjectId
# from 	flask_restplus 	import  marshal

from 	. 	import db_dict_by_type #, Marshaller
from 	solidata_api._choices._choices_docs import doc_type_dict


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### GLOBAL FUNCTION TO QUERY LIST FROM DB
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 

def Query_db_delete (
		ns, 
		models,
		document_type,
		doc_id,
		claims,
		roles_for_delete 	= ["admin"],
		auth_can_delete 	= ["owner"],
	):

	### prepare marshaller 
	# marshaller = Marshaller(ns, models)

	### default values
	db_collection				= db_dict_by_type[document_type]
	document_type_full 	= doc_type_dict[document_type]
	user_id = user_oid	= None
	user_role						= "anonymous"
	doc_oid							= ObjectId(doc_id)
	document_out				= None
	response_code				= 401
	user_allowed_to_delete 	= False
	message 						= "dear user, you don't have the credentials to delete this {} with this oid : {}".format(document_type_full, doc_id) 

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
		response_code	= 400
		document		= None

	### sum up all query arguments
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
			team_oids = { t["oid_usr"] : t["edit_auth"] for t in document["team"] }
			log.debug( "team_oids : \n%s", pformat(team_oids) )

		### marshal out results given user's claims / doc's public_auth / doc's team ... 
		# for admin or members of the team --> complete infos model
		if user_role in roles_for_delete or user_oid in team_oids : 

			# flag as member of doc's team
			if user_oid in team_oids :
				query_resume["is_member_of_team"] = True

			### check user's role in team
			if user_role in roles_for_delete or team_oids[user_oid] in auth_can_delete : 
				user_allowed_to_delete = True

			if user_allowed_to_delete : 
				### delete doc from db
				db_collection.delete_one({"_id" : doc_oid })

				### TO DO - delete user info from all projects and other datasets 
				
				
				### TO DO - OR choice to keep at least email / or / delete all data

				message 				= "dear user, you just deleted the following %s with oid : %s" %(document_type_full, doc_id)
				response_code 	= 200

	else : 
		message 		= "dear user, there is no {} with this oid : {}".format(document_type_full, doc_id) 
		response_code 	= 404

	log.debug( "message : %s", message )

	### return response
	return {
				"msg" 	: message ,
				"query"	: query_resume,
			}, response_code