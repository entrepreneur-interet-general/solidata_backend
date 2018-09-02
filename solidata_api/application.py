# -*- encoding: utf-8 -*-

"""
application.py  
- creates a Flask app instance and registers the database object
"""

from log_config import log, pprint, pformat
log.debug ("... starting app ...")

from flask import Flask, g, current_app

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### FLASK-EXTENDED-JWT IMPORTS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
# cf : https://github.com/vimalloc/flask-jwt-extended/issues/14
from flask_jwt_extended import JWTManager

# declare JWT empty connector
jwt_manager = JWTManager()
log.debug("... jwt_manager() ...")
# log.debug(" jwt_manager() : \n%s ", pformat(jwt_manager))


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### LOGIN MANAGER 
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

# from  	flask_login import 	LoginManager, login_user, logout_user, login_required, \
# 				current_user


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### FLASK-ADMIN IMPORTS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
# from	flask_admin 							import Admin, AdminIndexView
# from 	flask_admin.model 				import typefmt
# from 	flask_admin.model.widgets import XEditableWidget


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### FLASK-CORS IMPORTS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
from flask_cors import CORS, cross_origin


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### FLASK-PYMONGO IMPORTS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
from flask_pymongo import PyMongo

# declare mongo empty connector
mongo = PyMongo()


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### FLASK-MAIL IMPORTS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
from flask_mail import Mail
mail = Mail()



### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### CREATE APP
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
# application factory, see: http://flask.pocoo.org/docs/patterns/appfactories/

def create_app( app_name='SOLIDATA_API', run_mode="dev" ):  

	log.debug ("... creating app ...")

	### create Flask app
	app = Flask(app_name)

	### load config 
	if run_mode == "prod" : 	
		app.config.from_object('solidata_api.config_prod.Prod')
	elif run_mode == "dev_email" : 
		app.config.from_object('solidata_api.config_prod.DevEmail')
	else : 
		app.config.from_object('solidata_api.config.BaseConfig')

	print()
	log.debug("... app.config :\n %s", pformat(app.config))
	print()


	### init JWT manager
	log.debug("... init jwt_manager ...")
	jwt_manager.init_app(app)

	### init mongodb client
	log.debug("... init mongo ...")
	mongo.init_app(app)

	### init mail client
	log.debug("... init mail ...")
	mail.init_app(app)


	with app.app_context() :


		# import async functions and decorators
		from solidata_api._core.async_tasks import async

		# access mongodb collections
		from solidata_api._core.queries_db import ( 
				
				db_dict, db_dict_by_type,
				Query_db_list,
				Query_db_doc,
				Query_db_delete,

				mongo_users,
				mongo_tags,
				mongo_projects,
				mongo_datamodels_templates, 
				mongo_datamodels_fields,
				mongo_datasets_inputs,
				mongo_datasets_raws,
				mongo_datasets_outputs, 
				mongo_recipes,
				# mongo_connectors, ### all cd are treated as ds_i

				mongo_jwt_blacklist,
				mongo_licences,
				# mongo_corr_dicts   ### all cd are treated as ds_i
			) 

		# import token required
		from solidata_api._auth import authorizations #, token_required

		# import emailing functions
		from solidata_api._core.emailing import send_email, send_async_email 

		## DEBUGGING
		print()
		find_one_user = mongo_users.find({'infos.name': "Julien"})
		# find_one_user = db["mongo_users"].find({'infos.name': "Julien"})
		log.debug("DEBUG : find_one_user : \n%s", pformat(list(find_one_user)))


		### registering all blueprints
		print()
		log.debug("... registering blueprints ...")
		from solidata_api.api.api_users 		import blueprint as api_users
		app.register_blueprint( api_users, url_prefix="/api/usr" )

		from solidata_api.api.api_auth 	import blueprint as api_auth
		app.register_blueprint( api_auth, url_prefix='/api/auth')

		from solidata_api.api.api_projects 	import blueprint as api_proj
		app.register_blueprint( api_proj, url_prefix='/api/prj')

		from solidata_api.api.api_dataset_inputs 	import blueprint as api_dsi
		app.register_blueprint( api_dsi, url_prefix='/api/dsi')

		from solidata_api.api.api_datamodel_templates 	import blueprint as api_dmt
		app.register_blueprint( api_dmt, url_prefix='/api/dmt')

		from solidata_api.api.api_datamodel_fields 	import blueprint as api_dmf
		app.register_blueprint( api_dmf, url_prefix='/api/dmf')

		from solidata_api.api.api_tags 	import blueprint as api_tag
		app.register_blueprint( api_tag, url_prefix='/api/tag')

		from solidata_api.api.api_recipes 	import blueprint as api_rec
		app.register_blueprint( api_rec, url_prefix='/api/rec')


		### TO DO - write missing endpoints

		# from solidata_api.api.api_datasets_out 	import blueprint as api_dso
		# app.register_blueprint( api_dso, url_prefix='/api/dataset_outputs')




		### init CORS 
		from solidata_api._core.cors import CORS

		### DEBUG
		# @app.before_request
		# def debug_stuff():
		# 	# pass
		# 	log.debug ("\n%s", pformat(current_app.__dict__))


	return app