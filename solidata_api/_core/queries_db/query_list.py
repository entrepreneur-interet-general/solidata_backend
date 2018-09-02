# -*- encoding: utf-8 -*-

"""
_core/queries_db/query_list.py  
"""

from log_config import log, pformat
log.debug("... _core.queries_db.query_list.py ..." )

from	bson.objectid import ObjectId
from 	flask_restplus 	import  marshal

from 	. 	import db_dict_by_type, Marshaller
from 	solidata_api._choices._choices_docs import doc_type_dict


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### GLOBAL FUNCTION TO QUERY LIST FROM DB
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 

def Query_db_list (
		ns, 
		models,
		document_type,
		claims,
		page_args,
		query_args,
		roles_for_complete 	= ["admin"],
		check_teams			= True
	):

	### prepare marshaller 
	marshaller = Marshaller(ns, models)

	### default values
	db_collection			= db_dict_by_type[document_type]
	document_type_full 		= doc_type_dict[document_type]
	user_id = user_oid		= None
	user_role				= "anonymous"
	documents_out_in_team	= None
	documents_out_not_team	= None
	message 				= None
	dft_open_level_show		= ["open_data"]
	response_code			= 200
	cursor_in_team_count	= 0
	cursor_not_team_count	= 0

	### get user's role and _id
	# user_id 	= get_jwt_identity() ### get the oid as str
	if claims or claims != {}  :
		user_role 		= claims["auth"]["role"]
		user_id	 		= claims["_id"] ### get the oid as str
		if user_role != "anonymous" : 
			user_oid 		= ObjectId(user_id)
			log.debug("user_oid : %s", user_oid )
			dft_open_level_show += ["commons"]
			if user_role in roles_for_complete : 
				dft_open_level_show += ["private","collective"]
	log.debug('dft_open_level_show : \n%s', pformat(dft_open_level_show) )  


	page 			= page_args.get('page', 	1  )
	per_page 		= page_args.get('per_page', 10 )
	start_index		= ( page - 1 ) * per_page 
	end_index 		= start_index + per_page

	q_title 		= query_args.get('q_title', 		None )
	q_description 	= query_args.get('q_description', 	None )
	q_oid_list		= query_args.get('oids',			None )
	q_oid_tags		= query_args.get('tags',			None )
	q_only_stats	= query_args.get('only_stats',		False )

	### sum up all query arguments
	query_resume = {
		"document_type"		: document_type,	
		"user_id" 			: user_id,
		"user_role"			: user_role,
		"page_args"			: page_args,
		"query_args"		: query_args,
	}

	### TO FINISH !!!
	### prepare pipelines 
	pipeline_queries		= {
		"$or" : [
			{ "infos.title" : q_title },
			{ "infos.description" : q_description },
		]
	}

	pipeline_accessible 	= {
		"public_auth.open_level_show" : { 
			"$in" : dft_open_level_show,
		} 
	}
	pipeline_user_is_in_team 	= {
		"team" : { 
			"$elemMatch" : {
				"oid_usr" : user_oid
			}
		} 
	}
	pipeline_user_not_in_team 	= { 
		"public_auth.open_level_show" : { 
			"$in" : dft_open_level_show,
		},
		"team" : { 
			"$elemMatch" : {
				"oid_usr" : {
					"$nin" : [ user_oid ]
				}
			}
		} 
	}

	### DOCS ACCESSIBLE
	# retrieve docs from db
	cursor_accessible			= db_collection.find(pipeline_accessible)
	cursor_accessible_count		= cursor_accessible.count()
	log.debug('cursor_accessible_count : %s', cursor_accessible_count) 

	### DOCS USER IS IN TEAM
	# retrieve docs from db
	if user_role != "anonymous" : 
		cursor_in_team 			= db_collection.find(pipeline_user_is_in_team)
		cursor_in_team_count	= cursor_in_team.count()
		log.debug('cursor_in_team_count : %s', cursor_in_team_count) 
		if q_only_stats == False : 
			documents_in_team		= list(cursor_in_team)
			# log.debug( "documents_in_team : \n %s", pformat(documents_in_team) )
			# marshal out results
			if documents_in_team != [] :
					### trim list with pagimation
				if cursor_in_team_count > per_page : 
					documents_in_team = documents_in_team[ start_index : end_index ]

				if user_role in roles_for_complete : 
					documents_out_in_team = marshaller.marshal_as_complete( documents_in_team )	
				else : 
					documents_out_in_team = marshaller.marshal_as_guest( documents_in_team )

	log.debug( "documents_out_in_team : \n %s", pformat(documents_out_in_team) )


	### DOCS USER IS NOT IN TEAM
	# retrieve docs from db
	cursor_not_team			= db_collection.find(pipeline_user_not_in_team)
	cursor_not_team_count	= cursor_not_team.count()
	if q_only_stats == False : 
		documents_not_team	= list(cursor_not_team)
		# log.debug( "documents_not_team : \n %s", pformat(documents_not_team) )
		# marshal out results
		if documents_not_team != [] :
			### trim list with pagimation
			if cursor_not_team_count > per_page : 
				documents_not_team = documents_not_team[ start_index : end_index ]
			
			if user_role in roles_for_complete : 
				documents_out_not_team = marshaller.marshal_as_complete( documents_not_team )			
			elif user_role == "anonymous" :
				documents_out_not_team = marshaller.marshal_as_min( documents_not_team )
			else : 
				documents_out_not_team = marshaller.marshal_as_guest( documents_not_team )

	log.debug( "documents_out_not_team : \n %s", pformat(documents_out_not_team) )


	### count results
	counts 		= {
		"all_docs_in_db" 			: db_collection.count() ,
		"docs_you_can_access" 		: cursor_accessible_count ,
		"docs_you_are_in_team" 		: cursor_in_team_count ,
		"docs_you_are_not_in_team" 	: cursor_not_team_count ,
	}


	### prepare a response message
	message  = "dear user, there is the list of {}s you can access given your credentials".format(document_type_full)


	return {
				"msg" 			: message,
				"counts"		: counts ,

				"data"			: {
					"docs_user_is_in_team" 	: documents_out_in_team , 
					"docs_user_not_in_team" : documents_out_not_team , 
				}, 

				"query"			: query_resume,

			}, response_code