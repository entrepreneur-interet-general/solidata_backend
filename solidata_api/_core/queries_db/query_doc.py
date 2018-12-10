# -*- encoding: utf-8 -*-

"""
_core/queries_db/query_doc.py  
"""

import re

from log_config import log, pformat
log.debug("... _core.queries_db.query_doc.py ..." )

from	bson.objectid 	import ObjectId
from 	flask_restplus 	import  marshal

from 	. 	import db_dict_by_type, Marshaller
from 	solidata_api._choices._choices_docs import doc_type_dict

import operator


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### UTIL FUNCTION TO HELP SORTING LIST OF DICTS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : https://stackoverflow.com/questions/45737561/how-to-ignore-none-values-with-operator-itemgetter-when-sorting-a-list-of-dicts 

def weighted(nb):
	
	if nb is None:
		# return -float('inf')
		return ''
	else:
		# return nb
		return str(nb)
	# return -float('inf') if nb is None else nb

def sort_list_of_dicts(list_to_sort, key_value, is_reverse=True) :
	# return sorted(list_to_sort, key = lambda i: i[key_value]) 
	return sorted(list_to_sort, key=lambda i:weighted(i[key_value]), reverse=is_reverse)

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
		user_role 	= claims["auth"]["role"]
		user_id	 	= claims["_id"] ### get the oid as str
		if user_role != "anonymous" : 
			user_oid 		= ObjectId(user_id)
			log.debug("user_oid : %s", user_oid )
			dft_open_level_show += ["commons"]

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

	### get pagination arguments
	log.debug('page_args : \n%s', pformat(page_args) )  
	page 		= page_args.get('page', 	1 )
	per_page 	= page_args.get('per_page', 10 )
	if page != 1 :
		start_index		= ( page - 1 ) * per_page 
		end_index 		= start_index + per_page
	else : 
		start_index		= 0
		end_index 		= per_page	
	log.debug('start_index : %s', start_index )  
	log.debug('end_index   : %s', end_index )  

	### get query arguments
	log.debug('query_args : \n%s', pformat(query_args) )  
	q_value_str 	= query_args.get('q_value_str', 	None )
	q_value_int 	= query_args.get('q_value_int', 	None )
	q_in_field		= query_args.get('q_in_field',		None )
	only_f_data		= query_args.get('only_f_data',		False )
	only_stats		= query_args.get('only_stats',		False )
	slice_f_data	= query_args.get('slice_f_data',	True )
	sort_by			= query_args.get('sort_by',			None )


	### TO FINISH !!!
	### prepare pipelines 
	# pipeline_queries		= {
	# 	"$or" : [
	# 		{ "infos.title" : q_value_str },
	# 	]
	# }
	# pipeline_accessible 	= {
	# 	"public_auth.open_level_show" : { 
	# 		"$in" : dft_open_level_show,
	# 	} 
	# }
	# pipeline_user_is_in_team 	= {
	# 	"team" : { 
	# 		"$elemMatch" : {
	# 			"oid_usr" : user_oid
	# 		}
	# 	} 
	# }
	# pipeline_user_not_in_team 	= { 
	# 	"public_auth.open_level_show" : { 
	# 		"$in" : dft_open_level_show,
	# 	},
	# 	"team" : { 
	# 		"$not" : {
	# 			"$elemMatch" : {
	# 				"oid_usr" : {
	# 					"$in" : [ user_oid ]
	# 				}
	# 			}
	# 		}
	# 	} 
	# }


	### retrieve from db
	if ObjectId.is_valid(doc_id) : 
		document 		= db_collection.find_one( {"_id": ObjectId(doc_id) })
		log.debug( "document._id : %s", str(document["_id"]) )
		# log.debug( "document : \n%s", pformat(document) )
	else :
		response_code	= 400
		document		= None



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
			
				log.debug( '...document_type : %s', document_type )

				# if document_type == 'dsi' :
				# 	### TO DO --> GET dsr.data_raw.f_data instead of dsi.data_raw.f_data 
				# 	pass

				### copy f_data
				document_out["data_raw"]["f_data"] = document["data_raw"]["f_data"]
				log.debug( 'document_out["data_raw"]["f_data"][0] : \n%s', pformat(document_out["data_raw"]["f_data"][0]) )
				
				### sort results
				if sort_by != None :
					log.debug( 'sort_by : %s', sort_by )
					# NOT WORKING : document_out["data_raw"]["f_data"] = document_out["data_raw"]["f_data"].sort(key=operator.itemgetter(sort_by))
					# NOT WORKING WITH MISSING FIELDS : document_out["data_raw"]["f_data"] = sorted(document_out["data_raw"]["f_data"], key = lambda i: i[sort_by]) 
					document_out["data_raw"]["f_data"] = sort_list_of_dicts(document_out["data_raw"]["f_data"], sort_by)
					log.debug( '...document_out sorted' )
					log.debug( 'document_out["data_raw"]["f_data"][0] : \n%s', pformat(document_out["data_raw"]["f_data"][0]) )

				# slice f_data
				if slice_f_data == True :
					document_out["data_raw"]["f_data"] = document_out["data_raw"]["f_data"][ start_index : end_index ]

				# add total of items within f_data in response
				document_out["data_raw"]["f_data_count"] = len(document["data_raw"]["f_data"])

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
	
						log.debug( '...document_type : %s', document_type )

						# if document_type == 'dsi' :
						# 	### TO DO --> GET dsr.data_raw.f_data instead of dsi.data_raw.f_data 	
						# 	pass

						### copy f_data
						document_out["data_raw"]["f_data"] = document["data_raw"]["f_data"]
						log.debug( 'document_out["data_raw"]["f_data"][0] : \n%s', pformat(document_out["data_raw"]["f_data"][0]) )
						
						### sort results
						if sort_by != None :
							log.debug( 'sort_by : %s', sort_by )
							# NOT WORKING : document_out["data_raw"]["f_data"] = document_out["data_raw"]["f_data"].sort(key=operator.itemgetter(sort_by))
							document_out["data_raw"]["f_data"] = sorted(document_out["data_raw"]["f_data"], key = lambda i: i[sort_by]) 
							log.debug( '...document_out sorted' )
							log.debug( 'document_out["data_raw"]["f_data"][0] : \n%s', pformat(document_out["data_raw"]["f_data"][0]) )

						### slice f_data by default
						document_out["data_raw"]["f_data"] = document_out["data_raw"]["f_data"][ start_index : end_index ]
					
						# add total of items within f_data in response
						document_out["data_raw"]["f_data_count"] = len(document["data_raw"]["f_data"])
						
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