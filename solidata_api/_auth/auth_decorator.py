# -*- encoding: utf-8 -*-

"""
auth_decorator.py  
- creates a token_required decorator
"""

from log_config import log, pprint, pformat
log.debug ("... loading token_required ...")

from functools import wraps
from flask import request

import jwt

def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
  		
		token = None

		if "X-API-KEY" in request.headers : 
			token = request.headers["X-API-KEY"]



		if not token :
			return {"message" : "token is missing"}, 401
		
		if token == False :
			return {"message" : "token is wrong..."}, 401 
		
		log.debug("TOKEN : {}".format(token))

		return f(*args, **kwargs)

	return decorated