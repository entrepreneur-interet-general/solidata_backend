# -*- encoding: utf-8 -*-

"""
_auth.__init__.py.py  
- creates a authorizations description
- creates a token_required decorator
"""

from log_config import log, pformat
print()
log.debug(">>> _auth.__init__.py ..." )
log.debug(">>> _auth ... loading auth functions and decorators")


from .authorizations import authorizations

from .auth_decorators import ( 
								# import custom decorators
								anonymous_required,
								admin_required, current_user_required, guest_required,
								renew_pwd_required, reset_pwd_required,
								confirm_email_required
							) # token_required
# from .auth_confirmation_email import generate_confirmation_token, confirm_token