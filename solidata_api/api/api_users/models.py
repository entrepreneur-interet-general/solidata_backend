# -*- encoding: utf-8 -*-

"""
api_users/models.py  
- provides the models for PAGINATION definition in DB and Flask-Restplus
"""

from flask_restplus import fields

### import data serializers
from solidata_api._serializers.schema_users import *  

### iomport API namespaces
# from .endpoint_users import ns as ns_users
# from .endpoint_user_edit import ns as ns_user_edit

### create models from serializers
# nested models : https://github.com/noirbizarre/flask-restplus/issues/8
# model_user_infos 	= ns.model( "User model", user_infos) #, mask="{name,surname,email}" )



class NewUser : 

	def __init__(self, ns_):
		self.mod = ns_.model( "User_register", user_register )
	
	@property
	def model(self): 
		return self.mod


class User : 

	def __init__(self, ns_) :

		self.mod        = ns_.model('User', {
				'infos': fields.Nested(
					ns_.model('User_public_data', user_basics )
				),
				'auth': fields.Nested(
					ns_.model('User_authorizations',  user_auth  )
				),
				'preferences': fields.Nested(
					ns_.model('User_preferences',  user_preferences  )
				),
				'datasets': fields.Nested(
					ns_.model('User_datasets',  user_datasets  )
				),
		})

	@property
	def model(self): 
		return self.mod
