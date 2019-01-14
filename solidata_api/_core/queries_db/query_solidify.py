# -*- encoding: utf-8 -*-

"""
_core/queries_db/query_solidify.py  
"""

from log_config import log, pformat
log.debug("... _core.queries_db.query_solidify.py ..." )

from  	datetime import datetime, timedelta
from	bson.objectid 	import ObjectId
from 	flask_restplus 	import  marshal

from 	. 	import db_dict_by_type, Marshaller
from 	solidata_api._choices._choices_docs import doc_type_dict
from 	solidata_api._core.solidify import *

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### GLOBAL FUNCTION TO ENRICH ONE DOC FROM DB
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 

def Query_db_solidify (
		ns, 
		models,
		document_type,
		doc_id,
		claims,
		roles_for_complete 	= ["admin"],
		payload 			= {}
	):

	print()
	print("-+- "*40)
	log.debug("... _core.queries_db.Query_db_solidify.py ..." )

	### get mongodb collections
	prj_collection		= db_dict_by_type['prj']
	dmt_collection		= db_dict_by_type['dmt']
	dmf_collection		= db_dict_by_type['dmf']
	dsi_collection		= db_dict_by_type['dsi']
	rec_collection		= db_dict_by_type['rec']


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
			user_oid 	= ObjectId(user_id)
			log.debug("user_oid : %s", user_oid )
			dft_open_level_show += ["commons"]

	### retrieve doc (PRJ f.e.) from db
	if ObjectId.is_valid(doc_id) : 
		doc_oid			= ObjectId(doc_id)
		document 		= db_collection.find_one( {"_id": doc_oid } )
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
		"is_member_of_team" : False,
		"payload" 			: payload
	}

	if document : 

		### check doc's specs : public_auth, team...
		doc_open_level_edit = document["public_auth"]["open_level_edit"]
		log.debug( "doc_open_level_edit : %s", doc_open_level_edit )
		
		### get doc's team infos
		if "team" in document : 
			team_oids = [ t["oid_usr"] for t in document["team"] ]
			log.debug( "team_oids : \n%s", pformat(team_oids) )


		### marshal out results given user's claims / doc's public_auth / doc's team ... 
		
		# for admin or members of the team --> complete infos model
		if user_role in roles_for_complete or user_oid in team_oids : 
			
			log.debug( "payload : \n%s", pformat(payload) )

			### get recipe id to run from payload
			recipe_to_run = payload[0]["id_rec"]
			log.debug( "recipe_to_run : %s", recipe_to_run )

			### retrieve recipe from db
			rec_oid = ObjectId(recipe_to_run)
			log.debug( "rec_oid : %s", rec_oid )
			recipe = rec_collection.find_one( { "_id" : rec_oid })
			log.debug( "recipe : \n%s", pformat(recipe) )

			### retrieve recipe params from doc's mapping
			map_rec_list = document["mapping"]["map_rec"]
			log.debug( "map_rec_list : \n%s", pformat(map_rec_list) )
			rec_params = next( item for item in map_rec_list if item["oid_rec"] == rec_oid )
			log.debug( "rec_oid : \n%s", pformat(rec_params) )


			### choose the function to run from recipe in db
			









			### send back updated document
			document_updated 	= db_collection.find_one( {"_id": ObjectId(doc_id) } )
			document_out 		= marshal( document_updated, models["model_doc_out"] )

			# flag as member of doc's team
			if user_oid in team_oids :
				query_resume["is_member_of_team"] = True
		
			message = "dear user, there is the complete {} you requested ".format(document_type_full)



		# for other users
		else :

			response_code	= 401
			### unvalid credentials / empty response
			message = "dear user, you don't have the credentials to solidify this {} with this oid : {}".format(document_type_full, doc_id) 








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