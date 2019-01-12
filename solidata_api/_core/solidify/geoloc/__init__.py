# -*- encoding: utf-8 -*-

"""
geoloc.__init__.py  
"""


from log_config import log, pformat

log.debug("... loading geoloc.py ...")


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