# -*- encoding: utf-8 -*-

"""
parser_classes.py  
"""

from log_config import log, pformat

from flask_restplus import reqparse, inputs
from werkzeug.datastructures import FileStorage

### cf : https://flask-restplus.readthedocs.io/en/stable/parsing.html 

log.debug("~ ~ ~ loading parser_classes.py ...")


class RequestParserBuilder :

	def __init__(	self, 
					add_pagination 	= False,
					add_queries 	= False,
					add_files		= False
				) : 

		self.baseParser = reqparse.RequestParser()

		if add_pagination : 

			self.baseParser.add_argument(
				'page', 
				type=int, 
				required=False, 
				default=1, 
				help='Page number'
			)
			self.baseParser.add_argument(
				'per_page', 
				type=int, 
				required=False, 
				choices=[2, 10, 20, 30, 40, 50],
				default=10, 
				help='Results per page'
			)

		if add_queries : 

			self.baseParser.add_argument(
				'q_title', 
				action='append',
				type=str, 
				required=False, 
				help='find documents matching this string in the title'
			)
			self.baseParser.add_argument(
				'q_description', 
				action='append',
				type=str, 
				required=False, 
				help='find documents matching this string in the description'
			)
			self.baseParser.add_argument(
				'tags', 
				action='split',
				type=str, 
				required=False, 
				help='find documents matching this list of tags oid (separated by commas)'
			)
			self.baseParser.add_argument(
				'oids', 
				action='split',
				type=str, 
				required=False, 
				help='find documents matching this list of oid to find (separated by commas)'
			)
			self.baseParser.add_argument(
				'only_stats', 
				type=inputs.boolean, 
				required=False, 
				default=False, 
				help='just retrieve the stats of the result'
			)

		if add_files : 

			self.baseParser.add_argument(
				'data_file',  
				type=FileStorage, 
				location='files', 
				required=True, 
				help='any data file : tsv, csv, xml, xls, xlsx'
			)
			# self.baseParser.add_argument(
				# 'xls_file',  
				# type=FileStorage, 
				# location='files', 
				# required=False, 
				# help='XLS file'
			# )
			# self.baseParser.add_argument(
				# 'xlsx_file',  
				# type=FileStorage, 
				# location='files', 
				# required=False, 
				# help='XLSX file'
			# )
			# self.baseParser.add_argument(
				# 'csv_file',  
				# type=FileStorage, 
				# location='files', 
				# required=False, 
				# help='CSV file'
			# )
			# self.baseParser.add_argument(
				# 'xml_file',  
				# type=FileStorage, 
				# location='files', 
				# required=False, 
				# help='XML file'
			# )

	@property
	def get_parser (self) : 
		return self.baseParser


q_arguments 		= RequestParserBuilder(add_queries=True)
# log.debug(" q_arguments : \n%s ", pformat(q_arguments.__dict__))
query_arguments		= q_arguments.get_parser

q_files 			= RequestParserBuilder(add_files=True)
file_parser			= q_files.get_parser

q_pagination 		= RequestParserBuilder(add_pagination=True)
pagination_arguments = q_pagination.get_parser

q_pag_args 			= RequestParserBuilder(add_pagination=True, add_queries=True)
query_pag_args		= q_pag_args.get_parser
