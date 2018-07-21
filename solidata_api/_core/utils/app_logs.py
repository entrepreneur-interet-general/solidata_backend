# -*- encoding: utf-8 -*-

"""
app_logs.py  
"""


from log_config import log, pformat

log.debug("... loading app_logs.py ...")


from datetime import datetime, timedelta

def create_modif_log( doc, 
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
	modif = {"modif_at" : dt, "modif_for" : action }

	### add author of modif
	if by != None :
		modif["modif_by"] = by
		
	if val != None :
  		modif["modif_val"] = val

	doc["modif_log"].insert(0, modif)

	return doc