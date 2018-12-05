# -*- encoding: utf-8 -*-

"""
_core/queries_db/query_doc.py  
"""

from log_config import log, pformat
log.debug("... _core.queries_db.query_doc.py ..." )

from	bson.objectid 	import ObjectId
from 	flask_restplus 	import  marshal

from 	. 	import db_dict_by_type, Marshaller
from 	solidata_api._choices._choices_docs import doc_type_dict


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### GLOBAL FUNCTION TO QUERY ONE DOC FROM DB
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 

def Query_db_doc (
		ns, 
		models,
		document_type,
		doc_id,
		claims,
		page_args,
		query_args,
		roles_for_complete 	= ["admin"],

		slice_f_data		= True,

	):



	### prepare marshaller 
	# marshaller = Marshaller(ns, models)

	### default values
	db_collection		= db_dict_by_type[document_type]
	document_type_full 	= doc_type_dict[document_type]
	user_id = user_oid	= None
	user_role			= "anonymous"
	document_out		= None
	message 			= None
	dft_open_level_show = ["open_data"]
	response_code		= 200

	if claims or claims!={}  :
		user_role 		= claims["auth"]["role"]
		user_id	 		= claims["_id"] ### get the oid as str
		if user_role != "anonymous" : 
			user_oid 		= ObjectId(user_id)
			log.debug("user_oid : %s", user_oid )
			dft_open_level_show += ["commons"]

	### get pagination arguments
	log.debug('page_args : \n%s', pformat(page_args) )  
	page 			= page_args.get('page', 	1 )
	per_page 		= page_args.get('per_page', 0 )
	if per_page == 0 :
		start_index		= ( page - 1 ) * per_page 
		end_index 		= start_index + per_page
	else : 
		start_index		= 0 
		end_index 		= 5	

	### get query arguments
	q_title 		= query_args.get('q_title', 		None )
	q_description 	= query_args.get('q_description', 	None )
	q_oid_list		= query_args.get('oids',			None )
	q_oid_tags		= query_args.get('tags',			None )
	q_only_stats	= query_args.get('only_stats',		False )

	### retrieve from db
	if ObjectId.is_valid(doc_id) : 
		document 		= db_collection.find_one( {"_id": ObjectId(doc_id) })
		log.debug( "document._id : %s", str(document["_id"]) )
		# log.debug( "document : \n%s", pformat(document) )
	else :
		response_code	= 400
		document		= None

	### sum up all query arguments
	query_resume = {
		"document_type"		: document_type,	
		"doc_id" 			: doc_id,
		"user_id" 			: user_id,
		"user_role"			: user_role,
		"page_args"			: page_args,
		"query_args"		: query_args,
		"is_member_of_team" : False,
		"is_creator" 		: False,
	}

	if document : 

		### check doc's specs : public_auth, team...
		doc_open_level_show = document["public_auth"]["open_level_show"]
		log.debug( "doc_open_level_show : %s", doc_open_level_show )

		### get doc's owner infos
		created_by_oid = document["log"]["created_by"]
		log.debug( "created_by_oid : %s", str(created_by_oid) )

		### get doc's team infos
		if "team" in document : 
			team_oids = [ t["oid_usr"] for t in document["team"] ]
			log.debug( "team_oids : \n%s", pformat(team_oids) )


		### marshal out results given user's claims / doc's public_auth / doc's team ... 
		# for admin or members of the team --> complete infos model
		if user_role in roles_for_complete or user_oid in team_oids or user_oid == created_by_oid : 
			
			document_out = marshal( document, models["model_doc_out"] )

			# flag as member of doc's team
			if user_oid == created_by_oid :
				query_resume["is_creator"] = True

			# flag as member of doc's team
			if user_oid in team_oids :
				query_resume["is_member_of_team"] = True

			# append "f_data" if doc is in ["dsi", "dsr", "dsr"]
			if document_type in ["dsi", "dsr", "dsr"] :
    			
				# slice f_data
				if slice_f_data == False :
					document_out["data_raw"]["f_data"] = document["data_raw"]["f_data"]
				else :
					document_out["data_raw"]["f_data"] = document["data_raw"]["f_data"][ start_index : end_index ]

			message = "dear user, there is the complete {} you requested ".format(document_type_full)

		# for other users
		else :

			if doc_open_level_show in ["commons", "open_data"] : 
			
				### for anonymous users --> minimum infos model
				if user_id == None or user_role == "anonymous" : 
					document_out = marshal( document, models["model_doc_min"] )
				
				### for registred users (guests) --> guest infos model
				else :
					document_out = marshal( document, models["model_doc_guest_out"] )
					
					# append "f_data" if doc is in ["dsi", "dsr", "dso"]
					if document_type in ["dsi", "dsr", "dso"] :
    					
						### slice f_data by default
						document_out["data_raw"]["f_data"] = document["data_raw"]["f_data"][ start_index : end_index ]
						
				message = "dear user, there is the {} you requested given your credentials".format(document_type_full)

			else : 
				response_code	= 401
				### unvalid credentials / empty response
				message = "dear user, you don't have the credentials to access/see this {} with this oid : {}".format(document_type_full, doc_id) 

	else : 
		### no document / empty response
		response_code	= 404
		message 		= "dear user, there is no {} with this oid : {}".format(document_type_full, doc_id) 

	### return response
	return {
				"msg" 	: message ,
				"data"	: document_out,
				"query"	: query_resume,
			}, response_code