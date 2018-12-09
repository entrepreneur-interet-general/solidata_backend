# -*- encoding: utf-8 -*-

"""
_choices_files.py  
- all choices related to files
"""


from log_config import log, pformat

log.debug("... loading _choices_files.py ...")



authorized_filetypes = [
	"csv", "xls", "xlsx", "xml" # ...
	"API"
]

authorized_mimetype = [ 
	"application/xls", "application/vnd.ms-excel",
	"text/csv", "application/csv", "text/x-csv",
	"application/xml",
]

authorized_separators = [
	",", ";", "|"
]