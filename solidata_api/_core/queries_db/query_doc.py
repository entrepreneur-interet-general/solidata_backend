# -*- encoding: utf-8 -*-

"""
_core/queries_db/query_doc.py  
"""

import re
import random

import pandas as pd
from pandas.io.json import json_normalize

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

def build_first_term_query(dso_oid, query_args) : 
	""" 
	build query understandable by mongodb
	inspired by work on openscraper 
	""" 

	print()
	print("-+- "*40)
	log.debug( "... build_first_term_query " )

	log.debug('query_args : \n%s', pformat(query_args) )  

	search_for 		= query_args.get('search_for',	 	None )
	search_in 		= query_args.get('search_in', 		None )
	search_int 		= query_args.get('search_int', 		None )
	search_float 	= query_args.get('search_float', 	None )
	item_id 			= query_args.get('item_id', 			None )
	is_complete 	= query_args.get('is_complete', 	None )

	query = {'oid_dso' : dso_oid}

	### TO DO / TO FINISH ...

	# search by item_id
	if item_id != None :
		q_item = { "_id" : ObjectId(item_id)  } 
		query.update(q_item)

	### search by content --> collection need to be indexed
	# cf : https://stackoverflow.com/questions/6790819/searching-for-value-of-any-field-in-mongodb-without-explicitly-naming-it
	if search_for != None and search_for != [] and search_for != [''] :
		search_words = [ "\""+word+"\"" for word in search_for ]
		q_search_for = { "$text" : 
							{ "$search" : u" ".join(search_words) } # doable because text fields are indexed at main.py
		}
		query.update(q_search_for)
	
	return query


def get_dso_docs(doc_oid, query_args) : 
	"""
	get_dso_docs + search filters to f_data 
	"""

	print()
	print("-+- "*40)
	log.debug( "... get_dso_docs " )

	dso_doc_collection	= db_dict_by_type['dso_doc']

	query = build_first_term_query(doc_oid, query_args)
	log.debug('query : \n%s', pformat(query) )  

	# results = dso_doc_collection.find({'oid_dso' : doc_oid })
	cursor = dso_doc_collection.find(query)

	results = list(cursor)

	return results


def strip_f_data(	data_raw, 
									doc_open_level_show, 
									team_oids,
									created_by_oid,
									roles_for_complete, 
									user_role, 
									user_oid
								):
	""" 
	TO DO 
	strip f_data from fields not authorized for user
	""" 

	print()
	print("-+- "*40)
	log.debug( "... strip_f_data " )

	f_col_headers = data_raw["f_col_headers"] 
	f_data 				= data_raw["f_data"]

	if user_role in roles_for_complete : 
		pass

	else :

		### select f_col_headers given user auth
		
		if user_role == 'anonymous' : 
			f_col_headers_selected = [ h for h in f_col_headers if h["open_level_show"] in ["open_data"] ]
		
		elif user_oid in team_oids and user_oid != created_by_oid :
			f_col_headers_selected = [ h for h in f_col_headers if h["open_level_show"] in ["open_data", "commons", "collective"] ]
		
		elif user_oid == created_by_oid  : 
			f_col_headers_selected = f_col_headers

		else : 
			f_col_headers_selected = [ h for h in f_col_headers if h["open_level_show"] in ["open_data", "commons"] ]

		# log.debug('f_col_headers_selected : \n%s', pformat(f_col_headers_selected) )  

  	### load f_data as dataframe
		f_data_df 						= pd.DataFrame(f_data)
		log.debug('f_data_df.head(5) : \n%s', f_data_df.head(5) )  
		
		f_data_cols						= list(f_data_df.columns.values)
		log.debug('f_data_cols : \n%s', pformat(f_data_cols) )  

		f_col_headers_for_df 	= [ h["f_title"] for h in f_col_headers_selected if h["f_title"] in f_data_cols ]
		log.debug('f_col_headers_for_df : \n%s', pformat(f_col_headers_for_df) )  

		f_data_df_out 				= f_data_df[ f_col_headers_for_df ]
		f_data 								= f_data_df_out.to_dict('records')

		del f_data_df_out, f_data_df

	return f_data


def search_for_str( search_str, row) :

	print ()
	print ("= = =")
	log.debug( "search_str : %s", search_str )

	### TO DO : TREAT strings within "" and commas here 
	
	search_split = []
	for s in search_str :
		search_split += s.split() 
	search_reg = "|".join(search_split)
	log.debug( "search_reg : %s" , search_reg )

	### change series type as string
	row = row.astype(str)

	row_check = row.str.contains(search_reg, case=False, regex=True)
	
	if row.dtype.kind == 'O' : 
		log.debug( "row : \n%s", row )
		print ("- - -")
		log.debug( "row_check : \n%s", row_check )

	return row_check


