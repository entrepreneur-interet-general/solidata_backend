# -*- encoding: utf-8 -*-

"""
endpoint_usr.py  
- provides the API endpoints for consuming and producing
	REST requests and responses
"""

from solidata_api.api import *

log.debug(">>> api_users ... creating api endpoints for USERS")

### create namespace
ns = Namespace('list', description='Users : users lists related endpoints ')

### import models 
from solidata_api._models.models_user import *  
model_new_user  = NewUser(ns).model
model_user_out	= User_infos(ns).model_complete_out





### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 


@ns.doc(security='apikey')
@ns.route('/')
class Users_List(Resource):

	### TO DO  : pagination arguments
	@ns.doc('users_list')
	# @ns.expect(pagination_arguments)
	@jwt_optional
	# @ns.marshal_list_with( model_user_out, skip_none=True) #, envelop="users_list" ) 
	def get(self):
		"""
		List of all users in db

		>
			--- needs   : nothing - optionnal args : pagination, list of oid_usr, list of tags, query
			>>> returns : msg, users data as a list

		"""
		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )

		### DEBUG check
		log.debug ("payload : \n{}".format(pformat(ns.payload)))

		### check client identity and claims
		claims 			= get_jwt_claims() 
		log.debug("claims : \n %s", pformat(claims) )

		user_id 		= get_jwt_identity() ### get the oid as str
		log.debug('user_identity from jwt : \n%s', user_identity )  
		if user_id : 
			# user_id 		= claims["_id"]
			user_oid		= ObjectId(user_id)
			user_role 		= claims["auth"]["role"]

		### get pagination arguments
		page_args		= pagination_arguments.parse_args(request)
		log.debug('page_args : \n%s', pformat(page_args) )  
		page 			= page_args.get('page', 1)
		per_page 		= page_args.get('per_page', 10)

		### get query arguments
		query_args		= query_arguments.parse_args(request)
		log.debug('query_args : \n%s', pformat(query_args) )  




		### TO DO 
		### retrieve from db
		cursor 		= mongo_users.find({})
		users		= list(cursor)
		log.debug( "users : \n %s", pformat(users) )

		### marshall results given user's role
		users_out = marshal( users , model_user_out )


		return { 
					"msg"	: "dear admin, there is the users list... ", 
					"data"  : users 
				}, 200







