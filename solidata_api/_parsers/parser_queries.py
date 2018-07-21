# -*- encoding: utf-8 -*-

"""
parser_queries.py  
"""

from log_config import log, pformat

from flask_restplus import reqparse

log.debug("~ ~ ~ loading parser_queries.py ...")


query_arguments = reqparse.RequestParser()
query_arguments.add_argument(
	'q', 
	type=int, 
	required=False, 
	default=1, 
	help='raw query string'
)
