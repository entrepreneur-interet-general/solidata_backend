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

		# access mongodb collections
		from solidata_api._core.queries_db import db, \
			mongo_users,mongo_licences,mongo_projects,mongo_datamodels, \
			mongo_datamodels_fields,mongo_connectors, \
			mongo_datasets_inputs,mongo_datasets_outputs, \
			mongo_recipes,mongo_corr_dicts

		# import token required
		from solidata_api._auth import authorizations #, token_required


	## DEBUGGING
	print()
	find_one_user = mongo_users.find({'infos.name': "Julien"})
	# find_one_user = db["mongo_users"].find({'infos.name': "Julien"})
	log.debug("DEBUG : find_one_user : \n%s", pformat(list(find_one_user)))


	### registering all blueprints
	print()
	log.debug("... registering blueprints ...")
	from solidata_api.api.api_users 		import blueprint as api_users
	app.register_blueprint( api_users, url_prefix="/api/users" )

	from solidata_api.api.api_auth 	import blueprint as api_auth
	app.register_blueprint( api_auth, url_prefix='/api/auth')



	### DEBUG
	# @app.before_request
	# def debug_stuff():
	# 	# pass
	# 	log.debug ("\n%s", pformat(current_app.__dict__))


	return app