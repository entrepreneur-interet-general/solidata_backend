# -*- encoding: utf-8 -*-

"""
_choices_open_level.py  
- all choices related to open data levels
"""
# from copy import copy, deepcopy

from log_config import log, pformat

log.debug("... loading _choices_open_level.py ...")


open_level_choices = [
	"open_data",
	"commons",
	"collective",
	"private"
]

# open_level_rights = {
# 	"open_data"		: ["open_data"],
# 	"commons"			: ["open_data", "commons"] ,
# 	"collective"	: ["open_data", "commons", "collective"] ,
# 	"private"			: [""]
# }