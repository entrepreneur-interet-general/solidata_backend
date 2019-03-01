# -*- encoding: utf-8 -*-

"""
pd_read_files.py  
"""


from log_config import log, pformat

log.debug("... loading pd_read_files.py ...")

from . import pd

def cleanColumnName(colname, charsToReplace = u"°.[]", replaceWith="-" ): 
	log.debug("cleanColumnName / colname : %s", colname )
	colname_clean = colname
	for char in charsToReplace:
		colname_clean = colname_clean.replace( char ,replaceWith)
	log.debug("cleanColumnName / colname_clean : %s\n", colname_clean )
	return colname_clean

def read_file_with_pd ( uploaded_file, file_extension, sep="," ) : 
	
	if file_extension in ["csv", "tsv"] : 
		if file_extension == "tsv" : 
			sep = "\t"
		df = pd.read_csv(uploaded_file, sep=sep)

	elif file_extension in ["xls","xlsx"] : 
		df = pd.read_excel(uploaded_file)

	# elif file_extension in ["xml"] : 
	# 	### TO DO !!!
	# 	df = pd.read_excel(uploaded_file)

	### check if column names contain "." --> needs to be changed so bson could insert to db
	df_cols	= list(df.columns.values)
	df_cols_clean = { colname : cleanColumnName(colname) for colname in df_cols }
	df = df.rename( index=str, columns = df_cols_clean)

	return df 

