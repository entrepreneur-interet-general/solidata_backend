# -*- encoding: utf-8 -*-

"""
pd_concat_prj.py  
"""


from log_config import log, pformat

log.debug("... loading pd_concat_prj.py ...")

from . import pd, np
from solidata_api._choices._choices_f_types import *
from solidata_api._core.pandas_ops.pd_utils import *


def prj_dsi_mapping_as_df(prj_dsi_mapping) : 
	""" 
	prj_dsi_mapping to df + index
	""" 
	print()
	print( "- prj_dsi_mapping " + "-\- "*40)
	log.debug("... run prj_dsi_mapping_as_df ...")
	log.debug("... prj_dsi_mapping :\n %s", prj_dsi_mapping)  
	
	df_mapper_dsi_to_dmf 	= pd.DataFrame(prj_dsi_mapping)
	log.debug("... df_mapper_dsi_to_dmf :\n %s", df_mapper_dsi_to_dmf)  

	dsi_mapped_list		 		= list(set(df_mapper_dsi_to_dmf["oid_dsi"]))
	df_mapper_dsi_to_dmf 	= df_mapper_dsi_to_dmf.set_index(["oid_dsi","oid_dmf"]).sort_index()
	print()
	log.debug("... df_mapper_dsi_to_dmf ...")
	print(df_mapper_dsi_to_dmf)

	print("-\- "*40)
	return dsi_mapped_list, df_mapper_dsi_to_dmf



def convert_col_types (df_light, df_map_) : 
	""" 
	convert dataframe columns' types 
	depending on prj's dmf_list
	""" 

	# cf : https://stackoverflow.com/questions/15891038/change-data-type-of-columns-in-pandas/28648923

	print()
	print("-/- "*40)
	log.debug("... convert_col_types ...")

	### get back df_map_
	print()
	log.debug("... df_map_ ...")
	print(df_map_)

	### convert columns types depending on df_map_ 
	print()
	log.debug("... df_light ...")
	print(df_light.head(3))

	df_light = df_light.astype('object')

	for col in df_light.columns :

		print()
		log.debug("... col : %s", col)

		### get back f_type for corresponding header
		f_type = df_map_.loc[col]["f_type"]
		log.debug("... f_type : %s", f_type)

		if f_type in dmf_type_int or f_type in dmf_type_float :
			
			df_light[col] = pd.to_numeric(df_light[col], errors='coerce')
			print( df_light.head() )

			if f_type in dmf_type_int :
				df_light.loc[col] = df_light[col].astype('int')

			if f_type in dmf_type_float :
				df_light[col] = df_light[col].astype('float')


		if f_type in dmf_type_boolean :
			df_light[col] = df_light[col].astype('bool')

		if f_type in dmf_type_date :
			# cf : http://pandas.pydata.org/pandas-docs/stable/generated/pandas.to_datetime.html#pandas.to_datetime
			df_light[col] = pd.to_datetime(df_light[col], infer_datetime_format=True, errors='coerce')

		### TO FINISH
		# if f_type in dmf_type_categ :
		# 	df_light[col] = df_light[col].astype('str')

		if f_type in dmf_type_lists :
			# df_light[col] = df_light[col].apply(lambda x: ' | '.join(x))
			pass

		if f_type in dmf_type_objects :
			# df_light[col] = df_light[col].astype('str')
			pass

		else : 
			df_light[col] = df_light[col].astype('str')

		# log.debug("... dmf_types_list : %s", dmf_types_list)

		# df_light[col] = df_light[col].astype(float)


	print("-/- "*40)

	print()
	log.debug("... df_light end ...")
	print(df_light.head(3))


	return df_light



