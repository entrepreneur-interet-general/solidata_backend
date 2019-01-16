# -*- encoding: utf-8 -*-

"""
geoloc.__init__.py  
"""


from log_config import log, pformat

log.debug("... loading geoloc.py ...")

from  	datetime import datetime, timedelta
from	bson.objectid 	import ObjectId

from 	time import sleep
from 	multiprocessing import Process, Pool, cpu_count

import 	pprint
pp = pprint.PrettyPrinter(indent=2)

### import db collections
from .. import db_dict_by_type

### NOTEBOOK
# cf Jupyter notebook : '@/_snippets/tests_geopy_02.ipynb' 

### GEOCODE DATAFRAME WITH GEOPY
# cf : https://geopy.readthedocs.io/en/stable/#installation
# cf : https://wiki.openstreetmap.org/wiki/Nominatim
# cf : http://blog.adrienvh.fr/2015/01/18/geocoder-en-masse-plusieurs-milliers-dadresses-avec-python-et-nominatim/

# cf : https://github.com/jmcarpenter2/swifter
# cf : https://medium.com/@jmcarpenter2/swiftapply-automatically-efficient-pandas-apply-operations-50e1058909f9
import 	swifter

import 	geopy.geocoders
from 	geopy.geocoders import Nominatim, BANFrance
from 	geopy.extra.rate_limiter import RateLimiter

geopy.geocoders.options.default_user_agent = "solidata_app"

from 	functools import partial
# from tqdm import tqdm

### import pandas functions
from 	solidata_api._core.pandas_ops import pd, np, prj_dsi_mapping_as_df


'''
### example multhithreading ... 
### cf : https://stackoverflow.com/questions/31967571/run-two-python-functions-simultaneously-with-sleep
def foo(x):
	while True:
		print ("It deletes dat file and creates new one")
		time.sleep(x)

def bar():
	while True:
		print ("Wtires to dat file")

process1 = Process(target=foo, args=(0.05,))
process2 = Process(target=bar)
process1.start()
process2.start()
'''

### - - - - - - - - - - - - - - ### 
### GEOCODERS
### - - - - - - - - - - - - - - ### 

geocoder_nom = Nominatim(user_agent="solidata_app_to_Nominatim")
geocoder_ban = BANFrance(user_agent="solidata_app_to_BAN")
# geocoder_nom = Nominatim()
# geocoder_ban = BANFrance()


### - - - - - - - - - - - - - - ### 
### GENERIC VARIABLES
### - - - - - - - - - - - - - - ### 

dft_delay        = 1
dft_timeout      = 10
full_address_col = "temp_solidata_full_address_"
location_col     = "temp_solidata_location_"



### - - - - - - - - - - - - - - ### 
### GENERIC GEOLOC FUNCTIONS
### - - - - - - - - - - - - - - ### 

def LocToDict(location_raw) : 
	""" 
	location formater
	"""
	log.debug("... LocToDict / location_raw : \n%s ", pformat(location_raw) )
	if location_raw != None : 
		return {
			"raw"       : location_raw.raw,
			"address"   : location_raw.address,
			"point"     : location_raw.point,
			"latitude"  : location_raw.latitude,
			"longitude" : location_raw.longitude,
		}
	else : 
		return {
			"raw"        : None,
			"address"    : None,
			"point"      : None,
			"latitude"   : None,
			"longitude"  : None,
		}

def extract_loc(row, field_name="longitude") :
	""" 
	extract field value from a cell's dict
	"""
	# print(row)
	# print (type(row))
	return row[field_name]
	
def concat_cols(row, columns_to_concat):
	""" 
	concat function
	"""
	if len(columns_to_concat) > 1 :
		return ", ".join( row[col] for col in columns_to_concat )
	else : 
		return row[columns_to_concat[0]]


### TO DO  : prevent error 429 (too many requests) by using RateLimiter

