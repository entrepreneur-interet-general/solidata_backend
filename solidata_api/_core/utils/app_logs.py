


from datetime import datetime, timedelta

def create_modif_log( doc, 
											action, 
											field="log", 
											nested_field="modified_log", 
											dt=datetime.utcnow(), 
											by=None ) :
	"""
	Create a simple dict for modif_log
	and insert it into document
	"""
	
	### store modification
	modif = {"modif_at" : dt, "modif_for" : action }

	### add author of modif
	if by != None :
		modif["modif_by"] = by

	doc[field][nested_field].insert(0, modif)

	return doc