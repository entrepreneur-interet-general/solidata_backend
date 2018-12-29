# -*- encoding: utf-8 -*-

"""
_core/queries_db/query_update.py  
"""

from log_config import log, pformat
log.debug("... _core.queries_db.query_update.py ..." )

from  	datetime import datetime, timedelta
from	bson.objectid 	import ObjectId
from 	flask_restplus 	import  marshal

from 	. 	import db_dict_by_type, Marshaller
from 	solidata_api._choices._choices_docs import doc_type_dict


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### GLOBAL FUNCTION TO QUERY ONE DOC FROM DB
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 

def Query_db_update (
		ns, 
		models,
		document_type,
		doc_id,
		claims,
		roles_for_complete 	= ["admin"],
		payload 			= {}
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
			user_oid 	= ObjectId(user_id)
			log.debug("user_oid : %s", user_oid )
			dft_open_level_show += ["commons"]

	### retrieve from db
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
		doc_open_level_show = document["public_auth"]["open_level_show"]
		doc_open_level_edit = document["public_auth"]["open_level_edit"]
		log.debug( "doc_open_level_show : %s", doc_open_level_show )
		
		### get doc's team infos
		if "team" in document : 
			team_oids = [ t["oid_usr"] for t in document["team"] ]
			log.debug( "team_oids : \n%s", pformat(team_oids) )


		### marshal out results given user's claims / doc's public_auth / doc's team ... 
		

		# for admin or members of the team --> complete infos model
		if user_role in roles_for_complete or user_oid in team_oids or user_id == doc_id : 
			
			### add to list arg 
			log.debug( "payload : \n%s", pformat(payload) )
			
			for payload_data in payload : 
				
				log.debug( "payload_data : \n%s", pformat(payload_data) )

				field_to_update = payload_data["field_to_update"]
				log.debug( "field_to_update : %s", field_to_update )

				add_to_list = payload_data.get('add_to_list', False )
				is_mapping 	= payload_data.get('is_mapping', False )

				if is_mapping : 

					payload_map 		= {}
					delete_from_mapping = payload_data.get('del_mapping', False )

					# cf : https://stackoverflow.com/questions/10522347/mongodb-update-objects-in-a-documents-array-nested-updating 

					if field_to_update == "mapping.dmf_to_open_level" : 
						selector_f 								= field_to_update+".oid_dmf"
						selector_v 	= payload_map["oid_dmf"] 	= ObjectId( payload_data["id_dmf"] )
						selector 	= { selector_f : selector_v }
						payload_map["open_level_show"] 			= payload_data["open_level_show"]

					elif field_to_update == "mapping.dsi_to_dmf" : 
						selector_f 								= field_to_update+".dsi_header"
						selector_v 	= payload_map["dsi_header"] = payload_data["dsi_header"]
						selector_f_ 							= field_to_update+".oid_dsi"
						selector_v_ = payload_map["oid_dsi"] 	= ObjectId ( payload_data["id_dsi"] )
						selector 	= { selector_f : selector_v, selector_f_ : selector_v_ }
						if payload_data["id_dmf"] == "_ignore_" or delete_from_mapping : 
							# payload_map["oid_dmf"] 				= None
							pass
						else : 
							payload_map["oid_dmf"] 				= ObjectId( payload_data["id_dmf"] )

					elif field_to_update == "mapping.dmf_to_rec" : 
						selector_f 								= field_to_update+".oid_dmf"
						selector_v 	= payload_map["oid_dmf"] 	= ObjectId( payload_data["id_dmf"] )
						selector 	= { selector_f : selector_v }
						payload_map["oid_rec"] 					= ObjectId( payload_data["id_rec"] )

					elif field_to_update == "mapping.rec_to_func" : 
						selector_f 								= field_to_update+".oid_dmf"
						selector_v 	= payload_map["oid_rec"] 	= ObjectId( payload_data["id_rec"] )
						selector 	= { selector_f : selector_v }

					log.debug( "selector : \n%s", pformat(selector) )
					log.debug( "payload_map : \n%s", pformat(payload_map) )

					log.debug( "cursor : \n%s", pformat({ "_id"		: ObjectId(doc_id), **selector }) )

					### update mapping if selector_v already exists -> update array element

					log.debug( "update mapping / existing mapper... " )
					### $set from array if delete_mapping flag is False
					if not delete_from_mapping : 
						payload_set = { field_to_update+".$."+key : payload_map[key] for key in payload_map.keys() }
						doc_mapped = db_collection.update_one( 
							{ "_id"		: doc_oid, **selector }, 
							{ "$set" 	:  
								payload_set
								# { field_to_update+".$."+key : payload_map[key] for key in payload_map.keys() }
							}, 
						)
					### $pull from array if delete_mapping flag is True
					else : 
						payload_pull = payload_map
						doc_mapped = db_collection.update_one( 
							{ "_id"		: doc_oid, **selector }, 
							{ "$pull" : {
									field_to_update : payload_pull
								}
							}, 
						)
					log.debug( "...doc_mapped : \n%s ", pformat(doc_mapped) )
					log.debug( "...doc_mapped.matched_count : \n%s ", pformat(doc_mapped.matched_count) )

					# update mapping if selector_v doesn't exist -> add to array
					if doc_mapped.matched_count == 0 : 
						log.debug( "update mapping / non existing mapper... " )
						doc_mapped = db_collection.update_one( 
							{ "_id"		: doc_oid }, 
							{  "$addToSet"	:  
								{ field_to_update : payload_map }
							}, 
							upsert=True
						)
				
				elif add_to_list :

					log.debug( "add_to_list... " )

					### marshal payload as new entry in list - add 
					doc_added_type	= payload_data["doc_type"] 
					oid_item_field	= "oid_" + doc_added_type

					### update child document too in uses field ... 
					doc_added_oid 			= ObjectId( payload_data["field_value"] )
					db_collection_added 	= db_dict_by_type[ doc_added_type ]
					doc_added 				= db_collection_added.find_one( {"_id": doc_added_oid } )
					field_to_update_added 	= "uses.by_" + document_type
					
					### paylod for item 
					payload_ = {
						field_to_update : 
						{
							oid_item_field 	: doc_added_oid,
							"added_at" 		: datetime.utcnow() ,
							"added_by" 		: user_oid,
						}
					}
					### special payload_ for team updates
					if field_to_update == "team":

						log.debug( "updating team list ..." )

						# overwrite field_to_update_added
						field_to_update_added 	= "datasets." + document_type + "_list"

						### add extra special field when updating team field
						payload_["edit_auth"] 	= payload_data["edit_auth"]
						payload_["is_fav"] 		= True

					log.debug( "payload_ : \n%s", pformat(payload_) )

					### payload for added item
					payload_bis = {
						field_to_update_added : 
						{
							"used_at" : [ datetime.utcnow() ],
							"used_by" : doc_oid,
						}
					}
					log.debug( "payload_bis : \n%s", pformat(payload_bis) )

					### add_to_list
					if add_to_list == "add_to_list" :
    
						# check if subfield exists
						doc_list 	= document
						is_subfield = False
						try :
							for i in field_to_update.split('.'):
								doc_list = doc_list[i]
								is_subfield = True
						except : 
							is_subfield = False

						log.debug( "doc_list : \n%s", pformat(doc_list) )
						log.debug( "field_to_update.split('.')[-1] : %s", field_to_update.split('.')[-1] )
						log.debug( "doc_added_oid : %s", doc_added_oid )
						log.debug( "is_subfield : %s", is_subfield )
						
						# get existing list and check if doc_oid not already in list
						# cf : https://stackoverflow.com/questions/3897499/check-if-value-already-exists-within-list-of-dictionaries
						can_push = False
						if is_subfield :
							if not any(d.get( "oid_"+doc_added_type, None) == doc_added_oid for d in doc_list):
								can_push = True

						# if not any(d.get( "oid_"+doc_added_type, None) == doc_added_oid for d in doc_list):
						if can_push or not is_subfield : 
						
							## push in list 
							db_collection.update_one( 
								{ "_id"			: doc_oid }, 
								{ "$addToSet" 	: payload_ }, 
								upsert=True 
							)
							db_collection_added.update_one( 
								{ "_id"			: doc_added_oid }, 
								{ "$addToSet" 	: payload_bis }, 
								upsert=True 
							)

					### delete_from_list - 
					elif add_to_list == "delete_from_list" :

						log.debug( "field_to_update : %s", field_to_update )
						log.debug( "oid_item_field : %s", oid_item_field )
						log.debug( "field_to_update_added : %s", field_to_update_added )

						db_collection.update_one( 
							{ "_id": doc_oid }, 
							{ "$pull" : 
								{ field_to_update : { oid_item_field : doc_added_oid } } 
							}, 
						)
						db_collection_added.update_one( 
							{ "_id": doc_added_oid }, 
							{ "$pull" : 
								{ field_to_update_added : { "used_by" : doc_oid } } 
							}, 
						)

				else : 
					log.debug( "neither is_mapping nor add_to_list... " )
					payload_ = { field_to_update : payload_data["field_value"] }
					db_collection.update_one( 
						{ "_id"		: ObjectId(doc_id) }, 
						{ "$set" 	: payload_ }, 
						upsert=True 
					)

			document_updated 	= db_collection.find_one( {"_id": ObjectId(doc_id) } )
			document_out 		= marshal( document_updated, models["model_doc_out"] )

			# flag as member of doc's team
			if user_oid in team_oids :
				query_resume["is_member_of_team"] = True
		
			message = "dear user, there is the complete {} you requested ".format(document_type_full)



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