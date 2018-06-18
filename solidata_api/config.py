"""
config.py  
- settings for the flask application object
"""

class BaseConfig(object):  

	DEBUG = True

	# used for encryption and session management

	""" RESTPLUS CONFIG """
	# SWAGGER_UI_DOC_EXPANSION 		= 'list'
	SWAGGER_UI_JSONEDITOR 			= True
	SWAGGER_UI_OPERATION_ID 		= True
	SWAGGER_UI_REQUEST_DURATION = True

	""" APP SECRET KEY """
	SECRET_KEY			= "app_very_secret_key"

	""" SHARED JWT SECRET KEY : this key must be shared with openscraper and solidata """
	JWT_SECRET_KEY		= "a_key_shared_with_front_and_openscraper_and_solidata"

	""" HOST """
	DOMAIN_ROOT				= "localhost" 
	DOMAIN_PORT				= "4000"
	SERVER_NAME				= "localhost:4000"  ### if True need to set SESSION_COOKIE_DOMAIN + cf : https://stackoverflow.com/questions/47666210/cookies-not-saved-in-the-browser 
	DOMAIN_NAME				= "http://localhost:4000"
	SERVER_NAME_TEST	= "True" 

	""" MONGODB """
	MONGO_DBNAME								= 'solidata'
	MONGO_URI										= 'mongodb://localhost:27017/solidata'
	# collections
	MONGO_COLL_USERS						  = "users"
	MONGO_COLL_LICENCES					  = "licences"
	MONGO_COLL_PROJECTS					  = "projects"
	MONGO_COLL_DATAMODELS			  	 = "datamodels"
	MONGO_COLL_DATAMODELS_FIELDS	= "datamodels_fields"
	MONGO_COLL_CONNECTORS				  = "connectors"
	MONGO_COLL_DATASETS_INPUTS	  = "datasets_inputs"
	MONGO_COLL_DATASETS_OUTPUTS	  = "datasets_outputs"
	MONGO_COLL_RECIPES					  = "recipes"
	MONGO_COLL_CORR_DICTS				  = "corr_dicts"
