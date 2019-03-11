
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

  ### for objects like dicts
  'object',

  ### for lists
  'list_strings',
  'list_integers',
  'list_floats',
  'list_objects',

  'id',
  
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

dmf_types_uniques = [
  'text',

  'tag',
  'category',
  
  'other'
]

dmf_type_objects = [
  'object_raw',
]

dmf_type_lists = [
  'list_strings',
  'list_integers',
  'list_floats',
  'list_objects',
]

