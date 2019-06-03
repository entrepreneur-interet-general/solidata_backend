# -*- encoding: utf-8 -*-

"""
_core/queries_db/query_doc.py  
"""

import re
import random

import pandas as pd
import numpy as np
from pandas.io.json import json_normalize

from log_config import log, pformat
log.debug("... _core.queries_db.query_doc.py ..." )

from	bson.objectid 	import ObjectId
from 	flask_restplus 	import  marshal

from 	. 	import db_dict_by_type, Marshaller
from 	solidata_api._choices._choices_docs import doc_type_dict

import operator

from .query_utils import * 

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
  not_filtered = True
  db_collection = db_dict_by_type[document_type]
  document_type_full = doc_type_dict[document_type]
  user_id = user_oid = None
  user_role	= "anonymous"
  document_out = None
  message	= None
  dft_open_level_show = ["open_data"]
  response_code	= 200
  can_access_complete = True

  if claims or claims!={}  :
    user_role = claims["auth"]["role"]
    user_id   = claims["_id"] ### get the oid as str
    if user_role != "anonymous" : 
      user_oid = ObjectId(user_id)
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
  # log.debug('page_args : \n%s', pformat(page_args) )  
  # page     = page_args.get('page', 	1 )
  # per_page = page_args.get('per_page', 5 )
  # if page != 1 :
  # 	start_index		= ( page - 1 ) * per_page 
  # 	end_index 		= start_index + per_page
  # else : 
  # 	start_index		= 0
  # 	end_index 		= per_page	
  # log.debug('start_index : %s', start_index )  
  # log.debug('end_index   : %s', end_index )  

  ### get query arguments
  log.debug('query_args : \n%s', pformat(query_args) )  
  only_f_data		= query_args.get('only_f_data',		False )
  only_stats		= query_args.get('only_stats',		False )
  # slice_f_data	= query_args.get('slice_f_data',	True )
  # sort_by				= query_args.get('sort_by',				None )
  # descending		= query_args.get('descending',		False )
  # shuffle_seed	= query_args.get('shuffle_seed',	None )
  q_normalize		= query_args.get('normalize',			False )


  ### TO FINISH !!!
  """ ### prepare pipelines 
    pipeline_queries		= {
      "$or" : [
        { "infos.title" : q_value_str },
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
        "$not" : {
          "$elemMatch" : {
            "oid_usr" : {
              "$in" : [ user_oid ]
            }
          }
        }
      } 
    }
  """

  ### retrieve from db
  if ObjectId.is_valid(doc_id) : 
    doc_oid	 = ObjectId(doc_id)
    document = db_collection.find_one( {"_id": doc_oid })
    # log.debug( "document._id : %s", str(document["_id"]) )
    # log.debug( "document : \n%s", pformat(document) )
  else :
    response_code	= 400
    document = None



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

      ### append "f_data" if doc is in ["dsi", "dsr", "dsr"]
      document_out = GetFData( document_type, 
            can_access_complete, not_filtered,
            document, document_out, doc_oid, doc_open_level_show,
            team_oids, created_by_oid, roles_for_complete, user_role, user_oid,
            page_args, query_args,
            # shuffle_seed, sort_by, slice_f_data, 
            # start_index, end_index
      )
      message = "dear user, there is the complete {} you requested ".format(document_type_full)

    # for other users
    else :
  
      log.debug( "... user_role NOT in roles_for_complete or user_oid in team_oids or user_oid == created_by_oid " )

      if doc_open_level_show in ["commons", "open_data"] : 
      
        ### for anonymous users --> minimum infos model
        if user_id == None or user_role == "anonymous" : 
          document_out = marshal( document, models["model_doc_min"] )
          if doc_open_level_show != "open_data" : 
            can_access_complete = False
        
        ### for registred users (guests) --> guest infos model
        else :
          document_out = marshal( document, models["model_doc_guest_out"] )
        

        ### append "f_data" if doc is in ["dsi", "dsr", "dsr"]
        document_out = GetFData( document_type, 
              can_access_complete, not_filtered,
              document, document_out, doc_oid, doc_open_level_show,
              team_oids, created_by_oid, roles_for_complete, user_role, user_oid,
              page_args, query_args,
              # shuffle_seed, sort_by, slice_f_data, 
              # start_index, end_index
        )
        message = "dear user, there is the {} you requested given your credentials".format(document_type_full)

      else : 
        response_code	= 401
        ### unvalid credentials / empty response
        message = "dear user, you don't have the credentials to access/see this {} with this oid : {}".format(document_type_full, doc_id) 

    # normalize doc if needed
    if q_normalize :
    
      log.debug('\n q_normalize - normalize results with pandas...') 
      data_df = json_normalize(document_out)
      document_out = data_df.to_dict('records')
      del data_df

  else : 
    ### no document / empty response
    response_code	= 404
    message 			= "dear user, there is no {} with this oid : {}".format(document_type_full, doc_id) 
    document_out  = None


  log.debug('query_resume : \n%s', pformat(query_resume)) 
  # log.debug( 'document_out["data_raw"]["f_data"][0] : \n%s', pformat(document_out["data_raw"]["f_data"][0]) )
  log.debug( 'document_out : \n%s', pformat(document_out) )

  ### return response
  return {
        "msg" 	: message,
        "data"	: document_out,
        "query"	: query_resume,
      }, response_code