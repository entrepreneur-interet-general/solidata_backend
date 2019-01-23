# -*- encoding: utf-8 -*-

"""
endpoint_usr_register.py  
"""

from solidata_api.api import *

log.debug(">>> api_users ... creating api endpoints for USER_REGISTER")

from . import api, document_type

### create namespace
ns = Namespace('register', description='Users : register related endpoints')

### import models 
from solidata_api._models.models_user import *  
model_register_user			= NewUser(ns).model
model_user							= User_infos(ns)
model_register_user_out	= model_user.model_complete_out
model_user_complete_in	= model_user.model_complete_in
model_user_access				= model_user.model_access
model_user_login_out		= model_user.model_login_out

models 			= {
	"model_doc_in" 			: model_user_complete_in ,
	"model_doc_out" 		: model_register_user_out 
} 

### CREATE DEFAULT USRs FROM config_default_docs
### import default documents 
from solidata_api.config_default_docs import default_system_user_list
for dft_usr in default_system_user_list : 
	
	log.debug ("dft_usr : \n{}".format(pformat(dft_usr)))
	
	Query_db_insert(
		ns, 
		models,
		document_type,

		dft_usr,

		value_to_check 	= dft_usr["auth"]["role"],
		field_to_check	= "auth.role",

		user_role   	= "system"
	)

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 


@ns.doc(security='apikey')
@ns.route('/')
class Register(Resource):
	
	@ns.doc('usr_register')
	@ns.doc(security='apikey')
	@ns.expect(model_register_user, validate=True)
	@anonymous_required
	# @ns.marshal_with(model_register_user_out, envelope="new_user", code=201)
	def post(self):
		"""
		Create / register a new user

		>
			--- needs   : an anonymous access_token, an email, a name, a surname and and a password
			>>> returns : msg, access_token + refresh_token for not confirmed email, user's data marshalled 
		"""
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )
		log.debug ("payload : \n{}".format(pformat(ns.payload)))

		### TO DO = add a ghost field to filter out spams and robots

		### retrieve infos from form 
		# payload_email 			= ns.payload["email"]
		# payload_pwd 			= ns.payload["pwd"]
		# log.debug("email : %s", payload_email )
		# log.debug("password : %s", payload_pwd )
		
		payload_email_encrypted = ns.payload["email_encrypt"]
		log.debug("payload_email_encrypted : \n%s", payload_email_encrypted )
		payload_email = email_decoded = RSAdecrypt(payload_email_encrypted)
		log.debug("email_decoded    : %s", email_decoded )

		payload_pwd_encrypted = ns.payload["pwd_encrypt"]
		log.debug("payload_pwd_encrypted : \n%s", payload_pwd_encrypted )
		payload_pwd = password_decoded = RSAdecrypt(payload_pwd_encrypted)
		log.debug("password_decoded    : %s", password_decoded )

		### chek if user already exists in db
		existing_user = mongo_users.find_one({"infos.email" : payload_email})
		log.debug("existing_user : %s ", pformat(existing_user))

		if existing_user is None and payload_pwd not in bad_passwords and payload_email != "anonymous" :

			### create hashpassword
			hashpass = generate_password_hash(payload_pwd, method='sha256')
			log.debug("hashpass : %s", hashpass)

			### create user dict from form's data
			new_user_infos 	= {
				"infos" 	: ns.payload, 
				# "auth" 	: ns.payload 
				"log"		: { "created_at" 	: datetime.utcnow() },
				"profile" 	: { "lang" 		: ns.payload["lang"]}
			}
			new_user 															= marshal( new_user_infos , model_user_complete_in )
			new_user["auth"]["pwd"] 							= hashpass
			new_user["infos"]["email"]						= payload_email
			new_user["infos"]["open_level_edit"]	= "private"
			new_user["infos"]["open_level_show"]	= "commons"
			new_user["specs"]["doc_type"] 				= "usr"
			new_user["team"] 											= []

			### agreement to terms and conditions
			new_user["infos"]["agreement"]				= ns.payload["agreement"]

			### temporary save new user in db 
			_id = mongo_users.insert( new_user )
			log.info("new user is being created : \n%s", pformat(new_user))
			log.info("_id : \n%s", pformat(_id))

			### add _id to data
			new_user["_id"] 				= str(_id) # str(user_created["_id"])
			
			### create access tokens
			log.debug("... create_access_token")
			access_token 	= create_access_token( identity=new_user )
			
			### create refresh tokens
			log.debug("... refresh_token")
			### just create a temporary refresh token once / so it could be blacklisted
			expires 				= app.config["JWT_CONFIRM_EMAIL_REFRESH_TOKEN_EXPIRES"] # timedelta(days=7)
			refresh_token 	= create_refresh_token( identity=new_user, expires_delta=expires )
			
			### add confirm_email to claims for access_token_confirm_email
			new_user["confirm_email"]	 = True
			access_token_confirm_email = create_access_token( identity=new_user, expires_delta=expires )
			log.debug("access_token_confirm_email : \n %s", access_token_confirm_email )

			tokens = {
					'access_token'		: access_token,
					'refresh_token'		: refresh_token,
					'salt_token' 			: public_key_str,
					# 'access_token_confirm_email' 	: access_token_confirm_email
			}
			log.info("tokens : \n %s", pformat(tokens))

			### update new user in db		
			# user_created = mongo_users.find_one({"infos.email" : payload_email})
			user_created = mongo_users.find_one({"_id" : _id})
			user_created["log"]["created_by"] 	= _id
			user_created["auth"]["refr_tok"] 	= refresh_token
			mongo_users.save(user_created)
			log.info("new user is updated with its tokens : \n%s", pformat(new_user))

			### marshall output
			new_user_out = marshal( new_user, model_register_user_out )

			message = "new user has been created but no confirmation link has been sent"

			### send a confirmation email if not RUN_MODE not 'dev'
			if app.config["RUN_MODE"] in ["prod", "dev_email"] : 
				
				try : 
					# create url for confirmation to send in the mail
					confirm_url = app.config["DOMAIN_NAME"] + api.url_for(Confirm_email, token=access_token_confirm_email, external=True)
					log.info("confirm_url : \n %s", confirm_url)

					# generate html body of the email
					html = render_template('emails/confirm_email.html', confirm_url=confirm_url)
					
					# send the mail
					send_email( "Confirm your email", payload_email, template=html )

					message = "new user has been created and a confirmation link has been sent, you have {} days to confirm your email, otherwise this account will be erased...".format(expires)
			
				except : 
					message = "new user has been created but error occured while sending confirmation link to the email"

			return { 
						"msg"			: message,
						"expires"	: str(expires), 
						"tokens"	: tokens,
						"_id"			: str(user_created["_id"]),
						"infos"		: user_created["infos"],
						"data"		: new_user_out,
					}, 200

		else :
			
			return {
						"msg" : "email '{}' is already taken ".format(payload_email)
					}, 401



