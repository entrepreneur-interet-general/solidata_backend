# # -*- encoding: utf-8 -*-

# """
# parser_files.py  
# """

# from log_config import log, pformat

# from werkzeug.datastructures import FileStorage
# from flask_restplus import reqparse

# log.debug("~ ~ ~ loading parser_files.py ...")


# file_parser = reqparse.RequestParser()
# file_parser.add_argument('data_file',  
# 												 type=FileStorage, 
# 												 location='files', 
# 												 required=True, 
# 												 help='any data file : csv, xml, xls, xlsx')
# # file_parser.add_argument('xls_file',  
# #												 	 type=FileStorage, 
# # 												 location='files', 
# # 												 required=False, 
# # 												 help='XLS file')
# # file_parser.add_argument('xlsx_file',  
# #												 	 type=FileStorage, 
# # 												 location='files', 
# # 												 required=False, 
# # 												 help='XLSX file')
# # file_parser.add_argument('csv_file',  
# #												 	 type=FileStorage, 
# # 												 location='files', 
# # 												 required=False, 
# # 												 help='CSV file')
# # file_parser.add_argument('xml_file',  
# #												 	 type=FileStorage, 
# # 												 location='files', 
# # 												 required=False, 
# # 												 help='XML file')