
# -*- encoding: utf-8 -*-

"""
_choices_f_types.py  
- all choices related to documents
"""
# from copy import copy, deepcopy

from log_config import log, pformat

log.debug("... loading _choices_f_types.py ...")


dmf_types_list = [
	'text',
	'email',
	'float',
	'integer',
	'date',
	'price',

	'address',
	'geoloc',

	'tag',
	'category',

	'media_link',
	'hyperlink',

	'boolean',
	
	'other'
]

dmf_type_int = [
	'integer',
]
dmf_type_float = [
	'float',
	'price',
]
dmf_type_boolean = [
	'boolean',
]
dmf_type_date = [
	'date',
]
dmf_type_categ = [
	'tag',
	'category',
]