@ns.doc(security='apikey')
@ns.route("/confirm_email")
@ns.response(404, 'error in the redirection to confirm email')
@ns.param('token', 'The token sent by email when registering to confirm your email')
class Confirm_email(Resource):

	# The config  query paramater where the JWT is looked for is `token`,
	# The default query paramater where the JWT is looked for is `jwt`,
	# and can be changed with the JWT_QUERY_STRING_NAME option.
	# Making a request to this endpoint would look like:
	# /confirm?token=<REFRESH_TOKEN>
	@ns.doc('confirm_email')
	# @jwt_required 
	# @jwt_refresh_token_required ### verify refresh_token from request args or header
	@confirm_email_required
	def get(self):
		"""
		URL to confirm email sent once registered or when change email

		> 
			--- needs   : access_token_confirm_email as URL argument like : 
				'.../api/users/register/confirm?token=<access_token_confirm_email>'
			>>> returns : msg, access_token, refresh_tokens
		"""
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )

		user_identity = get_jwt_identity()
		log.debug( "user_identity : \n %s", user_identity ) 


		### check client identity and claims
		claims 				= get_jwt_claims() 
		log.debug("claims : \n %s", pformat(claims) )


		### !!! only works with access_token
		# claims = get_jwt_claims() 
		# log.debug(" claims : \n %s ", pformat(claims) )
		### retrieve and read token to get user's email
		# user_oid 		= claims["_id"]

		### find user created in db 
		user_to_confirm 	= mongo_users.find_one({"_id" : ObjectId(user_identity)})
		# user_to_confirm 	= mongo_users.find_one({"infos.email" : user_identity })

		if user_to_confirm : 

			### marshal user infos to create token
			user_light 					= marshal( user_to_confirm , model_user_login_out)
			user_light["_id"] 	= str(user_to_confirm["_id"])
			log.debug( "user_light : \n %s", pformat(user_light) ) 

			### create a new access token
			access_token = create_access_token(identity=user_light)

			### check if user is already confirmed
			is_confirmed 		= user_to_confirm["auth"]["conf_usr"] 
			is_blacklisted 	= user_to_confirm["auth"]["is_blacklisted"] 

			### user is not confirmed yet
			if is_confirmed == False and is_blacklisted == False :

				### renew the existing refresh token as a more valid token 
				refresh_token = create_refresh_token(identity=user_light)
				
				### confirm user's email and create a real refresh_token
				user_to_confirm["auth"]["refr_tok"] = refresh_token
				user_to_confirm["auth"]["role"] 	= "registred"
				user_to_confirm["auth"]["conf_usr"] = True

				### register as admin if user is the first to be created and confirmed in collection
				count_users = mongo_users.count()
				if count_users == 1 : 
					user_to_confirm["auth"]["role"] 	= "admin"

				### update modfication in user data
				user_to_confirm = create_modif_log(doc=user_to_confirm, action="confirm_email" )

				### save data
				mongo_users.save(user_to_confirm)

				### store tokens
				tokens = {
							'access_token'	: access_token,
							'refresh_token'	: refresh_token,
							'salt_token' 		: public_key_str,
						}
				log.info("tokens : \n%s", pformat(tokens))

				return { 
							"msg"								: "identity '{}' confirmed, new refresh token created...".format(user_identity),
							"tokens"						: tokens,
							"redirection_link" 	: app.config["REDIRECTION_FRONT"]
						}, 200
			
			### user is already confirmed
			else : 

				### retrieve the existing refresh_token
				refresh_token = user_to_confirm["auth"]["refr_tok"]

				### store tokens
				tokens = {
							'access_token'	: access_token,
							'refresh_token'	: refresh_token,
							'salt_token' 		: public_key_str,
						}
				log.info("tokens : \n%s", pformat(tokens))
				return { 
							"msg" 							: "identity '{}' is already confirmed OR user is blacklisted, existing refresh token is returned...".format(user_identity),
							"tokens"						: tokens,
							"redirection_link" 	: app.config["REDIRECTION_FRONT"]
						}, 201

		### user not found
		else : 

			return { 
						"msg" 		: "user to confirm was not found",
					}, 401