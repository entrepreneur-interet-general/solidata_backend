# -*- encoding: utf-8 -*-

"""
parser_queries.py  
- provides the QUERIES parser for 
	REST requests
"""

from flask_restplus import reqparse

query_arguments = reqparse.RequestParser()
query_arguments.add_argument(
  'q', 
  type=int, 
  required=False, 
  default=1, 
  help='raw query string'
)