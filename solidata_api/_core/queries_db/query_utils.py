# -*- encoding: utf-8 -*-

"""
_core/queries_db/query_utils.py  
"""

import re
import random

import pandas as pd
import 	numpy as np
from pandas.io.json import json_normalize

from log_config import log, pformat
log.debug("... _core.queries_db.query_doc.py ..." )

from	bson.objectid 	import ObjectId
from 	flask_restplus 	import  marshal

from 	. 	import db_dict_by_type, Marshaller
from 	solidata_api._choices._choices_docs import doc_type_dict
from 	solidata_api._choices._choices_f_types import dmf_types_list, dmf_type_categ
from solidata_api._core.pandas_ops.pd_utils import *

import operator


def removeKey(d, key):
  r = dict(d)
  del r[key]
  return r

def weighted(nb):
  
  if nb is None:
    # return -float('inf')
    return ''
  else:
    # return nb
    return str(nb)
  # return -float('inf') if nb is None else nb


def append_filters_to_query(query, search_filters, splitter="__") : 
  """
  build a dict from search_filters argument 
  """
  filters_dict = {}

  if search_filters != None :
    for q in search_filters : 
      splitted = q.split(splitter)
      filters_field = { splitted[0] : [] }
      filters_dict.update( filters_field )
    for q in search_filters :
      splitted = q.split(splitter)
      filters_dict[splitted[0]].append(splitted[1])

  if filters_dict != {}: 

    query["$and"] = []

    for key, values in filters_dict.items():
      
      q_filters = { "$or" : [] }
      
      regex_string = [ u".*"+word+".*" for word in values ] 
      new_filters = [{ key : { "$regex" : reg , "$options": "-i" } } for reg in regex_string ]
      
      q_filters["$or"] = new_filters

      query["$and"].append(q_filters)

  log.debug('query : \n%s', pformat(query) )
  return query

def sort_list_of_dicts(list_to_sort, key_value, is_reverse=True) :
  # return sorted(list_to_sort, key = lambda i: i[key_value]) 
  return sorted(list_to_sort, key=lambda i:weighted(i[key_value]), reverse=is_reverse)

def build_first_term_query(ds_oid, query_args, field_to_query="oid_dso") : 
  """ 
  build query understandable by mongodb
  inspired by work on openscraper 
  """ 

  print()
  print("-+- "*40)
  log.debug( "... build_first_term_query " )

  query = { field_to_query : ds_oid }

  log.debug('query_args : \n%s', pformat(query_args) )  

  search_for 		= query_args.get('search_for',	 	None )
  search_in 		= query_args.get('search_in', 		None )
  search_int 		= query_args.get('search_int', 		None )
  search_float 	= query_args.get('search_float', 	None )
  search_tags 	= query_args.get('search_tags', 	None )
  item_id 			= query_args.get('item_id', 			None )
  is_complete 	= query_args.get('is_complete', 	None )
  search_filters = query_args.get('search_filters', [] )


  ### TO FINISH ...
  ### append filters
  if search_filters != None and search_filters != [] : 
    query = append_filters_to_query( query, search_filters )


  # search by item_id
  if item_id != None :
    q_item = { "_id" : { "$in" : [ ObjectId(i_id) for i_id in item_id ] }}
    query.update(q_item)

  ### TO DO  ...
  # search by tags
  if search_tags != None :
    pass
    # q_tag = { "_id" : ObjectId(item_id)  } 
    # query.update(q_tag)

  ### search by content --> collection need to be indexed
  # cf : https://stackoverflow.com/questions/6790819/searching-for-value-of-any-field-in-mongodb-without-explicitly-naming-it
  if search_for != None and search_for != [] and search_for != [''] :
    search_words = [ "\""+word+"\"" for word in search_for ]
    q_search_for = { "$text" : 
              { "$search" : u" ".join(search_words) } # doable because text fields are indexed at main.py
    }
    query.update(q_search_for)
  
  return query

