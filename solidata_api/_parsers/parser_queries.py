# # -*- encoding: utf-8 -*-

# """
# parser_queries.py  
# """

# from log_config import log, pformat

# from flask_restplus import reqparse

# log.debug("~ ~ ~ loading parser_queries.py ...")

# ### cf : https://flask-restplus.readthedocs.io/en/stable/parsing.html 

# query_arguments = reqparse.RequestParser()
# query_arguments.add_argument(
# 	'q_title', 
# 	action='append',
# 	type=str, 
# 	required=False, 
# 	help='find documents matching this string in the title'
# )
# query_arguments.add_argument(
# 	'q_description', 
# 	action='append',
# 	type=str, 
# 	required=False, 
# 	help='find documents matching this string in the description'
# )
# query_arguments.add_argument(
# 	'tags', 
# 	action='split',
# 	type=str, 
# 	required=False, 
# 	help='find documents matching this list of tags oid'
# )
# query_arguments.add_argument(
# 	'oids', 
# 	action='split',
# 	type=str, 
# 	required=False, 
# 	help='find documents matching this list of oid to find'
# )
# query_arguments.add_argument(
#   'only_stats', 
#   type=bool, 
#   required=False, 
#   default=False, 
#   help='just retrieve the stats of the result'
# )

