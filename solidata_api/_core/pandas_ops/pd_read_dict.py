# -*- encoding: utf-8 -*-

"""
pd_read_dict.py  
"""


from log_config import log, pformat

log.debug("... loading pd_read_dict.py ...")

from . import pd


def read_dict_with_pd ( uploaded_json ) : 
	
	df = pd.DataFrame(uploaded_json)

	return df 