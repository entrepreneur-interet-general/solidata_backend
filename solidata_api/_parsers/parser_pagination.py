# # -*- encoding: utf-8 -*-

# """
# parser_pagination.py  
# """

# from log_config import log, pformat

# from flask_restplus import reqparse

# log.debug("~ ~ ~ loading parser_pagination.py ...")


# pagination_arguments = reqparse.RequestParser()
# pagination_arguments.add_argument(
#   'page', 
#   type=int, 
#   required=False, 
#   default=1, 
#   help='Page number'
# )
# # pagination_arguments.add_argument(
# #   'bool', 
# #   type=bool, 
# #   required=False, 
# #   default=True, 
# #   help='Page number'
# # )
# pagination_arguments.add_argument(
#   'per_page', 
#   type=int, 
#   required=False, 
#   choices=[2, 10, 20, 30, 40, 50],
# 	default=10, 
#   help='Results per page {error_msg}'
# )