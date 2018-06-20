# -*- encoding: utf-8 -*-

"""
api_users/models.py  
- provides the models for PAGINATION definition in DB and Flask-Restplus
"""

from flask_restplus import fields

### import data serializers
from solidata_api._serializers.schema_users import *  


### create models from serializers
# nested models : https://github.com/noirbizarre/flask-restplus/issues/8
# model_user_infos 	= ns.model( "User model", user_infos) #, mask="{name,surname,email}" )


# class NewUser : 

# 	def __init__(self, ns_):
# 		self.mod = ns_.model( "User_register", user_register )
	
# 	@property
# 	def model(self): 
# 		return self.mod


class LoginUser : 

	def __init__(self, ns_):
		self.mod = ns_.model( "User_login", user_login )
	
	@property
	def model(self): 
		return self.mod


# class User_out : 

# 	def __init__(self, ns_) :

# 		self.mod_complete  = ns_.model('User', {
# 				'infos': fields.Nested(
# 					ns_.model('User_public_data', user_basics )
# 				),
# 				'auth': fields.Nested(
# 					ns_.model('User_authorizations',  user_auth_out  )
# 				),
# 				'preferences': fields.Nested(
# 					ns_.model('User_preferences',  user_preferences_out  )
# 				),
# 				'datasets': fields.Nested(
# 					ns_.model('User_datasets',  user_datasets_out  )
# 				),
# 		})

# 		self.mod_for_token = ns_.model('User_token', {
# 				'infos': fields.Nested(
# 					ns_.model('User_public_data', user_identity )
# 				),
# 				'auth': fields.Nested(
# 					ns_.model('User_authorizations',  user_auth_out  )
# 				),
# 				'preferences': fields.Nested(
# 					ns_.model('User_preferences',  user_preferences_out  )
# 				),
# 		})

# 	@property
# 	def model(self): 
# 		return self.mod_complete

# 	@property
# 	def model_for_token(self): 
# 		return self.mod_for_token

# class User_in : 

# 	def __init__(self, ns_) :

# 		self.mod        = ns_.model('User', {
# 				'infos': fields.Nested(
# 					ns_.model('User_public_data', user_basics )
# 				),
# 				'auth': fields.Nested(
# 					ns_.model('User_authorizations',  user_auth  )
# 				),
# 				'preferences': fields.Nested(
# 					ns_.model('User_preferences',  user_preferences_in  )
# 				),
# 				'datasets': fields.Nested(
# 					ns_.model('User_datasets',  user_datasets_in  )
# 				),
# 		})

# 	@property
# 	def model(self): 
# 		return self.mod