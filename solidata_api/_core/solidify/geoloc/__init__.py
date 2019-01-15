# -*- encoding: utf-8 -*-

"""
geoloc.__init__.py  
"""


from log_config import log, pformat

log.debug("... loading geoloc.py ...")

from .. import db_dict_by_type

### NOTEBOOK
# cf Jupyter notebook : '@/_snippets/tests_geopy_02.ipynb' 

### GEOCODE DATAFRAME WITH GEOPY
# cf : https://geopy.readthedocs.io/en/stable/#installation
# cf : https://wiki.openstreetmap.org/wiki/Nominatim
# cf : http://blog.adrienvh.fr/2015/01/18/geocoder-en-masse-plusieurs-milliers-dadresses-avec-python-et-nominatim/

from time import sleep
from multiprocessing import Process

import pprint
pp = pprint.PrettyPrinter(indent=2)

import pandas as pd
# cf : https://github.com/jmcarpenter2/swifter
# cf : https://medium.com/@jmcarpenter2/swiftapply-automatically-efficient-pandas-apply-operations-50e1058909f9
import swifter

from geopy.geocoders import Nominatim, BANFrance
from geopy.extra.rate_limiter import RateLimiter

from functools import partial
# from tqdm import tqdm


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
### GENERIC VARIABLES
### - - - - - - - - - - - - - - ### 

dft_delay        = 1
dft_timeout      = 20
full_address_col = "_solidata_full_address_"
location_col     = "_solidata_location_"


### - - - - - - - - - - - - - - ### 
### GEOCODERS
### - - - - - - - - - - - - - - ### 

geocoder_nom = Nominatim(user_agent="solidata_app")
geocoder_ban = BANFrance(user_agent="solidata_app")
### rate limiter
geocode_nom = RateLimiter(geocoder_nom.geocode, min_delay_seconds=dft_delay)
geocode_ban = RateLimiter(geocoder_ban.geocode, min_delay_seconds=dft_delay)


### - - - - - - - - - - - - - - ### 
### GENERIC GEOLOC FUNCTIONS
### - - - - - - - - - - - - - - ### 

### location formater
def LocToDict(location) : 
	if location != None : 
		return {
			"raw"       : location.raw,
			"address"   : location.address,
			"point"     : location.point,
			"latitude"  : location.latitude,
			"longitude" : location.longitude,
		}
	else : 
		return {
			"raw"        : None,
			"address"    : None,
			"point"      : None,
			"latitude"   : None,
			"longitude"  : None,
		}

### concat function
def concat_cols(row, columns_to_concat):
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
		delay		= dft_delay 
	) : 

	"""
	used like that on a dataframe 'df' :

	df[location_col] = df[full_address_col].swifter.apply( 
		geoloc_df_col, 
		complement=adress_complement, 
		time_out=dft_timeout, 
		delay=dft_delay, 
	)

	"""

	log.debug("\n- row_val : ", row_val)
	
	if pd.notnull(row_val) : 
		
		adress = ", ".join( [ row_val, complement ] )
		log.debug("- adress : ", adress)

		try :
			location = geocoder_nom.geocode( query=adress, timeout=time_out, extratags=True)
		except : 
			location = geocoder_ban.geocode( query=adress, timeout=time_out)

		log.debug("- location : ", location)

		sleep(delay)

		if location : 
			return LocToDict(location)
		
		else : 
			return None
	
	else : 
		return None




### - - - - - - - - - - - - - - - - - - - - ### 
### GEOLOC WRAPPER / RUNNER FOR SOLIDATA
### - - - - - - - - - - - - - - - - - - - - ### 

class geoloc_prj : 
	
	def __init__ ( 	self, 
					src_docs 		= None, 
					rec_params		= {},
					is_complex_rec	= False,
				) : 
		""" 
		initiate the class to add geolocalization to data
		""" 

		print()
		print("- ~ "*40)

		log.debug("... initiating geoloc_prj ...")
		self.src_docs 		= src_docs
		self.rec_params 	= rec_params
		self.is_complex_rec = is_complex_rec

		log.debug("... rec_params : \n%s", pformat(rec_params) )


	def remap_prj (self) : 
	
		log.debug("... running remap_prj ...")

		### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
		### OPERATIONS ON PRJ's MAPPING
		### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
	
		### remap open_level of each new_dmf in PRJ's mapping with default value

		### add mapping for each DSI's new column in PRJ's mapping 


		### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
		### OPERATIONS ON DMT
		### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

		### add new_dmfs to DMT if does not exist yet

		### save updated DMT


	def run_geoloc ( self, *args, **kwargs ) : 

		log.debug("... running geoloc_prj ...")

		### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
		### OPERATIONS ON DSI
		### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
		### load every DSI's f_data as a dataframe & add new columns (new_dmfs) if does not exist yet
		for dsi_doc in self.src_docs["dsi_list"] : 
			
			print()
			log.debug("... solidifying dsi_doc['infos']['title'] : %s", dsi_doc['infos']['title'])

			### proceed geoloc for f_data
			dsi_f_data 	= dsi_doc["data_raw"]["f_data"]
			df_f_data 	= pd.DataFrame(dsi_f_data)
			print (df_f_data.head(3))

			### get columns to geoloc from mapper / rec_params

			### save/update new f_data for each DSI



		### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
		### COMPLEX OPERATIONS : UPDATE DMT / REMAP PRJ's DMT-OPEN_LEVEL / REMAP PRJ's DSI-DMT 
		### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
		if self.is_complex_rec == True :
			
			log.debug("... running geoloc_prj ...")
			
			self.remap_prj()






	

