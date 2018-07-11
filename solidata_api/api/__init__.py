

from log_config import log, pformat
log.debug("... importing all common vars and libs from solidata.api root")


from	copy import copy, deepcopy
from  datetime import datetime, timedelta
from	bson import json_util
from	bson.objectid import ObjectId
from	bson.json_util import dumps

from flask import Blueprint, current_app as app, url_for, request

from 	werkzeug.security 	import 	generate_password_hash, check_password_hash

from flask_restplus import Api, Namespace, Resource, fields, marshal, reqparse

import jwt
from flask_jwt_extended import (
		jwt_required, jwt_optional, jwt_refresh_token_required, fresh_jwt_required,
		create_access_token, create_refresh_token,
		get_jwt_identity, get_jwt_claims, get_raw_jwt,
)


### DEBUGGING CONFIRMAITON EMAIL 
# from solidata_api._auth import generate_confirmation_token

# from solidata_api.application import mongo

# ### import data serializers
# from solidata_api._serializers.schema_users import *  

from solidata_api._auth.authorizations import authorizations as auth_check

from solidata_api._auth import ( 
	admin_required, current_user_required, confirm_email_required,
	anonymous_required, renew_pwd_required, reset_pwd_required 
	)

from solidata_api._parsers.parser_pagination import pagination_arguments

from solidata_api._serializers._choices_user import bad_passwords

from solidata_api._core.utils import create_modif_log

from solidata_api._core.emailing import send_email

### import mongo utils
from solidata_api._core.queries_db import *
