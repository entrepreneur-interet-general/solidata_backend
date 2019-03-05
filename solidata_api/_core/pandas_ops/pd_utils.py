# -*- encoding: utf-8 -*-

"""
pd_utils.py  
"""

from log_config import log, pformat

log.debug("... loading pd_utils.py ...")

from . import pd, np

def cleanDfFromNans(df) :
  
	### clean df from NaNs
	df = df.dropna(how="all")
	df = df.replace({np.nan:None})  

	return df