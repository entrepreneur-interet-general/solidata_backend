# -*- encoding: utf-8 -*-

"""
application.py  
- creates a Flask app instance and registers the database object
"""

from log_config import log, pprint, pformat

from flask import Flask, g, current_app


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### LOGIN MANAGER 
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

from  	flask_login import 	LoginManager, login_user, logout_user, login_required, \
				current_user


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### FLASK-ADMIN IMPORTS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
from	flask_admin 							import Admin, AdminIndexView
from 	flask_admin.model 				import typefmt
from 	flask_admin.model.widgets import XEditableWidget


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### FLASK-PYMONGO IMPORTS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
from flask_pymongo import PyMongo
# from solidata_api.core.queries_db import MongoCollection

# declare mongo empty connector
mongo = PyMongo()


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### FLASK-MAIL IMPORTS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
# from flask_mail import Mail
# mail = Mail()



### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### CREATE APP
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
# application factory, see: http://flask.pocoo.org/docs/patterns/appfactories/

def create_app(app_name='SOLIDATA_API'):  

	log.debug ("... creating app ...")

	app = Flask(app_name)

	app.config.from_object('solidata_api.config.BaseConfig')

	log.debug("... app.config :\n %s", pformat(app.config))
	print()

	mongo.init_app(app)

	# access mongodb collections
	with app.app_context() :

		from solidata_api._core.queries_db import db, \
			mongo_users,mongo_licences,mongo_projects,mongo_datamodels, \
			mongo_datamodels_fields,mongo_connectors, \
			mongo_datasets_inputs,mongo_datasets_outputs, \
			mongo_recipes,mongo_corr_dicts


	## DEBUG
	find_one_user = mongo_users.find({'infos.name': "Julien"})
	# find_one_user = db["mongo_users"].find({'infos.name': "Julien"})
	log.debug("DEBUG : find_one_user : \n%s", pformat(list(find_one_user)))
	print()


	### registering all blueprints
	from solidata_api.api.api_users 		import blueprint as api_users
	app.register_blueprint( api_users, url_prefix="/api/users" )

	# from solidata_api.api.api_projects 	import blueprint as api_projects
	# app.register_blueprint( api_projects, url_prefix='/api/projects')



	### DEBUG
	# @app.before_request
	# def debug_stuff():
  # 	# pass
	# 	log.debug ("\n%s", pformat(current_app.__dict__))


	return app