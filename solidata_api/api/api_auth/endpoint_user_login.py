# -*- encoding: utf-8 -*-

"""
endpoint_user_login.py  
"""

from solidata_api.api import *

log.debug(">>> api_auth ... creating api endpoints for USER_LOGIN")

### import mongo utils
from solidata_api._core.queries_db import mongo_users

### create namespace
ns = Namespace('login', description='User : login related endpoints')

### import models 
from solidata_api._models.models_user import LoginUser, User_infos, AnonymousUser
model_login_user  		= LoginUser(ns).model
model_user						= User_infos(ns)
model_user_access			= model_user.model_access
model_user_login_out	= model_user.model_login_out


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### DECRYPTION
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

# import Crypto
# from Crypto.PublicKey import RSA


# cf : https://github.com/berlincode/sjcl
# from sjcl import SJCL
# cyphertext = SJCL().encrypt( b"secret message to encrypt", "shared_secret")
# log.debug ("cyphertext : %s", cyphertext)
# cyphertext_decrypt = SJCL().decrypt(cyphertext, "shared_secret")
# log.debug ("cyphertext_decrypt : %s",cyphertext_decrypt )



# import base64
# import urllib
# import binascii

# from Crypto.Cipher import AES

# # KEY = 'This is a key123'
# IV = 'IV_solidata'
# MODE = AES.MODE_CFB
# BLOCK_SIZE = 16
# SEGMENT_SIZE = 128

# # cf : https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256 

# def decrypt_AES( cipher_text, key):
	
# 	log.debug ("\ncipher_text : \n%s", pformat(cipher_text))

# 	decryption_suite = AES.new(key, AES.MODE_CBC, IV)
# 	plain_text = decryption_suite.decrypt(cipher_text)

# 	# encodedEncrypted = urllib.parse.unquote(quotedEncodedEncrypted)
# 	# log.debug ("encodedEncrypted : %s", pformat(encodedEncrypted))

# 	# cipher = AES.new(key)
# 	# log.debug ("cipher : %s", pformat(cipher))

# 	# decrypted = cipher.decrypt(base64.b64decode(encodedEncrypted))[:16]
# 	# log.debug ("decrypted : %s", pformat(decrypted))

# 	# for i in range(1, len(base64.b64decode(encodedEncrypted))/16):
		
# 	# 	cipher = AES.new(key, AES.MODE_CBC, base64.b64decode(encodedEncrypted)[(i-1)*16:i*16])
# 	# 	log.debug ("cipher : %s", pformat(cipher))
		
# 	# 	decrypted += cipher.decrypt(base64.b64decode(encodedEncrypted)[i*16:])[:16]
# 	# 	log.debug ("decrypted : %s", pformat(decrypted))

# 	# log.debug ("decrypted.strip() : %s", pformat(decrypted.strip()))
# 	# return decrypted.strip()


# # cf : https://chase-seibert.github.io/blog/2016/01/29/cryptojs-pycrypto-ios-aes256.html



# def encrypt(key, iv, plaintext):
# 	aes = AES.new(key, MODE, iv, segment_size=SEGMENT_SIZE)
# 	plaintext = _pad_string(plaintext)
# 	encrypted_text = aes.encrypt(plaintext)
# 	return binascii.b2a_hex(encrypted_text).rstrip()

# def decrypt(key, iv, encrypted_text):
# 	aes = AES.new(key, MODE, iv, segment_size=SEGMENT_SIZE)
# 	encrypted_text_bytes = binascii.a2b_hex(encrypted_text)
# 	decrypted_text = aes.decrypt(encrypted_text_bytes)
# 	decrypted_text = _unpad_string(decrypted_text)
# 	return decrypted_text

# def _pad_string(value):
# 	length = len(value)
# 	pad_size = BLOCK_SIZE - (length % BLOCK_SIZE)
# 	return value.ljust(length + pad_size, '\x00')

# def _unpad_string(value):
# 	while value[-1] == '\x00':
# 		value = value[:-1]
# 	return value

# # if __name__ == '__main__':
# # 	input_plaintext = 'The answer is no'
# # 	encrypted_text = encrypt(KEY, IV, input_plaintext)
# # 	decrypted_text = decrypt(KEY, IV, encrypted_text)
# # 	assert decrypted_text == input_plaintext


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 

# @cross_origin()
@ns.route('/anonymous/')
class AnonymousLogin(Resource):

	@ns.doc('user_anonymous')
	@ns.doc(responses={200: 'success : anonymous user created with its access and refresh tokens'})
	def get(self):
		"""
		Login as anonymous user

		>
			--- needs   : nothing in particular
			>>> returns : msg, anonymous access_token + anonymous refresh_token with a short expiration date
		"""

		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )

		### create a fake user 
		anon_user_class = AnonymousUser()
		anonymous_user 	= anon_user_class.__dict__

		### create corresponding access token
		anonymous_access_token		= create_access_token(identity=anonymous_user) #, expires_delta=expires)

		### create a random string for later login / register encryption in frontend
		anonymous_access_token_decoded	= decode_token(anonymous_access_token)
		log.debug("anonymous_access_token_decoded : \n %s", pformat(anonymous_access_token_decoded) )
		# salt_token	= anonymous_access_token_decoded['jti']
		# salt_token	= salt_token.replace("-", "")
		salt_token 		= public_key_str #.decode("utf-8")

		### create corresponding refresh token
		expires 					= app.config["JWT_ANONYMOUS_REFRESH_TOKEN_EXPIRES"]
		anonymous_refresh_token		= create_refresh_token(identity=anonymous_user, expires_delta=expires)

		log.debug("anonymous_access_token 	: \n %s", anonymous_access_token )
		log.debug("anonymous_refresh_token 	: \n %s", anonymous_refresh_token )
		log.debug("salt_token 					: \n %s", salt_token )

		### store tokens in dict
		tokens = {
					'access_token' 	: anonymous_access_token,
					'refresh_token' : anonymous_refresh_token,
					'salt_token' 	: salt_token,
				}

		return {	
					"msg" 		: "anonymous user - an anonymous access_token has been created + a valid refresh_token for {} hours".format(expires) , 
					"tokens"	:  tokens
				}, 200



