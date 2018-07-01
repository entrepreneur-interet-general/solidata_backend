# -*- encoding: utf-8 -*-

"""
_auth.__init__.py.py  
- creates a authorizations description
- creates a token_required decorator
"""

from .auth_decorators import admin_required, current_user_required # token_required
from .authorizations import authorizations
# from .auth_confirmation_email import generate_confirmation_token, confirm_token