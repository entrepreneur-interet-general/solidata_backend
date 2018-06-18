# -*- encoding: utf-8 -*-

"""
api_users/models.py  
- provides the models for PAGINATION definition in DB and Flask-Restplus
"""

from flask_restplus import fields

### import data serializers
from solidata_api._serializers.schema_users import *  

### iomport API namespace
from .endpoints import ns

### create models from serializers
# nested models : https://github.com/noirbizarre/flask-restplus/issues/8

# model_user_infos 	= ns.model( "User model", user_infos) #, mask="{name,surname,email}" )
model_new_user 		= ns.model( "User_register", user_register )

model_user        = ns.model('User', {
		'infos': fields.Nested(
			ns.model('User_public_data', user_basics )
		),
		'auth': fields.Nested(
			ns.model('User_authorizations',  user_auth  )
		),
		'preferences': fields.Nested(
			ns.model('User_preferences',  user_preferences  )
		),
		'datasets': fields.Nested(
			ns.model('User_datasets',  user_datasets  )
		),
})