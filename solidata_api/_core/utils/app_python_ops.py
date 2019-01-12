# -*- encoding: utf-8 -*-

"""
app_python_ops.py  
"""


from log_config import log, pformat

log.debug("... loading app_python_ops.py ...")


### cf : https://codereview.stackexchange.com/questions/74462/merge-two-dict-in-separate-list-by-id
from itertools import chain
from collections import defaultdict


def merge_by_key(dicts, key):
    
	merged = defaultdict(dict)

	for dict_ in dicts:
		merged[dict_[key]].update(dict_)

	return merged.values()