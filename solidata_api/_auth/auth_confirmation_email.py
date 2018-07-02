# -*- encoding: utf-8 -*-

"""
auth_confirmation_email.py  
- create safe email to confirm user
"""

from log_config import log, pprint, pformat
log.debug ("... loading token_required ...")

from flask import current_app as app

from itsdangerous import URLSafeTimedSerializer



### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### !!! - DEPRECATED - 
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

### cf : https://realpython.com/handling-email-confirmation-in-flask/ 

def generate_confirmation_token(email):
	"""
	generate a confirmation email sent once registred
	"""
	serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
	return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
	"""
	confirm the email 
	"""
	serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
	try:
			email = serializer.loads(
					token,
					salt=app.config['SECURITY_PASSWORD_SALT'],
					max_age=expiration
			)
	except:
			return False
	return email