### main geolocalizing function for dataframe
### NOTE : try to slice dataframe by 100 rows 
###        + update doc after each slice so to show progress to user
def geoloc_df_col( 
		row_val, 
		complement	= "", 
		time_out	= dft_timeout, 
		delay		= dft_delay, 
		apply_sleep = False
	) : 

	"""
	used like that on a dataframe 'df' :

	df[location_col] = df[full_address_col].swifter.apply( 
		geoloc_df_col, 
		complement=adress_complement, 
		time_out=dft_timeout, 
		delay=dft_delay, 
	)

	* note : used with swifter for performance purposes...

	"""
	print()
	print ( "- geoloc_df_col " + "*.  "*40 ) 
	log.debug("\n- row_val : %s", row_val)
	
	### rate limiter
	geocode_nom = RateLimiter(geocoder_nom.geocode, min_delay_seconds=delay)
	geocode_ban = RateLimiter(geocoder_ban.geocode, min_delay_seconds=delay)

	if pd.notnull(row_val) : 
		
		### add address complement to full_address_col value (in case it helps)
		adress = ", ".join( [ row_val, complement ] )
		log.debug("- adress : %s", adress)

		try :
			### test with nominatim first
			location_raw = geocoder_nom.geocode( query=adress, timeout=time_out, extratags=True)
		except : 
			### test with BAN first
			location_raw = geocoder_ban.geocode( query=adress, timeout=time_out)

		log.debug("- location_raw : \n%s", pformat(location_raw))

		### make function sleep 
		if apply_sleep : 
			sleep(delay)

		if location_raw : 
			return LocToDict(location_raw)
		
		else : 
			return None
	
	else : 
		return None


### - - - - - - - - - - - - - - - - - - - ### 
### MAIN GEOLOC FUNCTIONS FOR DSIs
### - - - - - - - - - - - - - - - - - - - ### 

def callback_geoloc (result_geoloc) : 
	log.debug('callback_geoloc - result_geoloc : \n%s', result_geoloc )

def errorhandler(exc):
	log.warning('Exception : \n%s', exc)


def geoloc_dsi ( 	dsi_doc, 
					params, 
					self_df_mapper_dsi_to_dmf, 
					self_dmf_list_to_geocode,
					use_swifter 	= False,
					dft_test_trim 	= 4,
				) : 

	print()
	print ( "- geoloc_dsi " + "-   "*40 ) 
	log.debug("... solidifying dsi_doc['infos']['title'] : %s", dsi_doc['infos']['title'])
	
	log.debug("... params : \n%s", pformat(params) )

	### retrieve dsi_oid and check test
	dsi_oid 		= dsi_doc["_id"]
	test_geoloc 	= params["test_geoloc"]
	new_dmfs_list	= params["new_dmfs_list"]
	dsi_is_running 	= dsi_doc["log"].get( "is_running", False )

	### get mapped headers for this dsi
	dsi_mapper = self_df_mapper_dsi_to_dmf.loc[dsi_oid]
	print()
	log.debug("... dsi_mapper ... ")
	print(dsi_mapper)

	### select list of meaningfull columns to be concatenated as base for geoloc input
	df_headers_selection = dsi_mapper.loc[dsi_mapper.index.isin( self_dmf_list_to_geocode )]
	print()
	log.debug("... df_headers_selection ... ")
	print(df_headers_selection)
	cols_to_concat = list(df_headers_selection["dsi_header"])
	log.debug("... cols_to_concat : \n%s ", pformat(cols_to_concat))

	### load every DSI's f_data as a dataframe & add new columns (new_dmfs) if does not exist yet
	dsi_f_data 		= dsi_doc["data_raw"]["f_data"]
	df_f_data_src 	= pd.DataFrame(dsi_f_data)
	# print()
	# log.debug("... df_f_data.head(3) ... ")
	# print (df_f_data.head(3))
	
	### just keep cols_to_concat we want to work on to save memory
	df_f_data = df_f_data_src[ cols_to_concat ]

	### before concatenating columns clean cols_to_concat from NaN values
	df_f_data = df_f_data.fillna(value="")

	''' apply concat function to each row (axis=1) --> alternative LESS pythonic
			### change type of every target column --> string 
			df_f_data[cols_to_concat] 	= df_f_data[cols_to_concat].astype(str)
			log.debug("... df_f_data.head(3) - after changing types ... ")
			### apply concat function to each row (axis=1)
			df_f_data[full_address_col] = df_f_data.apply(concat_cols, args=[cols_to_concat], axis=1)
			log.debug("... df_f_data.head(3) - after apply 'concat_cols' ... ")
			print (df_f_data.head(3))
	'''

	### apply concat function to each row (axis=1) --> alternative MORE pythonic
	df_f_data[full_address_col] = df_f_data[ cols_to_concat ].apply( lambda x : ', '.join(x.astype(str)), axis=1 )

	log.debug("... df_f_data.shape - before test check : %s", df_f_data.shape )

	### slice only first n rows if test mode is activated : 
	if test_geoloc : 
		df_f_data = df_f_data.iloc[ 0 : dft_test_trim ]

	log.debug("... df_f_data.shape - after test check : %s", df_f_data.shape )
	print()
	log.debug("... df_f_data.head(10) - after apply 'concat_cols' ... ")
	print (df_f_data.head(10))

	### proceed geoloc for f_data
	log.debug("type( df_f_data[ full_address_col ] ) : %s", type(df_f_data[ full_address_col ])  )
	

	### flag dsi as already running
	src_ = db_dict_by_type['dsi'].update_one( {"_id" : dsi_oid }, { "$set" : { "log.is_running" : True } } )

	if dsi_is_running == False : 

		if use_swifter : 
			### with swifter
			df_f_data[ location_col ] = df_f_data[ full_address_col ].swifter.apply( 
				geoloc_df_col, 
				complement	= params["address_complement"], 
				time_out	= params["timeout"], 
				delay		= params["delay"],
				apply_sleep = False
			)
		else :
			### without swifter
			df_f_data[ location_col ] = df_f_data[ full_address_col ].apply( 
				geoloc_df_col, 
				complement	= params["address_complement"], 
				time_out	= params["timeout"], 
				delay		= params["delay"],
				apply_sleep = False
			)

		### create and populate new columns in df_f_data_src from new_dmfs_list
		for new_col in new_dmfs_list : 
			new_col_title 					= new_col["infos"]["title"]
			df_f_data_src[new_col_title] 	= df_f_data[location_col].apply(extract_loc, field_name=new_col_title)


	print()
	log.debug("... df_f_data_src.head(10) - after ageocoding ... ")
	print (df_f_data_src.head(10))

	### save updated DSI's F_DATA
	updated_f_data = df_f_data_src.to_dict('records')

	### unflag is_running
	dsi_ = db_dict_by_type['dsi'].update_one( {"_id" : dsi_oid }, {"$set" :  { "log.is_running" : False} } )

	# if test_geoloc == False and dsi_is_running == False : 
	# 	dsi_ = db_dict_by_type['dsi'].update_one( {"_id" : dsi_oid }, {"$set" :  { "data_raw.f_data" : updated_f_data} } )


	### callback for multiprocessing
	log.debug("geoloc_dsi finished ... building response for callback")
	return_response = { 
		"oid_dsi" 			: dsi_oid, 
		"f_data_geoloc"		: df_f_data,
		"is_geolocalized" 	: True 
	}
	return return_response



