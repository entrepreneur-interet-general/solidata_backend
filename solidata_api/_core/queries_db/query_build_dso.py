# -*- encoding: utf-8 -*-

"""
_core/queries_db/query_build_dso.py  
"""

from log_config import log, pformat
log.debug("... _core.queries_db.query_build_dso.py ..." )

from  	datetime import datetime, timedelta
from	bson.objectid 	import ObjectId
from 	flask_restplus 	import  marshal

from 	. 	import db_dict_by_type, Marshaller
from 	solidata_api._choices._choices_docs import doc_type_dict
from 	solidata_api._core.utils import merge_by_key, chain
from 	solidata_api._core.pandas_ops import pd, concat_dsi_list, prj_dsi_mapping_as_df

	
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### GLOBAL FUNCTION TO BUILD A DSO FROM A PRJ DOC FROM DB
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 

def Query_db_build_dso (
		ns, 
		models,
		doc_id,
		claims,
		roles_for_complete 	= ["admin"],
		payload				= {}
	):

	print()
	print("-+- "*40)
	log.debug("... _core.queries_db.query_build_doc.py ..." )

	### get mongodb collections
	prj_collection			= db_dict_by_type['prj']
	dmt_collection			= db_dict_by_type['dmt']
	dmf_collection			= db_dict_by_type['dmf']
	dsi_collection			= db_dict_by_type['dsi']
	dsi_doc_collection	= db_dict_by_type['dsi_doc']
	dso_collection			= db_dict_by_type['dso']
	dso_doc_collection	= db_dict_by_type['dso_doc']

	prj_type_full 			= doc_type_dict['prj']
	dso_type_full 			= doc_type_dict['dso']

	user_id = user_oid	= None
	user_role						= "anonymous"
	document_out				= None
	message 						= None
	response_code				= 200

	if claims or claims!={}  :
		user_role = claims["auth"]["role"]
		user_id	 	= claims["_id"] ### get the oid as str
		if user_role != "anonymous" : 
			user_oid 	= ObjectId(user_id)
			log.debug("user_oid : %s", user_oid )

	### retrieve PRJ from db
	if ObjectId.is_valid(doc_id) : 
		doc_oid			= ObjectId(doc_id)
		doc_prj 		= prj_collection.find_one( {"_id": doc_oid } )
		log.debug( "doc_prj PRJ : \n%s", pformat(doc_prj) )
	else :
		response_code	= 400
		doc_prj		= None

	### sum up all query arguments
	query_resume = {
		"document_type"			: 'prj',	
		"doc_id" 						: doc_id,
		"user_id" 					: user_id,
		"user_role"					: user_role,
		"is_member_of_team" : False,
		"payload" 					: payload
	}

	### if prj exists
	if doc_prj : 

		### check PRJ doc's specs : public_auth, team...
		doc_open_level_show = doc_prj["public_auth"]["open_level_show"]
		doc_open_level_edit = doc_prj["public_auth"]["open_level_edit"]
		log.debug( "doc_open_level_show : %s", doc_open_level_show )

		### get doc's team infos
		if "team" in doc_prj : 
			team_oids = [ t["oid_usr"] for t in doc_prj["team"] ]
			log.debug( "team_oids : \n%s", pformat(team_oids) )
			if user_oid in team_oids : 
				query_resume["is_member_of_team"] = True

		# for admin or members of the team --> complete infos model
		if user_role in roles_for_complete or user_oid in team_oids : 

			## get payload's args 
			log.debug( "payload : \n%s", pformat(payload) )

			print("-+- "*40)
			log.debug( "...and now let's build this DSO mate ! ..." )
			print("-+- "*40)

			## build an empty dso from marshall template
			dso_in = marshal( {} , models["model_doc_in"])

			### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
			### copy main infos from PRJ
			### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
			dso_in['_id'] 				= doc_oid
			dso_in['infos'] 			= doc_prj["infos"]
			dso_in['specs'] 			= {"doc_type" : "dso"}
			dso_in['public_auth']	= doc_prj["public_auth"]
			dso_in['datasets'] 		= doc_prj["datasets"]
			dso_in['team'] 				= doc_prj["team"]
			dso_in['mapping'] 		= doc_prj["mapping"]

			### update auto_fields 
			dso_auto_fields = { 
				"log"			: { 
					"created_at"	: datetime.utcnow(),
					"created_by"	: user_oid,
				},
				"uses"			: {
					"by_prj"		: [ 
						{
							"used_by" : doc_oid,
							"used_at" : [ 
								datetime.utcnow() 
							]
						} 
					]
				},
			}
			dso_in = { **dso_in, **dso_auto_fields }


			### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
			### get all DMF from PRJ's DMT
			### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

			### get prj's dmt (if not empty) - from prj/datasets/dmt_list
			dmt_refs = doc_prj["datasets"]["dmt_list"]
			if len(dmt_refs) > 0 : 
				dmt_oid = dmt_refs[0]["oid_dmt"]
				# log.debug( "dmt_oid : %s", pformat(dmt_oid) )
				dmt_doc	= dmt_collection.find_one({"_id" : dmt_oid }) 
				# log.debug( "dmt_doc : \n%s", pformat(dmt_doc) )

				### get dmt's dmfs (if not empty) - from dmt/datasets/dmf_list
				dmt_dmf_refs = dmt_doc["datasets"]["dmf_list"]
				if len(dmt_dmf_refs) > 0 :
					dmf_oids = [ dmf_ref["oid_dmf"] for dmf_ref in dmt_dmf_refs ]			
					# log.debug( "len(dmf_oids) : %s", len(dmf_oids) )
					# log.debug( "dmf_oids : \n%s", pformat(dmf_oids) )
					dmf_list_cursor = dmf_collection.find({"_id" : {"$in" : dmf_oids} })
					log.debug( "dmf_list_cursor.count() : %s", dmf_list_cursor.count() )
					log.debug( "dmf_list_cursor : \n%s", pformat(dmf_list_cursor) )

					### convert cursor into list
					dmf_list = list(dmf_list_cursor)
					# print()
					# for d in dmf_list : 
					# 	log.debug("d['_id'] : %s", d['_id'] )
					# 	log.debug("d['infos']['title'] : %s", d['infos']['title'] )
					# print()

					### dmf_list_light (referenced dmf for prj' dmt ) -> just list of pure oid_dmf from dmf_list (aka prj's dmt)
					dmf_list_light 	= [ d['_id'] for d in dmf_list ]
					log.debug( "dmf_list_light - prj's dmt's dmfs - from dmt/datasets/dmf_list : \n%s", pformat(dmf_list_light) )


					### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
					### get PRJ's mappers - dmf_to_open_level --> create DSO's headers
					### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

					### get prj's dmfs' mapping (if not empty) - from prj/mapping/dmf_to_open_level
					prj_dmf_mapping = doc_prj["mapping"]["dmf_to_open_level"]
					log.debug( "prj_dmf_mapping - from prj/mapping/dmf_to_open_level : \n%s", pformat(prj_dmf_mapping) )
					if len(prj_dmf_mapping) > 0 : 

						### lighten prj_dmf_mapping_ list (referenced dmf for prj' dmt ) -> just oid_dmf and open_level_show fields if dmf in dmf_list_light
						prj_dmf_mapping_ = [ { "oid_dmf" : d["oid_dmf"] , "open_level_show" : d["open_level_show"] } for d in prj_dmf_mapping if d["oid_dmf"] in dmf_list_light ]
						log.debug( "prj_dmf_mapping_ - exclude dmf not in dmf_list_light : \n%s", pformat(prj_dmf_mapping_) )
						
						### lighten prj_dmf_mapping_ list (referenced dmf for prj' dmt ) -> just list of pure oid_dmf
						dmf_list_from_map = [ d['oid_dmf'] for d in prj_dmf_mapping_ ]
						log.debug( "dmf_list_from_map : \n%s", pformat(dmf_list_from_map) )

						### get prj's dmfs' headers (if not empty) - from dmf_list (aka prj's dmt)
						headers_dso_from_dmf_list 	= [ 
							{ 	
								"oid_dmf" : d["_id"] , 
								"f_type" 	: d["data_raw"]["f_type"],
								"f_code" 	: d["data_raw"]["f_code"],
								"f_title" : d["infos"]["title"]
							} 
							for d in dmf_list if d["_id"] in dmf_list_from_map 
						]
						log.debug( "headers_dso_from_dmf_list : \n%s", pformat(headers_dso_from_dmf_list) )

						### merge prj_dmf_mapping_ and headers_dso_from_dmf_list
						headers_dso 			= list( merge_by_key( chain( prj_dmf_mapping_, headers_dso_from_dmf_list), 'oid_dmf') )
						log.debug( "headers_dso : \n%s", pformat(headers_dso) )

						### copy headers to dso_in
						dso_in["data_raw"]["f_col_headers"] = headers_dso


						### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
						### get PRJ's mappers - dsi_to_dmf --> filter out dmf not in dmf_list_light
						### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

						### get prj's dsis' mapping (if not empty) - from prj/mapping/dsi_to_dmf
						prj_dsi_mapping = doc_prj["mapping"]["dsi_to_dmf"]
						log.debug( "prj_dsi_mapping : \n%s", pformat(prj_dsi_mapping) )


						### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
						### get all DSI from PRJ's dataset - only mapped DSIs
						### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

						### dsis' doc list - from prj/datasets/dsi_list
						dsi_oids = [ dsi_ref["oid_dsi"] for dsi_ref in doc_prj["datasets"]["dsi_list"] ]
						log.debug( "dsi_oids : \n%s", pformat(dsi_oids) )
						if len(dsi_oids) > 0 and len(prj_dsi_mapping) : 
							dsi_list = dsi_collection.find({"_id" : {"$in" : dsi_oids} })
							log.debug( "dsi_list.count() : %s", dsi_list.count() )
							log.debug( "dsi_list : \n%s", pformat(dsi_list) )

							### prj_dsi_mapping to df + index
							# df_mapper_dsi_to_dmf = pd.DataFrame(prj_dsi_mapping)
							# dsi_mapped_list		 = list(df_mapper_dsi_to_dmf["oid_dsi"])
							# df_mapper_dsi_to_dmf = df_mapper_dsi_to_dmf.set_index(["oid_dsi","oid_dmf"])
							# print()
							# log.debug("... df_mapper_dsi_to_dmf ...")
							# print(df_mapper_dsi_to_dmf)
							dsi_mapped_list, df_mapper_dsi_to_dmf = prj_dsi_mapping_as_df(prj_dsi_mapping)

							### TO DO --> REFACTOR (cf query_solidify.py )
							### get all dsis' f_data
							dsi_raw_data_list = []
							for dsi in dsi_list :
								### check if at least one field of this dsi is mapped in df_mapper_dsi_to_dmf
								if dsi["_id"] in dsi_mapped_list : 
									# initiate dsi_data_raw
									dsi_data_raw = { 
										"f_col_headers" : dsi["data_raw"]["f_col_headers"], 
										"f_data" : [] 
									}
									# get corresponding docs in dsi_doc_collection
									dsi_docs = list(dsi_doc_collection.find({"oid_dsi" : dsi["_id"] }))
									# store as dataframe
									dsi_f_data = pd.DataFrame(dsi_docs)
									dsi_f_data_cols	= list(dsi_f_data.columns.values)
									f_col_headers_for_df = [ h for h in dsi_f_data_cols if h != "_id" ]
									dsi_f_data = dsi_f_data[ f_col_headers_for_df ]
									f_data = dsi_f_data.to_dict('records')
									dsi_data_raw["f_data"] = f_data

									# dsi_data_raw = dsi["data_raw"]
									dsi_raw_data_list.append( { "oid_dsi" : dsi["_id"], "data_raw" : dsi_data_raw } )
							# log.debug( "dsi_raw_data_list : \n%s", pformat(dsi_raw_data_list) )

							### reindex and concatenate all f_data from headers_dso and df_mapper_dsi_to_dmf with pandas
							if len(dsi_raw_data_list) > 0 :
								df_data_concat = concat_dsi_list(headers_dso, df_mapper_dsi_to_dmf, dsi_raw_data_list)

								### add PRJ/DSO oid entry to dso_f_data
								df_data_concat['oid_dso'] = doc_oid

								### get df_data_concat as a list
								dso_f_data = df_data_concat.to_dict('records')
								log.debug("... dso_f_data is composed ...")

							else : 
								dso_f_data = []
							log.debug("... dso_f_data is composed ...")
							log.debug("... dso_f_data[:5] : \n%s", pformat(dso_f_data[:5]))

							### copy f_data to dso_in
							# dso_in["data_raw"]["f_data"] 	= dso_f_data

							### flag dso as loaded
							dso_in["log"]["is_loaded"] 		= True


						else : 
							message = "dear user, the project can't be completly built : no dsi mapping or no dsi in project "

					else : 
						message = "dear user, the project can't be built : no dmf in dmt"

				else : 
					message = "dear user, the project can't be built : no dmt"

			else : 
				message = "dear user, you are not part of the team"


			### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
			### replace / upsert DSO built 
			### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
			# value_test_f_data = dso_in["data_raw"]["f_data"][0]
			value_test_f_data = dso_f_data[0]
			log.debug( "value_test_f_data : \n%s", pformat(value_test_f_data) )
			for k, v in value_test_f_data.items() : 
				print()
				log.debug("type(k) : %s", type(k))
				log.debug("type(v) : %s", type(v))
			log.debug("... preparing to replace / insert dso_in ...")

			_id = dso_collection.replace_one( {"_id" : doc_oid }, dso_in, upsert=True )
			log.info("dso_in has been created and stored in DB ...")
			log.info("_id : \n%s", pformat(str(_id) ) )
			



			### delete previous documents from dso_doc_collection
			log.info("deleting documents related to prj in dso_doc_collection ...")
			try :
				dso_doc_collection.delete_many({ 'oid_dso' : doc_oid })
			except : 
				pass

			### insert many docs in dso_docs for every entry of dso_f_data
			log.info("inserting documents related to prj in dso_doc_collection ...")
			if len(dso_f_data) > 0 and len(dso_f_data) < 2 :
				dso_doc_collection.insert_one( dso_f_data )
			else :
				dso_doc_collection.insert_many( dso_f_data )



			document_out 	= marshal( dso_in, models["model_doc_out"] )
			message 			= "the {} corresponding to the {} has been rebuilt".format(dso_type_full, prj_type_full) 


		# TO DO 
		# for other users
		else :

			if doc_open_level_show in ["commons", "open_data"] : 
			
				# for anonymous users --> minimum infos model
				if user_id == None or user_role == "anonymous" : 
					document_out = marshal( doc_prj, models["model_doc_min"] )
				
				# for registred users (guests) --> guest infos model
				else :
					document_out = marshal( doc_prj, models["model_doc_guest_out"] )

				log.debug( "document_out : \n %s", pformat(document_out) )
				message = "dear user, there is the {} you requested given your credentials".format(prj_type_full)

			else : 
				response_code	= 401
				### unvalid credentials / empty response
				message = "dear user, you don't have the credentials to build a dso from this {} with this oid : {}".format(prj_type_full, doc_id) 


	else : 
		### no doc_prj / empty response
		response_code	= 404
		message 		= "dear user, there is no {} with this oid : {}".format(prj_type_full, doc_id) 

	### return response
	return {
				"msg" 	: message ,
				# "data"	: document_out,
				"query"	: query_resume,
			}, response_code