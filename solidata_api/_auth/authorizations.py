# -*- encoding: utf-8 -*-

"""
authorizations.py  
- describe authorizations

cf : https://flask-restplus.readthedocs.io/en/stable/swagger.html?highlight=authorizations#documenting-authorizations
"""

from log_config import log, pprint, pformat
log.debug (">>> _auth ... loading authorizations ...")

from flask import current_app as app #, request

authorizations = {
		'apikey': {
				'type'  : 'apiKey', 
				'in'    : 'header',
				'name'  : app.config["JWT_HEADER_NAME"], # 'X-API-KEY'
		},
}