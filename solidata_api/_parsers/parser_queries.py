# -*- encoding: utf-8 -*-

"""
parser_queries.py  
"""

from log_config import log, pformat

from flask_restplus import reqparse

log.debug("~ ~ ~ loading parser_queries.py ...")

### cf : https://flask-restplus.readthedocs.io/en/stable/parsing.html 

query_arguments = reqparse.RequestParser()
query_arguments.add_argument(
	'q', 
	action='append',
	type=str, 
	required=False, 
	help='raw query string to find'
)
query_arguments.add_argument(
	'tags', 
	action='split',
	type=str, 
	required=False, 
	help='tags to find'
)
query_arguments.add_argument(
	'oid', 
	action='split',
	type=str, 
	required=False, 
	help='documents oid to find'
)


