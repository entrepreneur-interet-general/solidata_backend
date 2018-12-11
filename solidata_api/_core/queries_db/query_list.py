# -*- encoding: utf-8 -*-

"""
_core/queries_db/query_list.py  
"""

import re
import pandas as pd
from pandas.io.json import json_normalize

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

	### sum up all query arguments
	query_resume = {
		"document_type"		: document_type,	
		"user_id" 			: user_id,
		"user_role"			: user_role,
		"page_args"			: page_args,
		"query_args"		: query_args,
	}
	
	### get pagination arguments
	log.debug('page_args : \n%s', pformat(page_args) )  
	page 			= page_args.get('page', 	1 )
	per_page 		= page_args.get('per_page', 10 )
	if page != 1 :
		start_index		= ( page - 1 ) * per_page 
		end_index 		= start_index + per_page
	else : 
		start_index		= page - 1
		end_index 		= per_page - 1	

	### get query arguments
	log.debug('query_args : \n%s', pformat(query_args) )  
	# q_title 		= query_args.get('q_title', 		None )
	# q_description = query_args.get('q_description', 	None )
	q_search_for 	= query_args.get('search_for', 		None )
	q_oid_list		= query_args.get('oids',			None )
	# q_oid_tags		= query_args.get('tags',			None )
	q_only_stats	= query_args.get('only_stats',		False )
	q_ignore_team	= query_args.get('ignore_teams',	False )
	q_pivot			= query_args.get('pivot_results',	False )
	q_normalize		= query_args.get('normalize',	False )


	### pipelines for basic query
	pipeline_queries 	= {}
	pipe_concat			= []
	do_query_pipe 		= False


	# if q_oid_list != None :
	# 	q_oid_list_ = [ ObjectId(oid) for oid in q_oid_list ]
	# else :
	# 	q_oid_list_ = None
	# log.debug('q_oid_list_ : %s', q_oid_list_) 

	### search by oids 
	if q_oid_list != None : 
		if q_oid_list != []:  
			log.debug('q_oid_list : %s', q_oid_list) 
			do_query_pipe 		= True

			q_oid_list_ 		= [ ObjectId(oid) for oid in q_oid_list ]
			log.debug('q_oid_list_ : %s', q_oid_list_) 

			pipe_oids 			= { "_id" : { "$in" : q_oid_list_ } }
			# pipe_oids 			= { "_id" : { "$in" : q_oid_list } }
			log.debug('pipe_oids : %s', pipe_oids) 

			pipe_concat.append(pipe_oids)
			log.debug('pipe_concat + oid_list : %s', pipe_concat) 
	
	# if q_title != None : 
	# 	do_query_pipe 		= True
	# 	pipe_title 			= { "infos.title" : q_title }
	# 	pipe_concat.append(pipe_title)
	
	# if q_description != None : 
	# 	do_query_pipe 		= True
	# 	pipe_description 	= { "infos.description" : q_description }
	# 	pipe_concat.append(pipe_description)

	### search by string in indexed fields 
	if q_search_for != None : 
		if q_search_for != [] :
			log.debug('q_search_for : %s', q_search_for) 
			do_query_pipe 		= True
			search_words 		= [ '\"' + word + '\"' for word in search_words ]
			pipe_search_for 	= { '$text' : { '$search' : u' '.join(search_words) } }
			pipe_concat.append(pipe_search_for)
			log.debug('pipe_concat + search_for: %s', pipe_concat) 

	### build query
	if do_query_pipe : 
		log.debug('--> pipe_concat : %s', pipe_concat) 
		pipeline_queries = {
			"$or" : [ q for q in pipe_concat ]
		}
	log.debug('pipeline_queries : \n%s', pformat(pipeline_queries) )  


	### check query results at this point
	cursor_queries			= db_collection.find(pipeline_queries)
	cursor_queries_count	= cursor_queries.count()
	log.debug('cursor_queries_count : %s', cursor_queries_count) 


	### pipelines for : accessible / in_tem / not_in_team
	pipeline_accessible 	= { 
		**pipeline_queries, 
		**{	"public_auth.open_level_show" : { 
				"$in" : dft_open_level_show,
			} 
		}
	}
	pipeline_user_is_in_team 	= { 
		**pipeline_queries, 
		**{	"team" : { 
				"$elemMatch" : {
					"oid_usr" : user_oid
				}
			} 
		}
	}
	pipeline_user_not_in_team 	= { 
		**pipeline_queries, 
		**{ "public_auth.open_level_show" : { 
				"$in" : dft_open_level_show,
			},
			"team" : { 
				"$not" : {
					"$elemMatch" : {
						"oid_usr" : {
							"$in" : [ user_oid ]
						}
					}
				}
			} 
		}
	}

	### DOCS ACCESSIBLE
	# retrieve docs from db
	cursor_accessible			= db_collection.find(pipeline_accessible)
	# cursor_accessible			= cursor_queries.find(pipeline_accessible)
	cursor_accessible_count		= cursor_accessible.count()
	log.debug('cursor_accessible_count : %s', cursor_accessible_count) 

	### DOCS USER IS IN TEAM
	# retrieve docs from db
	if user_role != "anonymous" : 
		cursor_in_team 			= db_collection.find(pipeline_user_is_in_team)
		# cursor_in_team 			= cursor_queries.find(pipeline_user_is_in_team)
		cursor_in_team_count	= cursor_in_team.count()
		log.debug('cursor_in_team_count : %s', cursor_in_team_count) 
		cursor_in_team			= cursor_in_team.sort(  [ ("infos.title", 1)]  )
		
		if q_only_stats == False : 
			documents_in_team		= list(cursor_in_team)
			# log.debug( "documents_in_team : \n %s", pformat(documents_in_team) )
			# marshal out results
			if documents_in_team != [] :
					
				### trim list with pagination
				if per_page == 0 :
					pass
				elif cursor_in_team_count > per_page : 
					documents_in_team = documents_in_team[ start_index : end_index ]

				### choose marshalling
				if user_role in roles_for_complete : 
					documents_out_in_team = marshaller.marshal_as_complete( documents_in_team )	
				else : 
					documents_out_in_team = marshaller.marshal_as_guest( documents_in_team )

	# log.debug( "documents_out_in_team : \n %s", pformat(documents_out_in_team) )


	### DOCS USER IS NOT IN TEAM
	# retrieve docs from db
	cursor_not_team			= db_collection.find(pipeline_user_not_in_team)
	# cursor_not_team			= cursor_queries.find(pipeline_user_not_in_team)
	cursor_not_team_count	= cursor_not_team.count()
	log.debug('cursor_not_team_count : %s', cursor_not_team_count) 
	cursor_not_team			= cursor_not_team.sort(  [ ("infos.title", 1)]  )

	if q_only_stats == False : 
		documents_not_team	= list(cursor_not_team)
		# log.debug( "documents_not_team : \n %s", pformat(documents_not_team) )
		# marshal out results
		if documents_not_team != [] :
				
			### trim list with pagination
			if per_page == 0 :
				pass
			elif cursor_in_team_count > per_page : 
				documents_not_team = documents_not_team[ start_index : end_index ]

			### choose marshalling
			if user_role in roles_for_complete : 
				documents_out_not_team = marshaller.marshal_as_complete( documents_not_team )			
			elif user_role == "anonymous" :
				documents_out_not_team = marshaller.marshal_as_min( documents_not_team )
			else : 
				documents_out_not_team = marshaller.marshal_as_guest( documents_not_team )

	# log.debug( "documents_out_not_team : \n %s", pformat(documents_out_not_team) )


	### count results
	counts 		= {
		"all_docs_in_db" 			: db_collection.count() ,
		"docs_you_can_access" 		: cursor_accessible_count ,
		"docs_you_are_in_team" 		: cursor_in_team_count ,
		"docs_you_are_not_in_team" 	: cursor_not_team_count ,
	}


	### prepare a response message
	message  = "dear user, there is the list of {}s you can access given your credentials".format(document_type_full)

	### concatenate data into one single list if : q_ignore_team == True
	if q_ignore_team : 

		log.debug('q_ignore_team - concatenating lists...') 

		if cursor_in_team_count > 0 : 
			data_in = documents_out_in_team
		else :
			data_in = []
		
		if cursor_not_team_count > 0 : 
			data_not = documents_out_not_team
		else :
			data_not = []
		
		data = data_in + data_not
		log.debug('q_ignore_team - concatenating lists / finished ') 
		# log.debug( "data : \n %s", pformat(data) )

	else : 
		data = {
			"docs_user_is_in_team" 	: documents_out_in_team , 
			"docs_user_not_in_team" : documents_out_not_team , 
		}
		# log.debug( "data : \n %s", pformat(data) )



	### concatenate data into one single list if : q_ignore_team == True
	if q_pivot and q_ignore_team : 

		log.debug('\n q_pivot - pivot results with pandas...') 

		log.debug('q_pivot - data[0] : \n %s', data[0]) 
		data_df = json_normalize(data)
		data_df_indexed = data_df.set_index('_id')
		print ( "q_pivot / data_df_indexed.head(2) : \n%s", data_df_indexed.head(2) )

		data = data_df_indexed.to_dict()
		print ( "\n q_pivot / data[info.title]: \n%s", data["infos.title"] )


	if q_normalize :

		log.debug('\n q_normalize - nomralize results with pandas...') 
		data_df = json_normalize(data)
		data = data_df.to_dict('records')


	return {
				"msg" 			: message,
				"counts"		: counts ,
				"data"			: data, 
				"query"			: query_resume,
			}, response_code