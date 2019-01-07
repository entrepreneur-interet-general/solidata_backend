# -*- encoding: utf-8 -*-

"""
_core/queries_db/query_insert_doc.py  
"""

from log_config import log, pformat
log.debug("... _core.queries_db.query_insert_doc.py ..." )

from  	datetime import datetime, timedelta
from	bson.objectid 	import ObjectId
from 	flask_restplus 	import  marshal

from 	. 	import db_dict_by_type, Marshaller
from 	solidata_api._choices._choices_docs import doc_type_dict


from solidata_api.config_default_docs import default_system_user_list

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### GLOBAL FUNCTION TO INSERT ONE DOC FROM DB
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 

def Query_db_insert (
		ns, 
		models,
		document_type,

		new_doc,

		value_to_check,
		field_to_check="infos.title",

		roles_for_complete 	= ["system", "admin"],
		user_role   		= "system"
	):

	print()
	print("-+- "*40)
	log.debug("... _core.queries_db.query_insert_doc.py ... %s", document_type )
	
	### default values
	db_collection		= db_dict_by_type[document_type]
	document_type_full 	= doc_type_dict[document_type]

	filter_doc = { field_to_check : value_to_check }
	log.debug('filter_doc : %s', pformat(filter_doc) )  

	### check if doc already exists 
	document 		= db_collection.find_one( filter_doc )
	log.debug('document : \n%s', pformat(document) )  


	### retrieve system user's OID
	system_user = db_dict_by_type['usr'].find_one( { 'auth.role' : user_role } )
	log.debug('system_user : \n%s', pformat(system_user) )  

	# check if system user exists
	# system_user exists
	if system_user : 

		log.debug('system_user exists ...' )  
		user_oid	= system_user["_id"]

	# no system user 
	else : 
		log.debug('system_user is None ...' )  
		
		### create a dummy system user which is gonna be replaced
		new_system_user = db_collection.insert( default_system_user_list[0] )
		log.debug('system_user : %s', new_system_user )  
		user_oid		= ObjectId(new_system_user)


	### marshall infos with new_doc complete model
	new_doc_in 		= marshal( new_doc , models["model_doc_in"])
	log.debug('new_doc_in : \n%s', pformat(new_doc_in) )  
	
	### complete missing default fields
	if document_type != "usr" :
		new_doc_auto_fields = { 
			"public_auth"	: {
				"open_level_edit"	: "private",
				"open_level_show"	: "open_data",
			},
			"log"			: { 
				"created_at"	: datetime.utcnow(),
				"created_by"	: user_oid,
			},
			"uses"			: {
				"by_usr"		: [ 
					{
						"used_by" : user_oid,
						"used_at" : [ 
							datetime.utcnow() 
						]
					} 
				]
			},
			"team"			: [ 
				{
					'oid_usr'	: user_oid,
					'edit_auth'	: "owner",
					'added_at'  : datetime.utcnow(),
					'added_by'  : user_oid,
				}
			],
		}
	### SYSTEM USR
	else : 
		new_doc_auto_fields = { 
			"public_auth"	: {
				"open_level_edit"	: "private",
				"open_level_show"	: "private",
			},
			"log"			: { 
				"created_at"	: datetime.utcnow(),
				"created_by"	: user_oid,
			},
			"team"			: []
		}
	log.debug('new_doc_auto_fields : \n%s', pformat(new_doc_auto_fields) )  

	### update marshalled infos by concatenating with auto fields
	new_doc_in 	= { **new_doc_in, **new_doc_auto_fields }
	log.debug('new_doc_in : \n%s', pformat(new_doc_in) )  

	### save/replace new_doc_in in db 
	_id = db_collection.replace_one( filter_doc, new_doc_in, upsert=True )
	log.info("new_doc_in has being created and stored in DB ...")
	log.info("_id : \n%s", pformat(str(_id) ) )