def search_f_data (data_raw, query_args, not_filtered=True) :
	"""
	apply search filters to f_data 
	"""
	print()
	print("-+- "*40)
	log.debug( "... search_f_data " )

	f_data = data_raw["f_data"]

	if not_filtered :
  	### f_data is not a filtered result from direct db query

		log.debug('query_args : \n%s', pformat(query_args) )  
		search_for 		= query_args.get('search_for',	 	None )
		search_in 		= query_args.get('search_in', 		None )
		search_int 		= query_args.get('search_int', 		None )
		search_float 	= query_args.get('search_float', 	None )
		item_id 			= query_args.get('item_id', 			None )
		is_complete 	= query_args.get('is_complete', 	None )

		### use pandas to retrieve search results from 
		f_data_df = pd.DataFrame(f_data)
		f_data_df_cols = list(f_data_df.columns.values)
		log.debug( "... f_data_df_cols : \n%s", pformat(f_data_df_cols) )
		log.debug( "... f_data_df : \n%s", f_data_df.head(5) )
		
		if search_for is not None and search_for != [''] : 
			f_data_df = f_data_df[f_data_df.apply(lambda row: search_for_str(search_for, row) ).any(axis=1)]

		f_data = f_data_df.to_dict('records')

	return f_data


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

	### DEBUGGING
	print()
	print("-+- "*40)
	log.debug( "... Query_db_doc / document_type : %s", document_type )

	### prepare marshaller 
	# marshaller = Marshaller(ns, models)

	### default values
	not_filtered 				= True
	db_collection				= db_dict_by_type[document_type]
	document_type_full 	= doc_type_dict[document_type]
	user_id = user_oid	= None
	user_role						= "anonymous"
	document_out				= None
	message 						= None
	dft_open_level_show = ["open_data"]
	response_code				= 200

	if claims or claims!={}  :
		user_role 	= claims["auth"]["role"]
		user_id	 		= claims["_id"] ### get the oid as str
		if user_role != "anonymous" : 
			user_oid 		= ObjectId(user_id)
			log.debug("user_oid : %s", user_oid )
			dft_open_level_show += ["commons"]

	### sum up all query arguments
	query_resume = {
		"document_type"	: document_type,	
		"doc_id" 				: doc_id,
		"user_id" 			: user_id,
		"user_role"			: user_role,
		"page_args"			: page_args,
		"query_args"		: query_args,
		"is_member_of_team" : False,
		"is_creator" 		: False,
	}

	### get pagination arguments
	log.debug('page_args : \n%s', pformat(page_args) )  
	page 			= page_args.get('page', 	1 )
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
	only_f_data		= query_args.get('only_f_data',		False )
	only_stats		= query_args.get('only_stats',		False )
	slice_f_data	= query_args.get('slice_f_data',	True )
	sort_by				= query_args.get('sort_by',				None )
	descending		= query_args.get('descending',		False )
	shuffle_seed	= query_args.get('shuffle_seed',	None )
	q_normalize		= query_args.get('normalize',			False )


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
		doc_oid		= ObjectId(doc_id)
		document	= db_collection.find_one( {"_id": doc_oid })
		log.debug( "document._id : %s", str(document["_id"]) )
		# log.debug( "document : \n%s", pformat(document) )
	else :
		response_code	= 400
		document			= None



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

			log.debug( "... user_role in roles_for_complete or user_oid in team_oids or user_oid == created_by_oid " )

			document_out = marshal( document, models["model_doc_out"] )

			# flag as member of doc's team
			if user_oid == created_by_oid :
				query_resume["is_creator"] = True

			# flag as member of doc's team
			if user_oid in team_oids :
				query_resume["is_member_of_team"] = True

			# append "f_data" if doc is in ["dsi", "dsr", "dsr"]
			if document_type in ["dsi", "dsr", "dsr", "dso"] :
			
				log.debug( '...document_type : %s', document_type )
				log.debug( '...document["data_raw"]["f_data"][:1] : \n%s', pformat(document["data_raw"]["f_data"][:1]) )

				### copy f_data
				if document_type in ["dso"] :
						### strip f_data from not allowed fields
						not_filtered = False
						document_out["data_raw"]["f_data"] = get_dso_docs(doc_oid, query_args)
						document_out["data_raw"]["f_data"] = strip_f_data(	document_out["data_raw"], 
																				doc_open_level_show, 
																				team_oids,
																				created_by_oid,
																				roles_for_complete, 
																				user_role, 
																				user_oid
																			)
				else :
					document_out["data_raw"]["f_data"] = document["data_raw"]["f_data"]

				if len(document_out["data_raw"]["f_data"]) > 0 : 
					log.debug( 'document_out["data_raw"]["f_data"][0] : \n%s', pformat(document_out["data_raw"]["f_data"][0]) )

				### SEARCH QUERIES
				document_out["data_raw"]["f_data"] = search_f_data(document_out["data_raw"], query_args, not_filtered=not_filtered)

				### shuffle results
				if shuffle_seed != None :
					random.seed(shuffle_seed)
					random.shuffle(document_out["data_raw"]["f_data"])

				### sort results
				if sort_by != None :
					log.debug( 'sort_by : %s', sort_by )
					# NOT WORKING : document_out["data_raw"]["f_data"] = document_out["data_raw"]["f_data"].sort(key=operator.itemgetter(sort_by))
					# NOT WORKING WITH MISSING FIELDS : document_out["data_raw"]["f_data"] = sorted(document_out["data_raw"]["f_data"], key = lambda i: i[sort_by]) 
					document_out["data_raw"]["f_data"] = sort_list_of_dicts(document_out["data_raw"]["f_data"], sort_by)
					log.debug( '...document_out sorted' )

				# slice f_data
				if slice_f_data == True :
					log.debug( 'slice_f_data : %s', slice_f_data )
					document_out["data_raw"]["f_data"] = document_out["data_raw"]["f_data"][ start_index : end_index ]

				# add total of items within f_data in response
				document_out["data_raw"]["f_data_count"] = len(document_out["data_raw"]["f_data"])

			message = "dear user, there is the complete {} you requested ".format(document_type_full)

		# for other users
		else :

			log.debug( "... user_role NOT in roles_for_complete or user_oid in team_oids or user_oid == created_by_oid " )

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

					### copy f_data
					if document_type in ["dso"] :
  						### strip f_data from not allowed fields
							not_filtered = False
							document_out["data_raw"]["f_data"] = get_dso_docs(doc_oid, query_args)
							document_out["data_raw"]["f_data"] = strip_f_data(	document_out["data_raw"], 
																					doc_open_level_show, 
																					team_oids,
																					created_by_oid,
																					roles_for_complete, 
																					user_role, 
																					user_oid
																				)
					else :
						document_out["data_raw"]["f_data"] = document["data_raw"]["f_data"]
					
					if len(document_out["data_raw"]["f_data"]) > 0 : 
						log.debug( 'document_out["data_raw"]["f_data"][0] : \n%s', pformat(document_out["data_raw"]["f_data"][0]) )
					

					### SEARCH QUERIES
					document_out["data_raw"]["f_data"] = search_f_data(document_out["data_raw"], query_args, not_filtered=not_filtered)

					### shuffle results
					if shuffle_seed != None :
						random.seed(shuffle_seed)
						random.shuffle(document_out["data_raw"]["f_data"])

					### sort results
					if sort_by != None :
						log.debug( 'sort_by : %s', sort_by )
						# NOT WORKING : document_out["data_raw"]["f_data"] = document_out["data_raw"]["f_data"].sort(key=operator.itemgetter(sort_by))
						document_out["data_raw"]["f_data"] = sorted(document_out["data_raw"]["f_data"], key = lambda i: i[sort_by]) 
						log.debug( '...document_out sorted' )

					### slice f_data by default
					document_out["data_raw"]["f_data"] = document_out["data_raw"]["f_data"][ start_index : end_index ]
				
					# add total of items within f_data in response
					document_out["data_raw"]["f_data_count"] = len(document_out["data_raw"]["f_data"])
						
				message = "dear user, there is the {} you requested given your credentials".format(document_type_full)

			else : 
				response_code	= 401
				### unvalid credentials / empty response
				message = "dear user, you don't have the credentials to access/see this {} with this oid : {}".format(document_type_full, doc_id) 

		# normalize doc if needed
		if q_normalize :
		
			log.debug('\n q_normalize - nomralize results with pandas...') 
			data_df = json_normalize(document_out)
			document_out = data_df.to_dict('records')

	else : 
		### no document / empty response
		response_code	= 404
		message 			= "dear user, there is no {} with this oid : {}".format(document_type_full, doc_id) 
		document_out  = None


	log.debug('query_resume : \n%s', pformat(query_resume)) 

	### return response
	return {
				"msg" 	: message,
				"data"	: document_out,
				"query"	: query_resume,
			}, response_code