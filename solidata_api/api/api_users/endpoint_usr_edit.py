# -*- encoding: utf-8 -*-

"""
endpoint_usr_edit.py  
"""

from solidata_api.api import *

log.debug(">>> api_usr ... creating api endpoints for USR_EDIT")

from . import api, document_type

### create namespace
ns = Namespace('edit', description="Users : user's info edition related endpoints")

### import models 
from solidata_api._models.models_updates import * 
from solidata_api._models.models_user import *  
model_doc 				= User_infos(ns)
model_doc_out			= model_doc.model_complete_out
model_doc_guest_out		= model_doc.model_guest_out
model_doc_min			= model_doc.model_minimum
models 				= {
	"model_doc_out" 		: model_doc_out ,
	"model_doc_guest_out" 	: model_doc_guest_out ,
	"model_doc_min" 		: model_doc_min ,
} 
model_data				= UserData(ns).model
model_update	= Update_infos(ns, document_type).model_update_generic

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES 
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 

### cf : response codes : https://restfulapi.net/http-status-codes/ 


@ns.doc(security='apikey')
@ns.route("/<string:user_oid>/")
@ns.response(404, 'document not found')
@ns.param('doc_oid', 'The user unique identifier')
class Usr_edit(Resource) :
		
	"""
	usr edition :
	PUT    - Updates usr infos
	DELETE - Let you delete document
	"""
	
	@ns.doc('update_usr')
	@current_user_required
	def put(self):
		"""
		Update a tag in db
		"""

		return {
					"msg" : "nananana"
				}


	@ns.doc('delete_user')
	@ns.response(204, 'document deleted')
	@current_user_required
	def delete(self, doc_oid):
		"""
		Delete an user given its _id / only doable by admin or current_user
		
		> 
			--- needs   : a valid access_token (as admin or current user) in the header, an user_oid of the user in the request
			>>> returns : msg, response 204 as user is deleted

		"""

		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )

		### DEBUG check
		# log.debug ("payload : \n{}".format(pformat(ns.payload)))

		### check client identity and claims
		claims 				= get_jwt_claims() 
		log.debug("claims : \n %s", pformat(claims) )

		### query db from generic function 		
		results, response_code	= Query_db_delete (
			ns, 
			models,
			document_type,
			doc_id,
			claims,
			roles_for_delete 	= ["admin"],
			auth_can_delete 	= ["owner"],
		)

		log.debug("results : \n%s ", pformat(results) )


		return results, response_code



# @ns.doc(security='apikey')
# @ns.route("/<string:user_oid>/<field_to_update>")
# # @ns.response(404, 'user not found')
# @ns.doc(responses={401: 'error client : incorrect values'})
# @ns.doc(responses={404: 'error client : user not found'})
# # @ns.expect(model_data)
# @ns.param('user_oid', 'The user unique identifier in DB')
# class User_update(Resource) :
		
# 	### TO DO 
# 	@ns.doc('update_user_infos')
# 	@ns.expect(model_data)
# 	@current_user_required
# 	def put(self, user_oid, field_to_update=None) : #, data_oid=None):
# 		"""
# 		TO DO - Update an user given its _id / for client use
# 		only update fields one by one
# 		only takes the following client infos : 
# 		- in URL     : oid, field_to_update
# 		- in payload : the new value to put into the field

# 		--- 

# 		> user_basics : 
# 			- name
# 			- surmame 
# 			- email --> sends a confirmation email with refresh token valid 3 days
		
# 		> user_auth :
# 			- pwd --> sends a confirmation email with refresh token valid 1 days

# 		> user_preferences_in : 
# 			- lang
		
# 		> user_professional : 
# 			- struct_
# 			- profiles
		
# 		>
# 			--- needs 	: a valid access_token (as admin or current user) in the header, an user_oid of the user + the field to update in the request
# 			>>> returns : msg, updated data copy

# 		"""

# 		### DEBUGGING
# 		print()
# 		print("-+- "*40)
# 		log.debug("ROUTE class : %s", self.__class__.__name__ )
# 		log.debug("user_oid : %s", user_oid)

