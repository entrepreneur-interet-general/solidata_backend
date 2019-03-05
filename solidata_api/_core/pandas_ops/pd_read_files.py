# -*- encoding: utf-8 -*-

"""
pd_read_files.py  
"""


from log_config import log, pformat

log.debug("... loading pd_read_files.py ...")

from . import pd, np
from solidata_api._core.pandas_ops.pd_utils import *

def cleanColumnName(colname, charsToReplace = u"°.[]", replaceWith="-" ): 
	log.debug("cleanColumnName / colname : %s", colname )
	colname_clean = colname.replace( '"' , "'")
	for char in charsToReplace:
		colname_clean = colname_clean.replace( char ,replaceWith)
	log.debug("cleanColumnName / colname_clean : %s\n", colname_clean )
	return colname_clean

def cleanColNames(df, charsToReplace = u"°.[]", replaceWith="-" ):
    df_cols = list(df.columns.values)
    df_cols_clean = { 
			colname : cleanColumnName(colname,charsToReplace=charsToReplace,replaceWith=replaceWith) 
			for colname in df_cols 
		}
    df = df.rename( index=str, columns = df_cols_clean)
    return df

def read_file_with_pd ( uploaded_file, file_extension, sep=",", encoding = "utf-8" ) : 

	if file_extension in ["csv", "tsv"] : 
		if file_extension == "tsv" : 
			sep = "\t"
		log.debug("uploaded_file : %s", uploaded_file)
		try : 
			df = pd.read_csv(uploaded_file, sep=sep, encoding=encoding)
		except : 
			df = pd.read_csv(uploaded_file, sep=sep)

	elif file_extension in ["xls","xlsx"] : 
		df = pd.read_excel(uploaded_file, encoding=encoding)

	elif file_extension in ["xml"] : 
		pass
	# 	### TO DO !!!
	# 	df = pd.read_excel(uploaded_file)

	### check if column names contain "." --> needs to be changed so bson could insert to db
	# df_cols	= list(df.columns.values)
	# df_cols_clean = { colname : cleanColumnName(colname) for colname in df_cols }
	# df = df.rename( index=str, columns = df_cols_clean)
	df = cleanColNames(df, charsToReplace = u"°.[]", replaceWith="-")

	### clean df from NaNs
	# df = df.dropna(how="all")
	# df = df.replace({np.nan:None})  
	df = cleanDfFromNans(df)

	return df 