@ns.route('/')
class Login(Resource):

	@ns.doc('user_login')
	@ns.doc(security='apikey')
	@ns.expect(model_login_user)
	@anonymous_required
	@ns.doc(responses={200: 'success : user logged with its access and refresh tokens'})
	@ns.doc(responses={401: 'error client : incorrect login or no user'})
	def post(self):
		"""
		Log in an user given an email and a password 
		- checks if email exists in db 
		- check if salted pwd is equals to user's

		>
			--- needs   : an anonymous access_token (please use '.../login/anonymous/' first)
			>>> returns : msg, is_user_confirmed, preferences, access_token, refresh_tokens
		"""

		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )
		log.debug ("payload : \n{}".format(pformat(ns.payload)))

		### get raw JWT
		raw_jwt 		= get_raw_jwt()
		log.debug("raw_jwt : \n %s", pformat(raw_jwt) )
		# salt_key	= raw_jwt['jti']
		# salt_key	= salt_key.replace("-", "")
		# log.debug("salt_key : \n %s", salt_key )

		### retrieve current user identity from refresh token
		claims 			= get_jwt_claims() 
		log.debug("claims : \n %s", pformat(claims) )
		
		### retrieve infos from form
		# payload_email 				= ns.payload["email"]
		# log.debug("payload_email  : %s", payload_email )
		payload_email_encrypted   	= ns.payload["email_encrypt"]
		log.debug("payload_email_encrypted : \n%s", payload_email_encrypted )
		payload_email = email_decoded = RSAdecrypt(payload_email_encrypted)
		log.debug("email_decoded    : %s", email_decoded )

		# payload_pwd   				= ns.payload["pwd"]
		# log.debug("payload_pwd    : %s", payload_pwd )
		
		### DECYPHERING THE STRING FROM RSA JSENCRYPT IN FRONT !!!!!!
		### get hashed password from pwd_encrypt encoded with salt_key / public_key
		payload_pwd_encrypted   	= ns.payload["pwd_encrypt"]
		log.debug("payload_pwd_encrypted : \n%s", payload_pwd_encrypted )
		payload_pwd = password_decoded = RSAdecrypt(payload_pwd_encrypted)
		log.debug("password_decoded    : %s", password_decoded )

		payload_renew_refr_token   	= ns.payload.get("renew_refresh_token", app.config["JWT_RENEW_REFRESH_TOKEN_AT_LOGIN"] )
		log.debug("payload_renew_refr_token    : %s", payload_renew_refr_token )

		### retrieve user from db
		user = mongo_users.find_one( {"infos.email" : payload_email } ) #, {"_id": 0 })
		log.debug("user : \n %s", pformat(user)) 

		if user == None : 

			log.warning("no user found for - payload_email :%s", payload_email )
			log.warning("no user found for - payload_pwd :%s", payload_pwd )

			error_message = "no such user in db"
			return {	
						"msg" : "incorrect login / {}".format(error_message) 
					}, 401

		if user : 
			
			### check password
			pwd = user["auth"]["pwd"]

			if check_password_hash(pwd, payload_pwd) :
    
				### marshal user's info 
				# user_light 				= marshal( user , model_user_access)
				user_light 				= marshal( user , model_user_login_out)
				# user_light["_id"] 		= str(user["_id"])
				log.debug("user_light : \n %s", pformat(user_light) )

				### Use create_access_token() to create user's new access token 
				log.debug("... access_token")
				new_access_token 	= create_access_token(identity=user_light, fresh=False)

				### create a new refresh_token when logged
				log.debug("... refresh_token : create a new one...")
				if payload_renew_refr_token and user["auth"]["conf_usr"] == True :
					log.debug("... refresh_token")
					expires 					= app.config["JWT_REFRESH_TOKEN_EXPIRES"] 
					refresh_token 				= create_refresh_token( identity=user_light, expires_delta=expires )
					user["auth"]["refr_tok"] 	= refresh_token
				
				### retrieve existing refresh_token from db
				else :
					log.debug("... refresh_token : get existing one...")
					refresh_token 		= user["auth"]["refr_tok"]  

				### store tokens in dict
				tokens = {
						'access_token'	: new_access_token,
						'refresh_token' : refresh_token,
						'salt_token' 	: public_key_str,
				}
				print()
				log.debug("user_light['_id'] : %s", user_light["_id"] )
				log.debug("user_light 		 : \n%s", user_light )
				log.debug("new_access_token  : \n%s", new_access_token )
				log.debug("refresh_token 	 : \n%s", refresh_token )
				print()

				### update user log in db
				# user = create_modif_log(doc=user, action="login")
				user["log"]["login_count"] += 1
				mongo_users.save(user)

				return {	
							"msg"				: "user '{}' is logged".format(payload_email),

							# "is_user_confirmed" : user["auth"]["conf_usr"],
							# "_id"				: str(user["_id"]),
							# "infos"				: user["infos"],
							# "profile"			: user["profile"],
							
							"data"				: user_light,
							"tokens"			: tokens

						}, 200

			else : 

				error_message = "wrong password"
				return { 
							"msg" 				: "incorrect login / {}".format(error_message) 
						}, 401



