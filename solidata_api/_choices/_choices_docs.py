
# -*- encoding: utf-8 -*-

"""
_choices_docs.py  
- all choices related to documents
"""
# from copy import copy, deepcopy

from log_config import log, pformat

log.debug("... loading _choices_docs.py ...")

### cf: http://flask.pocoo.org/docs/1.0/patterns/fileuploads/

doc_src_type_list 	= ["api","xls","xlsx","xml","csv"]

doc_type_list		= ["usr","prj","dmt","dmf","dsi","dsr","rec","dso","tag","lic"]

doc_type_dict		= {

	"usr" : "user",
	"prj" : "project",
	"dmt" : "datamodel_template",
	"dmf" : "datamodel_field",
	"dsi" : "dataset_input",
	"dsr" : "dataset_raw",
	"rec" : "recipe",
	"dso" : "dataset_output",
	"tag" : "tag",
	"lic" : "licence",
	
}