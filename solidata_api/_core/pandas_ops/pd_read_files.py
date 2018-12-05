# -*- encoding: utf-8 -*-

"""
pd_read_files.py  
"""


from log_config import log, pformat

log.debug("... loading pd_read_files.py ...")

from . import pd

def read_file_with_pd ( uploaded_file, file_extension, sep="," ) : 
	
	if file_extension in ["csv", "tsv"] : 
		df = pd.read_csv(uploaded_file, sep=sep)

	elif file_extension in ["xls","xlsx"] : 
		df = pd.read_excel(uploaded_file)

	elif file_extension in ["xml"] : 
		### TO DO !!!
		df = pd.read_excel(uploaded_file)

	return df 