def build_projected_fields(ignore_fields_list=[], keep_fields_list=[] ) :
  """ 
  projection of the query 
  """
  ### cf : https://docs.mongodb.com/manual/tutorial/project-fields-from-query-results/

  print()
  print("-+- "*40)
  log.debug( "... build_projected_fields " )

  # add ignore_fields / keep_fields criterias to query if any
  projected_fields = None

  if ignore_fields_list != [] or keep_fields_list != [] : 
    
    projected_fields = {}
    
    # add fields to ignore
    if ignore_fields_list != [] :
      ignore_fields = { f : 0 for f in ignore_fields_list }
      projected_fields.update( ignore_fields )
    
    # add fields to retrieve
    if keep_fields_list != [] :
      keep_fields = { f : 1 for f in keep_fields_list }
      projected_fields.update( keep_fields )

  return projected_fields

def get_ds_docs(doc_oid, query_args, db_coll="dso_doc", f_col_headers=[] ) : 
  """
  get_ds_docs + search filters to f_data 
  """

  print()
  print("-+- "*40)
  log.debug( "... get_ds_docs " )
  log.debug( "... f_col_headers : \n%s", pformat(f_col_headers) )

  filters_field = ""
  keep_fields_list = []
  ignore_fields_list = []

  map_list = query_args.get('map_list',	False )
  get_filters = query_args.get('get_filters',	False )
  get_uniques = query_args.get('get_uniques',	None )

  if db_coll == "dso_doc" :
    field_to_query = "oid_dso"
  if db_coll == "dsi_doc" :
    field_to_query = "oid_dsi"

  ds_doc_collection	= db_dict_by_type[db_coll]

  query = build_first_term_query(doc_oid, query_args, field_to_query=field_to_query)
  log.debug('query : \n%s', pformat(query) )  
  
  if map_list : 
    keep_fields_list = ["_id", field_to_query, "lat", "lon"]
  
  if get_filters and db_coll == "dso_doc" :
    if get_uniques == None : 
      list_filters = dmf_type_categ
    else :
      list_filters = [ get_uniques ]
    keep_fields_list = [ h["f_title"] for h in f_col_headers if h["f_type"] in list_filters ]
  
  log.debug('keep_fields_list : \n%s', pformat(keep_fields_list) )  
  projected_fields = build_projected_fields(ignore_fields_list, keep_fields_list)
  log.debug('projected_fields : \n%s', pformat(projected_fields) )  

  # results = ds_doc_collection.find({'oid_dso' : doc_oid })
  cursor = ds_doc_collection.find(query, projected_fields)

  results = list(cursor)
  log.debug('results[0] : \n%s', pformat(results[0]) )  

  if get_filters : 
    u_values = []
    for h in keep_fields_list : 
      u_list = list(set( str(dic[h]) for dic in results if h in dic.keys() )) 
      u_val_fields = { h : u_list }
      u_values.append(u_val_fields)
    results = u_values

  return results

