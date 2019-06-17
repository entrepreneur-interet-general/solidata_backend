# -*- encoding: utf-8 -*-

"""
parser_classes.py  
"""

from log_config import log, pformat

from flask_restplus import reqparse, inputs
from werkzeug.datastructures import FileStorage

### cf : https://flask-restplus.readthedocs.io/en/stable/parsing.html 

log.debug("~ ~ ~ loading parser_classes.py ...")

from solidata_api._choices import *

"""
### cf : https://flask-restful.readthedocs.io/en/0.3.6/reqparse.html
default location for parsers 

	location : ('json', 'values'),
"""

class RequestParserBuilder :

	def __init__(	self, 
					add_pagination = False,
					add_slice_query = True,
					add_queries = False,
					add_data_query = False,
					add_map_query = False,
					add_filter_query = False,
					add_files = False,
				) : 

		self.baseParser = reqparse.RequestParser()

		self.baseParser.add_argument(
			'token', 
			type=str, 
			required=False, 
			default=None, 
			help='add token to slug to be able to retrieve more complete data from a DSO',
			# location = 'values'
		)

		if add_pagination : 

			self.baseParser.add_argument(
				'page', 
				type=int, 
				required=False, 
				default=1, 
				help='Page number',
				# location = 'values'
			)
			self.baseParser.add_argument(
				'per_page', 
				type=int, 
				required=False, 
				choices=[0, 1, 2, 3, 4, 5, 10, 20, 25, 50, 75, 100, 200, 300, 400, 500],
				default=10, 
				help='Results per page ( get all results if 0 )',
				# location = 'values'
			)

		if add_slice_query : 

			self.baseParser.add_argument(
				'slice_f_data', 
				type=inputs.boolean, 
				required=False, 
				default=True, 
				help='just retrieve a slice of the f_data',
				# location = 'values'
			)

		if add_queries : 

			# self.baseParser.add_argument(
			# 	'q_title', 
			# 	# action='append', ### multiple values
			# 	type=str, 
			# 	required=False, 
			# 	help='find documents matching this string in the title',
			# 	# location = 'values'
			# )
			# self.baseParser.add_argument(
			# 	'q_description', 
			# 	# action='append', ### multiple values
			# 	type=str, 
			# 	required=False, 
			# 	help='find documents matching this string in the description',
			# 	# location = 'values'
			# )
			self.baseParser.add_argument(
				'search_for', 
				action='append',
				type=str, 
				required=False, 
				help='find data in documents matching this string in records',
				# location = 'values'
			)
			self.baseParser.add_argument(
				'tags', 
				action='split',
				type=str, 
				required=False, 
				help='find documents matching this list of tags oid (separated by commas)',
				# location = 'values'
			)
			self.baseParser.add_argument(
				'oids', 
				action='split', ### expects string where values are separated by commas
				type=str, 
				required=False, 
				help='find documents matching this list of oid to find (separated by commas)',
				# location = 'values'
			)
			self.baseParser.add_argument(
				'only_stats', 
				type=inputs.boolean, 
				required=False, 
				default=False, 
				help='just retrieve the stats of the result',
				# location = 'values'
			)
			self.baseParser.add_argument(
				'ignore_teams', 
				type=inputs.boolean, 
				required=False, 
				default=False, 
				help='if true retrieve results mixing docs user is in the team or not',
				# location = 'values'
			)
			self.baseParser.add_argument(
				'pivot_results', 
				type=inputs.boolean, 
				required=False, 
				default=False, 
				help='pivot results',
				# location = 'values'
			)
			self.baseParser.add_argument(
				'normalize', 
				type=inputs.boolean, 
				required=False, 
				default=False, 
				help='normalize results',
				# location = 'values'
			)

		if add_map_query : 

			self.baseParser.add_argument(
				'map_list', 
				type=inputs.boolean, 
				required=False, 
				default=False, 
				help='get light results for map display : only sd_id, lat, lon',
				# location = 'values'
			)
			self.baseParser.add_argument(
				'as_latlng', 
				type=inputs.boolean, 
				required=False, 
				default=False, 
				help='coordinates as latlng tuple',
				# location = 'values'
			)
			self.baseParser.add_argument(
				'only_geocoded', 
				type=inputs.boolean, 
				required=False, 
				default=True, 
				help='retrieve only geocoded items',
				# location = 'values'
			)
			self.baseParser.add_argument(
				'geo_precision', 
				type=int, 
				required=False, 
				default=6, 
				choices=[0,1,2,3,4,5,6],
				help='precision of the coordinates as float numbers',
				# location = 'values'
			)

		if add_filter_query : 

			self.baseParser.add_argument(
				'get_filters', 
				type=inputs.boolean, 
				required=False, 
				default=False, 
				help='retrieve uniques values for each tag or category column in records',
				# location = 'values'
			)
			self.baseParser.add_argument(
				'get_uniques', 
				type=str, 
				required=False, 
				# default=None, 
				choices=dmf_types_uniques,
				help='retrieve uniques values for each column in records : text, tag, category, other',
				# location = 'values'
			)

		if add_data_query : 

			self.baseParser.add_argument(
				'search_for', 
				action='append',
				type=str, 
				required=False, 
				help='find data in documents matching this string in records',
				# location = 'values'
			)
			self.baseParser.add_argument(
				'search_in', 
				action='append',
				type=str, 
				required=False, 
				help='find data in document matching this string as field in records',
				# location = 'values'
			)
			self.baseParser.add_argument(
				'search_filters', 
				action='append',
				type=str, 
				required=False, 
				help='find data in document matching this kind of string : <field_name>__<valueToSearch>',
				# location = 'values'
			)
			self.baseParser.add_argument(
				'search_tags', 
				action='split',
				type=str, 
				required=False, 
				help='find documents matching this list of tags strings (separated by commas)',
				# location = 'values'
			)
			self.baseParser.add_argument(
				'search_int', 
				action='append',
				type=int, 
				required=False, 
				help='find data in document matching this integer in records',
				# location = 'values'
			)
			self.baseParser.add_argument(
				'search_float', 
				action='append',
				type=float, 
				required=False, 
				help='find data in document matching this float in records',
				# location = 'values'
			)
			self.baseParser.add_argument(
				'item_id', 
				action='append',
				type=str, 
				required=False, 
				help='find data inside the document matching this list of ids in records',
				# location = 'values'
			)
			# self.baseParser.add_argument(
			# 	'only_f_data', 
			# 	type=inputs.boolean, 
			# 	required=False, 
			# 	default=False, 
			# 	help='just retrieve the f_data of the result',
			# 	# location = 'values'
			# )
			self.baseParser.add_argument(
				'is_complete', 
				type=inputs.boolean, 
				required=False, 
				default=False, 
				help='just retrieve the complete f_data docs from the result',
				# location = 'values'
			)
			self.baseParser.add_argument(
				'only_stats', 
				type=inputs.boolean, 
				required=False, 
				default=False, 
				help='just retrieve the stats of the result',
				# location = 'values'
			)
			self.baseParser.add_argument(
				'sort_by', 
				type=str, 
				required=False, 
				help='sort data in document according to this field in records',
				# location = 'values'
			)
			self.baseParser.add_argument(
				'descending', 
				type=inputs.boolean, 
				required=False, 
				help='sort data in document ascending/descending',
				# location = 'values'
			)
			self.baseParser.add_argument(
				'shuffle_seed', 
				# action='append',
				type=int, 
				required=False, 
				default=None, 
				help='shuffle the list of results given a seed',
				# location = 'values'
			)
			self.baseParser.add_argument(
				'normalize', 
				type=inputs.boolean, 
				required=False, 
				default=False, 
				help='normalize results (aka data) in response',
				# location = 'values'
			)
			
		if add_files : 

			self.baseParser.add_argument(
				'data_file',  
				type=FileStorage, 
				# location=['files', 'form'], 
				location='files', 
				required=False, 
				help='any data file : tsv, csv, xml, xls, xlsx',
			)
			self.baseParser.add_argument(
				'csv_separator', 
				type=str, 
				required=False, 
				choices=[',',';','|'],
				default=',', 
				help='Separator',
				location = 'values'
			)
			# self.baseParser.add_argument(
			# 	'form_file',  
			# 	type=FileStorage, 
			# 	location='form', 
			# 	required=False, 
			# 	help='any data file : tsv, csv, xml, xls, xlsx',
			# )
			# self.baseParser.add_argument(
				# 'xls_file',  
				# type=FileStorage, 
				# location='files', 
				# required=False, 
				# help='XLS file',
			# )
			# self.baseParser.add_argument(
				# 'xlsx_file',  
				# type=FileStorage, 
				# location='files', 
				# required=False, 
				# help='XLSX file',
			# )
			# self.baseParser.add_argument(
				# 'csv_file',  
				# type=FileStorage, 
				# location='files', 
				# required=False, 
				# help='CSV file',
			# )
			# self.baseParser.add_argument(
				# 'xml_file',  
				# type=FileStorage, 
				# location='files', 
				# required=False, 
				# help='XML file',
			# )
			for field in [ 
					'title', 
					'description', 
					'licence', 
					'src_link'
				] : 
				self.baseParser.add_argument(
					field,
					location='form',
				)
			for field in [ 
					'open_level_show', 
					'open_level_edit', 
				] : 
				self.baseParser.add_argument(
					field, 
					location='form',
					choices=open_level_choices, 
					default="private"
				)
			for field in [ 
					'src_type', 
				] : 
				self.baseParser.add_argument(
					field, 
					location='form',
					choices=doc_src_type_list,
					default='csv'
				)
		

	@property
	def get_parser (self) : 
		return self.baseParser


q_minimal	= RequestParserBuilder()
query_min_arguments	= q_minimal.get_parser

q_arguments = RequestParserBuilder(add_queries=True)
query_arguments = q_arguments.get_parser
# log.debug(" query_arguments : \n%s ", pformat(query_arguments.args[0].__dict__ ))

q_data = RequestParserBuilder(add_data_query=True)
query_data_arguments = q_data.get_parser

q_files = RequestParserBuilder(add_files=True)
file_parser	= q_files.get_parser

q_pagination = RequestParserBuilder(add_pagination=True)
pagination_arguments = q_pagination.get_parser

q_pag_args = RequestParserBuilder(add_pagination=True, add_queries=True)
query_pag_args = q_pag_args.get_parser


q_data_dsi = RequestParserBuilder(add_pagination=True, add_slice_query=False, add_data_query=True)
query_data_dsi_arguments = q_data_dsi.get_parser

q_data_dso = RequestParserBuilder(add_pagination=True, add_slice_query=False, add_data_query=True, add_map_query=True, add_filter_query=True)
query_data_dso_arguments = q_data_dso.get_parser