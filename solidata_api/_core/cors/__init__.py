# -*- encoding: utf-8 -*-

"""
_core/cors/__init__.py  
"""

from log_config import log, pformat
print()
log.debug(">>> _core.cors.__init__.py ..." )

from flask import current_app as app

from solidata_api.application import CORS, cross_origin


### init CORS 
# cf : https://flask-cors.readthedocs.io/en/latest/api.html?highlight=Access-Control-Allow-Credentials
# cf : https://github.com/noirbizarre/flask-restplus/issues/54
# cf : https://github.com/criteo/biggraphite/commit/4379ae82a1ee2dbaad8aff11d890a0fffc300c63 

CORS(
	app, 
	# headers=['Content-Type', 'Authorization'], 
	resources={ 
		r"/api/*": {"origins": "*"}, 
		r"/swaggerui/*":{"origins": "*"} 
		},
	# send_wildcard=True,
	# expose_headers=['Access-Control-Allow-Origin', 'Origin'], 
	supports_credentials=True,
)
# log.debug("... cors :\n %s", pformat(CORS.__dict__))