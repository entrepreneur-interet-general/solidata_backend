

from log_config import log, pformat
log.debug("... importing all common vars and libs from solidata.api root")

import 	os
from		copy import copy, deepcopy
from  	datetime import datetime, timedelta
import 	json
from	bson import json_util
from	bson.objectid import ObjectId
from	bson.json_util import dumps
# from 	werkzeug.datastructures import ImmutableMultiDict
import 	operator

import 	pandas as pd
import 	numpy as np
import 	requests

from 	flask 				import Blueprint, current_app as app, url_for, request, render_template

from 	werkzeug.security 	import 	generate_password_hash, check_password_hash

from 	flask_restplus 		import Api, Namespace, Resource, fields, marshal, reqparse

### cf : https://stackoverflow.com/questions/47508257/serving-flask-restplus-on-https-server
# class MyApi(Api):
# 	@property
# 	def specs_url(self):
# 		"""Monkey patch for HTTPS"""
# 		# log.debug("self.base_url : %s" , self.base_url)
# 		# log.debug("app.config['RUN_MODE'] : %s" , app.config["RUN_MODE"])
# 		scheme = 'http' if "http" in self.base_url else 'https'
# 		# scheme = 'https' if app.config["RUN_MODE"] in ["prod","preprod"] else 'http'
# 		# scheme = 'http' if app.config["ENV"] in ["dev"] or app.config["DOMAIN_PORT"] in self.base_url else 'https'
# 		# scheme = 'http' if app.config["DOMAIN_PORT"] in self.base_url else 'https'
# 		return url_for(self.endpoint('specs'), _external=True, _scheme=scheme)

import jwt
from flask_jwt_extended import (
		jwt_required, jwt_optional, jwt_refresh_token_required, fresh_jwt_required,
		create_access_token, create_refresh_token, decode_token,
		get_jwt_identity, get_jwt_claims, get_raw_jwt,
)


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### generate RSA key
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

import Crypto
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP, PKCS1_v1_5
from Crypto import Random

import ast
from base64 import b64decode, b64encode


# cf : https://stackoverflow.com/questions/44892946/rsa-encryption-in-python-decrypt-in-js
# cf : https://pythonhosted.org/pycrypto/Crypto.PublicKey.RSA._RSAobj-class.html#exportKey 
# cf : https://www.pycryptodome.org/en/latest/src/examples.html 
random_generator 	= Random.new().read
key_pair 			= RSA.generate(1024, random_generator)

private_key_str		= key_pair.exportKey().decode("utf-8")
log.debug("private_key_str : \n %s", pformat(private_key_str))

public_key 			= key_pair.publickey()
public_key_str		= public_key.exportKey().decode("utf-8")
log.debug("public_key_str : \n %s", pformat(public_key_str))

# cf : https://medium.com/@DannyAziz97/rsa-encryption-with-js-python-7e031cbb66bb
# cf : https://stackoverflow.com/questions/44427934/notimplementederror-use-module-crypto-cipher-pkcs1-oaep-instead-error
# decryptor 			= PKCS1_OAEP.new(key_pair, hashAlgo=SHA256)

cipher = PKCS1_v1_5.new(key_pair)

def RSAencrypt(msg_clear):
	log.debug("\ \ / / msg_clear    : \n%s", msg_clear )
	ciphertext = cipher.encrypt(msg_clear.encode('utf8'))
	return b64encode(ciphertext).decode('ascii')

def RSAdecrypt(msg_encrypted):
	log.debug("\ \ / / msg_encrypted    : \n%s", msg_encrypted )
	ciphertext = b64decode(msg_encrypted.encode('ascii'))
	log.debug("\ \ / / ciphertext    : \n%s", ciphertext )
	plaintext = cipher.decrypt(ciphertext, b'DECRYPTION FAILED')
	log.debug("\ \ / / plaintext    : \n%s", plaintext )
	return plaintext.decode('utf8')
	
### TEST ENCRYPT
ciphertext = RSAencrypt('a-very-common-password')
log.info("/ / \ \ ciphertext : \n%s", ciphertext)
### TEST DECRYPT
plaintext = RSAdecrypt(ciphertext)
log.info("/ / \ \ plaintext : \n%s", plaintext)

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### DEBUGGING CONFIRMAITON EMAIL 
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
# from solidata_api._auth import generate_confirmation_token

# from solidata_api.application import mongo


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### import CORS settings
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
from solidata_api._core.cors 			import CORS, cross_origin

# ### import data serializers
# from solidata_api._serializers.schema_users import *  

from solidata_api._auth.authorizations 	import authorizations as auth_check

from solidata_api._auth 				import ( 
	admin_required, current_user_required, confirm_email_required, guest_required,
	anonymous_required, renew_pwd_required, reset_pwd_required 
	)

from solidata_api._parsers 	import * # pagination_arguments
# from solidata_api._parsers.parser_pagination 	import * # pagination_arguments
# from solidata_api._parsers.parser_queries 		import * # query_arguments
# from solidata_api._parsers.parser_files 		import * # files_arguments

from solidata_api._choices 			import bad_passwords, authorized_filetypes, authorized_mimetype

from solidata_api._core.utils 		import * # create_modif_log, secure_filename, allowed_file, return_payload
from solidata_api._core.pandas_ops 	import * # create_modif_log, secure_filename, allowed_file
from solidata_api._core.emailing 	import send_email

### import mongo utils
from solidata_api._core.queries_db 	import *