def strip_f_data(	data_raw, 
                  doc_open_level_show, 
                  team_oids,
                  created_by_oid,
                  roles_for_complete, 
                  user_role, 
                  user_oid,
                  document_type="dso"
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

  ### load f_data as dataframe
  f_data_df = pd.DataFrame(f_data)
  log.debug('f_data_df.head(5) : \n%s', f_data_df.head(5) )  


  ### select f_col_headers given user auth
  if document_type == "dso" : 

    if user_role == 'anonymous' : 
      f_col_headers_selected = [ h for h in f_col_headers if h["open_level_show"] in ["open_data"] ]

    elif user_oid in team_oids and user_oid != created_by_oid :
      f_col_headers_selected = [ h for h in f_col_headers if h["open_level_show"] in ["open_data", "commons", "collective"] ]

    elif user_oid == created_by_oid  : 
      f_col_headers_selected = f_col_headers

    elif user_role in roles_for_complete : 
      f_col_headers_selected = f_col_headers 

    else : 
      f_col_headers_selected = [ h for h in f_col_headers if h["open_level_show"] in ["open_data", "commons"] ]

      # log.debug('f_col_headers_selected : \n%s', pformat(f_col_headers_selected) )  

  elif document_type == "dsi" : 
    f_col_headers_selected = f_col_headers 
    
  f_data_cols = list(f_data_df.columns.values)
  log.debug('f_data_cols : \n%s', pformat(f_data_cols) )  

  if document_type == "dsi" : 
    f_col_headers_for_df 	= [ h["f_coll_header_val"] for h in f_col_headers_selected ]
  elif document_type == "dso" : 
    f_col_headers_for_df 	= [ h["f_title"] for h in f_col_headers_selected if h["f_title"] in f_data_cols ]
    
  ### append "_id" column to authorized columns
  f_data_df["_id"] = f_data_df["_id"].apply(lambda x: str(x))
  f_data_df = f_data_df.rename( index=str, columns = {"_id" : "sd_id"})
  f_col_headers_for_df.append("sd_id")

  log.debug('f_col_headers_for_df : \n%s', pformat(f_col_headers_for_df) )  
  f_data_df_out = f_data_df[ f_col_headers_for_df ]

  ### clean f_data_df_out from NaNs
  # f_data_df_out = f_data_df_out.dropna(how="all")
  f_data_df_out = f_data_df_out.replace({np.nan:None})  

  ### transform f_data to dict
  f_data = f_data_df_out.to_dict('records')

  del f_data_df_out, f_data_df

  return f_data

def search_for_str( search_str, row) :

  ### TO DO : TREAT strings within "" and commas here 

  search_split = []
  for s in search_str :
    search_split += s.split() 
  search_reg = "|".join(search_split)
  # log.debug( "search_reg : %s" , search_reg )

  ### change series type as string
  row = row.astype(str)

  row_check = row.str.contains(search_reg, case=False, regex=True)
  
  # if row.dtype.kind == 'O' : 
  # 	log.debug( "search_str : %s", search_str )
  # 	log.debug( "row : \n%s", row )
  # 	print ("- - -")
  # 	log.debug( "row_check : \n%s", row_check )

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

    ### convert Nan to None
    f_data_df = f_data_df.replace({np.nan:None})

    f_data = f_data_df.to_dict('records')
    log.debug( "... f_data[0] : \n%s ", pformat(f_data[0]) )

  return f_data

def latLngTuple(f_data, query_args) : 

  map_list	= query_args.get('map_list',	False )
  
  ### map listing required
  if map_list : 

    as_latlng	= query_args.get('as_latlng',	False )
    geo_precision	= query_args.get('geo_precision',	6 )
    only_geocoded	= query_args.get('only_geocoded',	True )

    f_data_tupled = []

    for d in f_data : 
      d_keys = list(d.keys())
      has_geo = False
      if "lat" in d_keys and "lon" in d_keys : 
        if d["lat"]!= 'None' and d["lon"]!='None' : 
          has_geo = True
          d["lat"] = round(float(d["lat"]), geo_precision)
          d["lon"] = round(float(d["lon"]), geo_precision)
          if as_latlng : 
            d["latlng"] = ( d["lat"], d["lon"]) 
            d = removeKey(d, "lat")
            d = removeKey(d, "lon")
        else : 
            d = removeKey(d, "lat")
            d = removeKey(d, "lon")

      if only_geocoded == False : 
        f_data_tupled.append(d)
      else :
        if has_geo : 
          f_data_tupled.append(d)
  
  ### map_list not required
  else : 
    f_data_tupled = f_data
  
  return f_data_tupled

def GetFData( document_type, 
              can_access_complete, not_filtered,
              document, document_out, doc_oid, doc_open_level_show,
              team_oids, created_by_oid, roles_for_complete, user_role, user_oid,
              page_args, query_args,
            ) : 
              # start_index, end_index
              # shuffle_seed, sort_by, slice_f_data, 
  """ 
  refactoring getting f_data 
  """
  ### get pagination arguments
  log.debug('page_args : \n%s', pformat(page_args) )  
  page     = page_args.get('page', 	1 )
  per_page = page_args.get('per_page', 5 )
  if page != 1 :
    start_index		= ( page - 1 ) * per_page 
    end_index 		= start_index + per_page
  else : 
    start_index		= 0
    end_index 		= per_page	
  log.debug('start_index : %s', start_index )  
  log.debug('end_index   : %s', end_index )  

  # ### get query arguments
  # log.debug('query_args : \n%s', pformat(query_args) )  
  # only_f_data		= query_args.get('only_f_data',		False )
  # only_stats		= query_args.get('only_stats',		False )
  slice_f_data	 = query_args.get('slice_f_data',	True )
  sort_by				 = query_args.get('sort_by',				None )
  descending		 = query_args.get('descending',		False )
  shuffle_seed	 = query_args.get('shuffle_seed',	None )
  # q_normalize		= query_args.get('normalize',			False )
  map_list			 = query_args.get('map_list',	False )
  get_filters    = query_args.get('get_filters',	False )

  # append "f_data" if doc is in ["dsi", "dsr", "dsr"]
  if document_type in ["dsi", "dso"] and can_access_complete :
    
    ### override slice_f_data in case doc is dsi or dso to avoid overloading the api or the client
    slice_f_data = True 

    log.debug( '...document_type : %s', document_type )
    # log.debug( '...document["data_raw"]["f_data"][:1] : \n%s', pformat(document["data_raw"]["f_data"][:1]) )
    # log.debug( '...document["data_raw"] : \n%s', pformat(document["data_raw"]) )
    
    ### copy f_data
    if document_type in ["dso", "dsi"] :
        
        ### strip f_data from not allowed fields
        not_filtered = False
        if document_type == "dso" :	
          db_coll="dso_doc"
          document_out["data_raw"]["f_col_headers"].append(
            {	
              'f_title' : '_id',
              'open_level_show' : 'sd_id',
              'f_type' : 'id'
            }
          )
        elif document_type == "dsi" : 
          db_coll="dsi_doc"
          document_out["data_raw"] = {"f_col_headers" : document["data_raw"]["f_col_headers"]}
          document_out["data_raw"]["f_col_headers"].append(
            {	
              'f_coll_header_text': 'sd_id',
              'f_coll_header_val': 'sd_id'
            }
          )
        document_out["data_raw"]["f_data"] = get_ds_docs(
                                    doc_oid, 
                                    query_args, 
                                    db_coll=db_coll,
                                    f_col_headers=document["data_raw"]["f_col_headers"]
                                  )
        if get_filters == False :
          document_out["data_raw"]["f_data"] = strip_f_data(	
                                      document_out["data_raw"], 
                                      doc_open_level_show, 
                                      team_oids,
                                      created_by_oid,
                                      roles_for_complete, 
                                      user_role, 
                                      user_oid,
                                      document_type=document_type
                                    )
          document_out["data_raw"]["f_data"] = latLngTuple(document_out["data_raw"]["f_data"], query_args)
    else :
      document_out["data_raw"]["f_data"] = document["data_raw"]["f_data"]

    # if len(document_out["data_raw"]["f_data"]) > 0 : 
    # 	log.debug( 'document_out["data_raw"]["f_data"][0] : \n%s', pformat(document_out["data_raw"]["f_data"][0]) )

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
      document_out["data_raw"]["f_data"] = sort_list_of_dicts(document_out["data_raw"]["f_data"], sort_by, is_reverse=descending)
      log.debug( '...document_out sorted' )

    # add total of items within f_data in response
    document_out["data_raw"]["f_data_count"] = len(document_out["data_raw"]["f_data"])

    # slice f_data
    if slice_f_data == True and map_list == False and get_filters == False :
      log.debug( 'slice_f_data : %s', slice_f_data )
      document_out["data_raw"]["f_data"] = document_out["data_raw"]["f_data"][ start_index : end_index ]
      # document_out["data_raw"]["f_data"] = document_out["data_raw"]["f_data"][ 0 : 1 ]

    # only f_data
    # if only_f_data : 
    # 	document_out = document_out["data_raw"]["f_data"]

    
  return document_out


def check_if_prj_is_buildable (doc_prj) :
  """ 
  check if prj has enough mapping to be buildable
  """

  print("-+- "*40)
  log.debug( "... check_if_prj_is_buildable ... " )

  is_buildable = False

  prj_dmt 		= doc_prj["datasets"]["dmt_list"]
  prj_dsi 		= doc_prj["datasets"]["dsi_list"]
  prj_map_open 	= doc_prj["mapping"]["dmf_to_open_level"]
  prj_map_dsi 	= doc_prj["mapping"]["dsi_to_dmf"]

  ### check if prj contains dmt and dsi
  if len(prj_dmt)>0 and len(prj_dsi)>0 :

    log.debug( "... lengths prj_dmt & prj_map_dsi : OK ... " )

    ### check if prj contains dmt and dsi
    if len(prj_map_open)>0 and len(prj_map_dsi)>0 :

      log.debug( "... lengths prj_map_open & prj_map_dsi : OK ... " )

      ### set of unique values of dmf from prj_map_open
      prj_dsi_set 	= { d['oid_dsi'] for d in prj_dsi }
      log.debug( "... prj_dsi_set : \n%s : ", pformat(prj_dsi_set) )

      ### set of unique values of dmf from prj_map_open
      prj_map_dmf_set 		= { d['oid_dmf'] for d in prj_map_open }
      log.debug( "... prj_map_dmf_set : \n%s : ", pformat(prj_map_dmf_set) )

      ### unique values of dsi from prj_map_dsi
      prj_map_dsi_dict 		= { d['oid_dsi'] : { "dmf_list" : [] } for d in prj_map_dsi }
      for d in prj_map_dsi : 
        prj_map_dsi_dict[ d['oid_dsi'] ]["dmf_list"].append( d["oid_dmf"] )
      log.debug( "... prj_map_dsi_dict : \n%s : ", pformat(prj_map_dsi_dict) )

      ### set of unique values of dmf for each dsi from prj_map_dsi_dict
      prj_map_dsi_sets 		= { k : set(v['dmf_list']) for k,v in prj_map_dsi_dict.items() }
      log.debug( "... prj_map_dsi_sets : \n%s : ", pformat(prj_map_dsi_sets) )

      ### check if dmf in prj_map_dsi are in prj_map_open
      dsi_mapped_not_in_prj 					= 0
      dsi_mapped_but_no_dmf_mapped_in_prj_map = 0

      for dsi_oid, dsi_dmf_mapped_set in prj_map_dsi_sets.items() : 
        
        log.debug( "... dsi_oid : %s ", dsi_oid )
        
        if dsi_oid in prj_dsi_set :
          ### check if dsi_dmf_mapped_set contains at least 1 dmf from prj_map_dmf_set
          log.debug( "... dsi_dmf_mapped_set : \n%s ", pformat(dsi_dmf_mapped_set) )
          log.debug( "... prj_map_dmf_set : \n%s ", pformat(prj_map_dmf_set) )
          intersection 		= dsi_dmf_mapped_set & prj_map_dmf_set
          log.debug( "... intersection : %s ", intersection )
          len_intersection 	= len(intersection)
          if len_intersection == 0 :
            dsi_mapped_but_no_dmf_mapped_in_prj_map += 1

        else :
          dsi_mapped_not_in_prj += 1
      
      log.debug( "... dsi_mapped_not_in_prj : %s ", dsi_mapped_not_in_prj )
      log.debug( "... dsi_mapped_but_no_dmf_mapped_in_prj_map : %s ", dsi_mapped_but_no_dmf_mapped_in_prj_map )

      if dsi_mapped_but_no_dmf_mapped_in_prj_map == 0 :
        is_buildable = True

  return is_buildable
