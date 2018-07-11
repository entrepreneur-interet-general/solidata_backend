


from datetime import datetime, timedelta

def create_modif_log( doc, action, field="log", nested_field="modified_log", dt=datetime.utcnow() ) :
	"""
	Create a simple dict for modif_log
	and insert it into document
	"""
	
	modif = {"modif_at" : dt, "modif_for" : action }
	doc[field][nested_field].insert(0, modif)

	return doc