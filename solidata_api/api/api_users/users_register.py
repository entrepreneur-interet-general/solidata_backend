# -*- encoding: utf-8 -*-

"""
user_register.py  
- provides the API endpoints for consuming and producing
	REST requests and responses
"""

from flask_restplus import Namespace, Resource
import bcrypt

from . import user_schema

ns = Namespace('user_register', description='User registration ')

model = ns.model( "New user", user_schema, mask="{name,surname,password}" )


@ns.route('/register')
class Register(Resource):
	"""
	register a new user in DB
	"""
	
	@ns.expect(model)
	def post(self, validate=True) :
		"""
		register a new user in DB
		"""
		print(api.payload)
		new_user = api.payload

    ### read payload
    
    ### hash password

    ### add to db
		# users.append(new_user)

		return {"message" : "a new user has been created..."}, 201