def dsi_remap (dsi_data, df_mapper_dsi_to_dmf, df_mapper_col_headers ) : 
	""" 
	- get usefull map from df_mapper_dsi_to_dmf & df_mapper_col_headers
	- load a dsi f_data as df
	- drop useless columns
	- remap columns from dso's dsi_to_dmf list
	returns light df
	"""

	print()
	print("-|- "*40)
	log.debug("... dsi_remap ...")

	### add df_mapper_dsi_to_dmf from df_mapper_col_headers
	df_oid 		 = dsi_data["oid_dsi"]
	log.debug("... df_oid : %s", df_oid)
	df_map_light = df_mapper_dsi_to_dmf.loc[df_oid]
	df_map 		 = pd.merge(df_map_light, df_mapper_col_headers, on=['oid_dmf']).reset_index()
	df_map_ 	 = df_map.set_index('dsi_header')
	print() 
	log.debug("... df_map_ ...")
	print(df_map_)

	### list cols to keep : present in dsi and mapped
	# df_cols_to_keep  = list(df_map['dsi_header']) ### if no set_index before 
	df_cols_to_keep  = list(df_map_.index)			### if set_index before

	### generate df from dsi_data
	df_ 	= pd.DataFrame(dsi_data["data_raw"]["f_data"])
	
	### drop useless columns in df_
	df_cols 				= list(df_.columns)
	df_cols_to_drop = [ h for h in df_cols if h not in df_cols_to_keep ]
	df_light 				= df_.drop( df_cols_to_drop, axis=1 )
	# print()
	log.debug("... df_light (after columns drop) ...")
	# print(df_light.head(3))


	### convert Nan to None
	df_light = df_light.replace({np.nan:None})
	print()
	log.debug("... df_light : Nan values converted to None ...")
	log.debug("... df_light.dtypes : \n%s", pformat(df_light.dtypes))
	print(df_light.head(3))

	### convert columns types
	df_light = convert_col_types( df_light, df_map_ )
	log.debug("... df_light (after conversions) ...")
	print()
	print(df_light.dtypes)
	print(df_light.head(3))

	### convert NaT to None
	df_light = df_light.replace({pd.NaT:None})
	print()

	# ### rename columns dataframe
	remapper_dict			= dict(df_map_['f_title'])
	df_light.columns 	= df_light.columns.to_series().map(remapper_dict)
	# print()
	log.debug("... df_light (after renaming) ...")
	# print(df_light.head(3))

	return df_light



def concat_dsi_list(headers_dso, df_mapper_dsi_to_dmf, dsi_raw_data_list) : 
	"""
	concat and reindex several sets of data 
	"""

	print()
	print("-+- "*40)
	log.debug("... concat_dsi_list ...")

	# ### prj_dsi_mapping to df + index
	# df_mapper_dsi_to_dmf = pd.DataFrame(prj_dsi_mapping)
	# df_mapper_dsi_to_dmf = df_mapper_dsi_to_dmf.set_index(["oid_dsi","oid_dmf"])
	# print()
	# log.debug("... df_mapper_dsi_to_dmf ...")
	# print(df_mapper_dsi_to_dmf)

	### headers_dso to df + index
	df_mapper_col_headers = pd.DataFrame(headers_dso)
	df_mapper_col_headers = df_mapper_col_headers.set_index("oid_dmf")
	print()
	log.debug("... df_mapper_col_headers ...")
	print(df_mapper_col_headers)

	### store remapped each dsi's f_data in a df_list
	df_list = []
	for dsi_data in dsi_raw_data_list : 

		print()
		log.debug("... dsi_data['oid_dsi'] : %s", dsi_data['oid_dsi'])
		df_dsi = dsi_remap( dsi_data, df_mapper_dsi_to_dmf, df_mapper_col_headers )
		print(df_dsi.head(3))
		df_list.append(df_dsi)

	log.debug("... df_list is composed ...")

	### concat df_list
	df_data_concat = pd.concat(df_list, ignore_index=True, sort=False)	
	log.debug("... df_data_concat is composed ...")


	### convert Nan to None
	# df_data_concat = df_data_concat.replace({np.nan:None})
	# print()
	# log.debug("... df_data_concat : Nan values converted to None ...")
	# log.debug("... df_data_concat.dtypes : \n%s", pformat(df_data_concat.dtypes))
	# print(df_data_concat.head(3))


	return df_data_concat