# 		### check if client is an admin or if is the current user
# 		claims 					= get_jwt_claims() 
# 		log.debug("claims : \n %s", pformat(claims) )
# 		is_client_admin = claims["auth"]["role"]


# 		### retrieve user's data from payload
# 		user_updated_data = copy(ns.payload["data"])
# 		log.debug("user_updated_data : \n %s", pformat(user_updated_data) ) 

# 		### retrieve personnal infos from user in db
# 		user = mongo_users.find_one({"_id" : ObjectId(user_oid)})
# 		log.debug("user : \n %s", pformat(user))


# 		if user : 

# 			### update user info from data in pyaload
# 			if field_to_update in user_fields_admin_can_update_list : 
				
# 				log.debug("field_to_update in admin authorized fields : %s", field_to_update )

# 				### stop from updating not authorized field if client is not admin
# 				if is_client_admin != "admin" and field_to_update not in user_fields_client_can_update_list : 
# 					return {
# 							"msg"		  : "you are not authorized to update the field '{}'".format(field_to_update),
# 					}, 401


# 				else : 

# 					field_root 			= user_fields_dict[field_to_update]["field"]
# 					original_data		= user[field_root][field_to_update]

# 					if user_updated_data != original_data : 

# 						### marshall user in order to make tokens
# 						user_light 			= marshal( user, model_user_out )
# 						user_light["_id"] 	= str(user["_id"])

# 						### special function for user's email update
# 						if field_to_update == "email" :
								
# 							### add confirm_email claim
# 							user_light["confirm_email"]	= True
# 							expires 										= app.config["JWT_CONFIRM_EMAIL_REFRESH_TOKEN_EXPIRES"] # timedelta(days=7)
# 							access_token 								= create_access_token(identity=user_light, expires_delta=expires)

# 							### send a confirmation email if not RUN_MODE not 'dev'
# 							if app.config["RUN_MODE"] in ["prod", "dev_email"] : 
								
# 								# create url for confirmation to send in the mail
# 								confirm_url = app.config["DOMAIN_NAME"] + api.url_for(Confirm_email, token=access_token_confirm_email, external=True)
# 								log.info("confirm_url : \n %s", confirm_url)

# 								# generate html body of the email
# 								html = render_template('emails/confirm_email.html', confirm_url=confirm_url)
								
# 								# send the mail
# 								send_email( "Confirm your email", payload_email, template=html )
						
# 							### flag user's email as not confirmed
# 							user["auth"]["conf_usr"] = False


# 						### special function for user's pwd update 
# 						### WARNING --> only admin can access and create new password for users...
# 						if field_to_update == "pwd" :
# 								### create new hashpassword
# 								user_updated_data = generate_password_hash(user_updated_data, method='sha256')
# 								log.debug("hashpass : %s", hashpass)

# 						### update value in marshalled user
# 						if field_to_update != "pwd" : 
# 							user_light[ field_root ][ field_to_update ] = user_updated_data

# 						### update data in DB
# 						user[ field_root ][ field_to_update ] = user_updated_data
						
# 						### update modfication in user data
# 						user = create_modif_log(doc=user, action="update " + field_to_update )
# 						# modif = {"modif_at" : datetime.utcnow(), "modif_for" : field_to_update }
# 						# user["log"]["modified_log"].insert(0, modif)

# 						mongo_users.save(user)



# 						return { 
# 									"msg" 				: "updating user {} ".format(user_oid), # DAO.update(id, api.payload)
# 									"field_updated"		: field_to_update,
# 									# "new_tokens"		: user_updated_data
# 								}, 200


# 					else : {
# 								"msg"	: "no difference between previous and sent data for field '{}'".format(field_to_update),
# 							}, 201
	
# 			else : 
# 				return {
# 							"msg"	: "impossible to update the field '{}'".format(field_to_update),
# 						}, 401


# 		else : 
# 			return {
# 					"msg"	: "user oid '{}' not found".format(user_oid),
# 			}, 401





