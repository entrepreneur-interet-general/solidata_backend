# -*- encoding: utf-8 -*-

"""
schema_pagination.py  
- provides the serializers for PAGINATION definition in DB and Flask-Restplus
"""

from log_config import log, pformat

from flask_restplus import fields

### cf : https://flask-restplus.readthedocs.io/en/stable/parsing.html 

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### pagination
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

'page'			= fields.Integer(description='Number of this page of results')
'pages' 		= fields.Integer(description='Total number of pages of results')
'per_page'		= fields.Integer(description='Number of items per page of results')
'total' 		= fields.Integer(description='Total number of results')
'has_next'		= fields.Boolean()
'has_prev'		= fields.Boolean()