### - - - - - - - - - - - - - - - - - - - - ### 
### GEOLOC WRAPPER / RUNNER FOR SOLIDATA
### - - - - - - - - - - - - - - - - - - - - ### 

class geoloc_prj : 
	
	def __init__ ( 	self, 
					user_oid,
					src_docs 	= None, 
					rec_params	= {},

					use_multiprocessing	= True,
					pool_or_process		= "process",
					async_or_starmap	= "async",
					cpu_number			= 2
				) : 
		""" 
		initiate the class to add geolocalization to data
		""" 

		print()
		print("- ~ "*40)
		print ( "- remap_prj " + "-  ~ "*40 ) 

		log.debug("... initiating geoloc_prj ...")

		### for multiprocessing / Pool 
		self.use_multiprocessing 	= use_multiprocessing
		self.pool_or_process 		= pool_or_process
		self.async_or_starmap 		= async_or_starmap
		self.cpu_number				= cpu_number

		### payload
		self.user_oid		= user_oid
		self.rec_params		= rec_params
		self.run_time		= datetime.utcnow()
		self.src_doc 		= src_docs["src_doc"]
		self.src_doc_type 	= src_docs["src_doc"]["specs"]["doc_type"]

		# log.debug("... rec_params : \n%s", pformat(rec_params) )

		self.dmf_list_to_geocode 	= [ ObjectId(dmf_id) for dmf_id in rec_params["dmf_list_to_geocode"]]
		log.debug("... self.dmf_list_to_geocode : \n%s", pformat(self.dmf_list_to_geocode) )

		self.new_dmfs_list 			= rec_params["new_dmfs_list"]
		log.debug("... self.new_dmfs_list[0] : \n%s\n...", pformat(self.new_dmfs_list[0]) )

		self.new_dmfs_list_ligth 	= [ dmf_ref["_id"] for dmf_ref in self.new_dmfs_list  ]
		log.debug("... self.new_dmfs_list_ligth : \n%s", pformat(self.new_dmfs_list_ligth) )

		self.new_dmfs_ols 			= rec_params["new_dmf_open_level_show"]
		self.address_complement 	= rec_params["address_complement"]

		self.test_geoloc 			= rec_params.get("test_geoloc", False)
		log.debug("... self.test_geoloc : %s", self.test_geoloc )

		if rec_params["delay"] and rec_params["delay"] != 0 : 
			self.delay 				= rec_params["delay"]
		else : 
			self.delay = self.rec_params["delay"] = dft_delay
	
		if rec_params["timeout"] and rec_params["timeout"] != 0 : 
			self.timeout 				= rec_params["timeout"]
		else : 
			self.timeout = self.rec_params["timeout"] = dft_timeout

		### geoloc a PRJ
		if self.src_doc_type in ["prj"] : 	
			self.is_complex_rec 	= True
			self.dmt_doc 			= src_docs["dmt_doc"]
			self.dmf_list 			= src_docs["dmf_list"]
			self.dsi_list 			= src_docs["dsi_list"]
			self.prj_dmf_ols_mapping 	= src_docs["src_doc"]["mapping"]["dmf_to_open_level"]
			self.prj_dsi_mapping 		= src_docs["src_doc"]["mapping"]["dsi_to_dmf"]
		
		### only geoloc a DSI
		else : 
			self.is_complex_rec 	= False
			self.dsi_list 			= src_docs["src_doc"]

		self.dsi_mapped_list 		= []
		self.df_mapper_dsi_to_dmf 	= None


	def remap_dsi(self) :
		""" 
		to do : for geoloc call on only one DSI
		""" 

		print()
		log.debug("... running remap_dsi ...")

		### TO DO : store a dsi map as dataframe (same format as self.df_mapper_dsi_to_dmf )


	def remap_prj (self) : 
		""" 
		update mapping of a RPJ and related DMT
		""" 

		print()
		print ( "- remap_prj " + "-   "*40 ) 
		log.debug("... running remap_prj ...")

		### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
		### OPERATIONS ON PRJ's DMT
		### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
		print()
		### add new_dmfs to DMT if does not exist yet
		new_dmfs_refs_dataset = [ 	{ 
								"oid_dmf" 	: dmf_ref, 
								"added_by" 	: self.user_oid,
								"added_at"	: self.run_time,
							} for dmf_ref in self.new_dmfs_list_ligth ]
		log.debug("new_dmfs_refs_dataset :\n%s", pformat(new_dmfs_refs_dataset) )

		dmt_existing_dmf_dataset = [ dmf_ref for dmf_ref in self.dmt_doc["datasets"]["dmf_list"] if dmf_ref["oid_dmf"] not in self.new_dmfs_list_ligth ]
		log.debug("dmt_existing_dmf_dataset :\n%s", pformat(dmt_existing_dmf_dataset) )

		dmt_existing_dmf_oids	= [ dmf_ref["oid_dmf"] for dmf_ref in dmt_existing_dmf_dataset if dmf_ref["oid_dmf"] not in self.new_dmfs_list_ligth ]
		log.debug("dmt_existing_dmf_oids :\n%s", pformat(dmt_existing_dmf_oids) )
	
		dmf_to_add_to_existing 	= [ new_dmf for new_dmf in new_dmfs_refs_dataset if new_dmf["oid_dmf"] not in dmt_existing_dmf_oids ]
		log.debug("dmf_to_add_to_existing :\n%s", pformat(dmf_to_add_to_existing) )
		
		updated_dmf_list = dmt_existing_dmf_dataset + dmf_to_add_to_existing
		log.debug("updated_dmf_list :\n%s", pformat(updated_dmf_list) )

		### save updated DMT
		dmt_ = db_dict_by_type['dmt'].update_one( {"_id" : self.dmt_doc["_id"]}, { "$set" : { "datasets.dmf_list" : updated_dmf_list} } )


		### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
		### OPERATIONS ON PRJ's MAPPING / DMF_TO_OPEN_LEVEL
		### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
		print()
		### remap open_level of each new_dmf in PRJ's mapping with default value
		new_dmfs_refs_map_ols = [ 	{ 
								"oid_dmf" 			: dmf_ref, 
								"open_level_show" 	: self.new_dmfs_ols,
							} for dmf_ref in self.new_dmfs_list_ligth ]
		log.debug("new_dmfs_refs_map_ols :\n%s", pformat(new_dmfs_refs_map_ols) )
		log.debug("self.new_dmfs_list_ligth :\n%s", pformat(self.new_dmfs_list_ligth) )
		
		log.debug("self.prj_dmf_ols_mapping :\n%s", pformat(self.prj_dmf_ols_mapping) )

		if self.prj_dmf_ols_mapping != [] :

			prj_existing_mapping_dmf_ols		= [ dmf_ref for dmf_ref in self.prj_dmf_ols_mapping if dmf_ref["oid_dmf"] not in self.new_dmfs_list_ligth ]
			log.debug("prj_existing_mapping_dmf_ols :\n%s", pformat(prj_existing_mapping_dmf_ols) )

			prj_existing_mapping_dmf_ols_oids	= [ dmf_ref["oid_dmf"] for dmf_ref in prj_existing_mapping_dmf_ols ]
			log.debug("prj_existing_mapping_dmf_ols_oids :\n%s", pformat(prj_existing_mapping_dmf_ols_oids) )

			dmf_ols_to_add_to_existing 		= [ new_dmf for new_dmf in new_dmfs_refs_map_ols if new_dmf["oid_dmf"] not in prj_existing_mapping_dmf_ols_oids ]
			
			updated_dmf_ols_list = prj_existing_mapping_dmf_ols + dmf_ols_to_add_to_existing
			log.debug("updated_dmf_ols_list :\n%s", pformat(updated_dmf_ols_list) )
		
		else : 
			updated_dmf_ols_list = new_dmfs_refs_map_ols

		### save updated PRJ's MAPPING FOR DMF_TO_OPEN_LEVEL
		src_ = db_dict_by_type[self.src_doc_type].update_one( {"_id" : self.src_doc["_id"]}, { "$set" : { "mapping.dmf_to_open_level" : updated_dmf_ols_list} } )


		### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
		### OPERATIONS ON PRJ's MAPPING / DSI_TO_DMF
		### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
		print()
		### get columns to geoloc from mapper / rec_params
		### prj_dsi_mapping to df + index
		self.dsi_mapped_list, df_mapper_dsi_to_dmf = prj_dsi_mapping_as_df(self.prj_dsi_mapping)
		
		log.debug("self.dsi_mapped_list :\n%s", pformat(self.dsi_mapped_list) )

		### set up self.df_mapper_dsi_to_dmf for later purposes
		self.df_mapper_dsi_to_dmf = df_mapper_dsi_to_dmf

		### reset index of df_mapper_dsi_to_dmf_reindexed
		df_mapper_dsi_to_dmf_reindexed = df_mapper_dsi_to_dmf.copy() #.reset_index() 
		log.debug("df_mapper_dsi_to_dmf_reindexed ...") 
		print(df_mapper_dsi_to_dmf_reindexed)

		### add mapping for each DSI's new column in PRJ's mapping 
		dsi_oids = [ dsi_doc["_id"] for dsi_doc in self.dsi_list ]
		for dsi_oid in dsi_oids :  

			### create list of new entries
			newmap_dsi_to_dmf = [ {
					"dsi_header" 	: new_dmf_to_map["infos"]["title"], 
					"oid_dsi" 		: dsi_oid, 
					"oid_dmf" 		: new_dmf_to_map["_id"], 
				} for new_dmf_to_map in self.new_dmfs_list ]
			log.debug("newmap_dsi_to_dmf : \n%s ", pformat(newmap_dsi_to_dmf) ) 
			df_newmap_dsi_to_dmf = pd.DataFrame(newmap_dsi_to_dmf).set_index(["oid_dsi","oid_dmf"])

			### append list of values to df_mapper_dsi_to_dmf
			df_mapper_dsi_to_dmf_reindexed = df_mapper_dsi_to_dmf_reindexed.append(df_newmap_dsi_to_dmf)
	
		log.debug("df_mapper_dsi_to_dmf_reindexed -> after adding dsi entries ") 
		print(df_mapper_dsi_to_dmf_reindexed)

		df_mapper_dsi_to_dmf_reindexed = df_mapper_dsi_to_dmf[~df_mapper_dsi_to_dmf.index.duplicated(keep="first")].sort_index()
		log.debug("df_mapper_dsi_to_dmf_reindexed -> after deleting duplicate indices from multiindex") 
		print(df_mapper_dsi_to_dmf_reindexed)

		### reindex by oid_dsi -> oid_dmf (delete possible twin value) & reset index
		df_mapper_dsi_to_dmf_reindexed = df_mapper_dsi_to_dmf_reindexed.reset_index()
		log.debug("df_mapper_dsi_to_dmf_reindexed -> after adding dsi entries reset_index ...") 
		print(df_mapper_dsi_to_dmf_reindexed)

		### get list of values from dataframe
		updated_dsi_to_dmf_list = df_mapper_dsi_to_dmf_reindexed.to_dict('records')
		log.debug("updated_dsi_to_dmf_list : \n%s ", pformat(updated_dsi_to_dmf_list) ) 

		### save updated PRJ's MAPPING FOR DSI_TO_DMF
		src_ = db_dict_by_type[self.src_doc_type].update_one( {"_id" : self.src_doc["_id"]}, {"$set" :  { "mapping.dsi_to_dmf" : updated_dsi_to_dmf_list }} )
			
		

	def run_geoloc ( self, *args, **kwargs ) : 

		print()
		print ( "- run_geoloc " + "-   "*40 ) 
		log.debug("... running geoloc_prj ...")

		### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
		### COMPLEX OPERATIONS : UPDATE DMT / REMAP PRJ's DMT-OPEN_LEVEL / REMAP PRJ's DSI-DMT 
		### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
		
		### if doc_type in ["prj"]
		if self.is_complex_rec == True :
			log.debug("... run_geoloc / complex recipe ...")
			self.remap_prj()
		
		### if doc_type == "dsi"
		else : 
			log.debug("... run_geoloc / simple recipe ...")
			self.remap_dsi()


		### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
		### OPERATIONS ON DSI - AS MULTIPROCESSING PROCESSES (if needed)
		### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

		src_ = db_dict_by_type[self.src_doc_type].update_one( {"_id" : self.src_doc["_id"]}, { "$set" : { "log.is_running" : True} } )

		if self.use_multiprocessing : 
			processes 	= []
			if self.pool_or_process == "pool" :
				pool 	= Pool(self.cpu_number)

		### loop dsi list
		for dsi_doc in self.dsi_list : 

			## CHOICE A : use a Process (no return / call back)
			if self.use_multiprocessing and self.pool_or_process == "process" : 
				log.debug("... run_geoloc : multiprocessing / PROCESSES (Process) ...")
				process = Process( 
					target 	= geoloc_dsi, 
					args 	= ( dsi_doc, self.rec_params, self.df_mapper_dsi_to_dmf, self.dmf_list_to_geocode, )  
				)
				processes.append(process)

			### CHOICE B : use a Pool (call backs)
			elif self.use_multiprocessing and self.pool_or_process == "pool" : 

				if self.async_or_starmap == "starmap" : 
					log.debug("... run_geoloc : multiprocessing / POOL (pool.starmap) ...")
					result = pool.starmap( 	
									geoloc_dsi, 
									[ ( dsi_doc, self.rec_params, self.df_mapper_dsi_to_dmf, self.dmf_list_to_geocode ) ], 
								)

				elif self.async_or_starmap == "async" : 
					log.debug("... run_geoloc : multiprocessing / POOL (pool.async) ...")
					### Use apply_async if you want callback to be called for each time.
					result = pool.apply_async( 	
									geoloc_dsi, 
									( dsi_doc, self.rec_params, self.df_mapper_dsi_to_dmf, self.dmf_list_to_geocode ) ,
									callback		= callback_geoloc,
									error_callback	= errorhandler
								)

			### CHOICE C : chained as usual synchronous process
			else : 
				log.debug("... run_geoloc : multiprocessing / NONE ...")
				result = geoloc_dsi( dsi_doc, self.rec_params, self.df_mapper_dsi_to_dmf, self.dmf_list_to_geocode )


		## CHOICE A : run processes
		if self.use_multiprocessing and self.pool_or_process == "process" : 
			
			log.debug("... run_geoloc : multiprocessing / PROCESSES ...")
			result = [ p.start() for p in processes ]
			log.debug("process - result : \n%s ", pformat(result) )


		## CHOICE B : run Pool
		elif self.use_multiprocessing and self.pool_or_process == "pool" : 

			log.debug("... run_geoloc : multiprocessing / POOL ...")
			pool.close()
			pool.join() # wait for all subprocesses to finish

			log.debug("... run_geoloc : pool closed...")
			log.debug("process - result : \n%s ", pformat(result) )




		print ( "-   "*40 ) 
		log.debug("... run_geoloc : processes finished...")
		print ( "-   "*40 ) 



	

