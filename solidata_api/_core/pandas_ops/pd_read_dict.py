# -*- encoding: utf-8 -*-

"""
pd_read_dict.py  
"""


from log_config import log, pformat

log.debug("... loading pd_read_dict.py ...")

from . import pd


def read_dict_with_pd ( uploaded_json ) : 
	
	df = pd.DataFrame(uploaded_json)

	df_cols = list(df.columns.values)
	df_cols_clean = {}
	for h in df_cols :
		if h=="_id" : 
			df_cols_clean[h]="id"
		else:
			df_cols_clean[h]=h
	df = df.rename( index=str, columns = df_cols_clean)

	return df 