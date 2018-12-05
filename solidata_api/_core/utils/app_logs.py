# -*- encoding: utf-8 -*-

"""
app_logs.py  
"""


from log_config import log, pformat

log.debug("... loading app_logs.py ...")

from	bson.objectid import ObjectId
from 	datetime import datetime, timedelta
from 	solidata_api._core.queries_db import db_dict


def create_modif_log(	doc, 
						action, 
						dt						= datetime.utcnow(), 
						by						= None,
						val						= None,
					) :
	"""
	Create a simple dict for modif_log
	and insert it into document
	"""
	
	### store modification
	modif = {
		"modif_at" : dt, 
		"modif_for" : action 
	}

	### add author of modif
	if by != None :
		modif["modif_by"] = by
		
	if val != None :
			modif["modif_val"] = val

	doc["modif_log"].insert(0, modif)

	return doc


def add_to_datasets(coll, target_doc_oid, doc_type, oid_by, oid_to_add, include_is_fav=False) : 
	"""
  	expects all values as already stringified
	"""
	
	### select mongo collection
	mongo_coll = db_dict[coll]

	### add dsi ref to user
	doc_ = mongo_coll.find_one( {"_id" : ObjectId(target_doc_oid) } )

	### create ref to add to doc datasets
	new_ref_ 	= { 
		"oid_"+doc_type : oid_to_add,
		"added_by"		: oid_by ,
		"added_at"		: datetime.utcnow(),
	}
	if include_is_fav == True :
  		new_ref_["is_fav"]	= True

	doc_["datasets"][doc_type+"_list"].append(new_ref_)

	mongo_coll.save(doc_)	


def add_to_uses(coll, target_doc_oid, doc_type, oid_by) : 
	"""
  	expects all values as already stringified
	"""
	
	### select mongo collection
	mongo_coll = db_dict[coll]

	### add dsi ref to user
	doc_ = mongo_coll.find_one( {"_id" : ObjectId(target_doc_oid) } )

	### create ref to add to doc datasets
	new_ref_ 	= { 
		"used_by"	: oid_by ,
		"used_at"	: [datetime.utcnow()],
	}


	doc_["uses"]["by_"+doc_type].append(new_ref_)

	mongo_coll.save(doc_)	