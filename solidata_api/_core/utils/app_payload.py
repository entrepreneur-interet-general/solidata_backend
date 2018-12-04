# -*- encoding: utf-8 -*-

"""
app_payload.py  
"""


from log_config import log, pformat

log.debug("... loading app_payload.py ...")


def return_payload(request, ns_payload) : 
	"""
	check if payload is a form, and if files are submitted
	"""

	### DEBUG check
	log.debug ("ns_payload : \n{}".format(pformat(ns_payload)))
	log.debug ("request.files : \n{}".format(pformat(request.files)))

	is_form	= False
	payload = ns_payload 
	form 	= request.form 
	files 	= request.files 

	if form : 
		is_form	= True
		payload = form

	log.debug ("payload 	 : \n{}".format(pformat(payload)))

	return payload, is_form, files