
# -*- encoding: utf-8 -*-

"""
_choices_mapping.py  
- all choices related to document's mapping
"""
# from copy import copy, deepcopy

from log_config import log, pformat

log.debug("... loading _choices_mapping.py ...")

### cf: http://flask.pocoo.org/docs/1.0/patterns/fileuploads/

mapping_fields 	= [
	"dmf_to_open_level",
	"dsi_to_dmf",
	"dmf_to_rec",
	"rec_to_func"
]