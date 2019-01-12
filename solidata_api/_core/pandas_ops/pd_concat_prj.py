# -*- encoding: utf-8 -*-

"""
pd_concat_prj.py  
"""


from log_config import log, pformat

log.debug("... loading pd_concat_prj.py ...")

from . import pd, np


def dsi_remap (dsi_data, df_mapper_dsi_to_dmf, df_mapper_col_headers ) : 
	""" 
	- get usefull map from df_mapper_dsi_to_dmf & df_mapper_col_headers
	- load a dsi f_data as df
	- drop useless columns
	- remap columns from dso's dsi_to_dmf list
	returns light df
	"""

	### add df_mapper_dsi_to_dmf from df_mapper_col_headers
	df_oid 		 = dsi_data["oid_dsi"]
	log.debug("... df_oid : %s", df_oid)
	df_map_light = df_mapper_dsi_to_dmf.loc[df_oid]
	df_map 		 = pd.merge(df_map_light, df_mapper_col_headers, on=['oid_dmf']).reset_index()
	df_map_ 	 = df_map.set_index('dsi_header')

	### list cols to keep : present in dsi and mapped
	# df_cols_to_keep  = list(df_map['dsi_header']) ### if no set_index before 
	df_cols_to_keep  = list(df_map_.index)			### if set_index before

	### generate df from dsi_data
	df_ 	= pd.DataFrame(dsi_data["data_raw"]["f_data"])
	### drop useless columns in df_
	df_cols 			= list(df_.columns)
	df_cols_to_drop 	= [ h for h in df_cols if h not in df_cols_to_keep ]
	df_light 			= df_.drop( df_cols_to_drop, axis=1 )
	# print()
	log.debug("... df_light (before renaming) ...")
	# print(df_light)

	# ### rename columns dataframe
	remapper_dict		= dict(df_map_['name'])
	df_light.columns 	= df_light.columns.to_series().map(remapper_dict)
	# print()
	log.debug("... df_light (after renaming) ...")
	# print(df_light)

	return df_light




def concat_dsi_list(headers_dso, df_mapper_dsi_to_dmf, dsi_raw_data_list) : 
	"""
	concat and reindex several sets of data 
	"""

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
		log.debug("... dsi_data['oid_dsi'] : %s", dsi_data['oid_dsi'])
		df_dsi = dsi_remap( dsi_data, df_mapper_dsi_to_dmf, df_mapper_col_headers )
		df_list.append(df_dsi)

	### concat df_list
	df_data_concat = pd.concat(df_list, ignore_index=True, sort=False)	
	### convert Nan to None
	df_data_concat = df_data_concat.replace({np.nan:None})

	### get result as a list
	new_f_data = df_data_concat.to_dict('records')

	return new_f_data



