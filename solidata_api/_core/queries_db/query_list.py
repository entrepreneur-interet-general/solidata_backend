# -*- encoding: utf-8 -*-

"""
_core/queries_db/query_list.py  
"""

from log_config import log, pformat
log.debug("... _core.queries_db.query_list.py ..." )

from	bson.objectid import ObjectId

from 	. 	import db_dict_by_type, Marshaller
from 	solidata_api._choices._choices_docs import doc_type_dict



# ### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
# ### SERIALIZERS
# ### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
# class Marshaller :

# 	def __init__( self, ns, models ):
    	
# 		self.ns 					= ns
# 		self.model_doc_out 			= models["model_doc_out"]
# 		self.model_doc_guest_out 	= models["model_doc_guest_out"]
# 		self.model_doc_min		 	= models["model_doc_min"]

# 		self.results_list			= None 

# 	def marshal_as_complete (self, results_list ) :

# 		ns 					= self.ns
# 		self.results_list 	= results_list
# 		log.debug('results_list : \n%s', pformat(results_list) )  
		
# 		@ns.marshal_with(self.model_doc_out)
# 		def get_results():
# 			return results_list
# 		return get_results()

# 	def marshal_as_guest (self, results_list ) :
    
# 		ns 					= self.ns
# 		self.results_list 	= results_list
# 		log.debug('results_list : \n%s', pformat(results_list) )  
		
# 		@ns.marshal_with(self.model_doc_guest_out)
# 		def get_results():
# 			return results_list
# 		return get_results()

# 	def marshal_as_min (self, results_list ) :
    
# 		ns 					= self.ns
# 		self.results_list 	= results_list
# 		log.debug('results_list : \n%s', pformat(results_list) )  
		
# 		@ns.marshal_with(self.model_doc_min)
# 		def get_results():
# 			return results_list
# 		return get_results()


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### GLOBAL FUNCTION TO QUERY LIST FROM DB
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
# def Query_db_list_test(document_type) :
# 	log.debug('... Query_db_list_test')
# 	log.debug('document_type : %s', document_type )   


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

	### get user's role and _id
	# user_id 	= get_jwt_identity() ### get the oid as str
	if claims or claims!={}  :
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
	cursor_in_team 			= db_collection.find(pipeline_user_is_in_team)
	cursor_in_team_count	= cursor_in_team.count()
	log.debug('cursor_in_team_count : %s', cursor_in_team_count) 
	if q_only_stats : 
		documents_in_team		= list(cursor_in_team)
		# log.debug( "documents_in_team : \n %s", pformat(documents_in_team) )
		# marshal out results
		if documents_in_team != [] :
			if cursor_in_team_count > per_page : 
				documents_in_team = documents_in_team[ start_index : end_index ]
			
			documents_out_in_team = marshaller.marshal_as_complete( documents_in_team )
			# documents_out_in_team = _documents_out_in_team.marshal_as_complete()
	log.debug( "documents_out_in_team : \n %s", pformat(documents_out_in_team) )


	### DOCS USER IS NOT IN TEAM
	# retrieve docs from db
	cursor_not_team			= db_collection.find(pipeline_user_not_in_team)
	cursor_not_team_count	= cursor_not_team.count()
	if q_only_stats : 
		documents_not_team	= list(cursor_not_team)
		# log.debug( "documents_not_team : \n %s", pformat(documents_not_team) )
		# marshal out results
		if documents_not_team != [] :
			### trim list with pagimation
			if cursor_in_team_count > per_page : 
				documents_not_team = documents_not_team[ start_index : end_index ]
			
			if user_role in roles_for_complete : 
				documents_out_not_team = marshaller.marshal_as_complete( documents_not_team )
				# documents_out_not_team =_documents_out_not_team.marshal_as_complete()
			else : 
				documents_out_not_team = marshaller.marshal_as_guest( documents_not_team )
				# documents_out_not_team = _documents_out_not_team.marshal_as_min()
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

			}