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
class UsersList(Resource):

	### TO DO  : pagination arguments
	@ns.doc('users_list')
	@admin_required
	@ns.expect(pagination_arguments)
	@ns.marshal_list_with( model_user_out, skip_none=True) #, envelop="users_list" ) 
	def get(self):
		"""
		List of all users in db (without _id)

		>
			--- needs   : a valid admin access_token in the header
			>>> returns : msg, users data as a list
		"""
		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )
		log.debug ("payload : \n{}".format(pformat(ns.payload)))

		### DEBUG check
		user_identity = get_jwt_identity()
		log.debug('user_identity from jwt : \n%s', user_identity )  

		### TO DO : get pagination
		args 			= pagination_arguments.parse_args(request)
		page 			= args.get('page', 1)
		per_page 	= args.get('per_page', 10)

		### retrieve from db
		cursor 	= mongo_users.find({}, {"_id": 0 })
		users		= list(cursor)
		log.debug( "users : \n %s", pformat(users) )

		return { 
							"msg"					: "dear admin, there is the users list... ", 
							"users_list"  : users 
					}, 200







