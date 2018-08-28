# -*- encoding: utf-8 -*-

"""
_choices_user.py  
- all choices related to user UX
"""
from copy import copy, deepcopy

from log_config import log, pformat

log.debug("... loading _choices_user.py ...")


from ._choices_docs import * 

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### CHOICES ONLY FOR ADMIN
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

user_roles = [
	"admin", 
	"staff",   ### can edit all datamodels : dmf + dmt
	# "collective", 
	"registred", 
	"guest", ### not registred yet
	"anonymous"
]

bad_passwords = [ 
	'test', 
	'password', 'Password',
	'12345' 
]

user_edit_auth = [
	"owner",
	"can_edit",
	# "can_edit_all",
	# "can_edit_prj",
	# "can_edit_dmt",
	# "can_edit_dmf",
	# "can_edit_dsi",
	# "can_edit_rec",
	"can_view",
]



### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### CHOICES FOR USERS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

### user fields as recorded in DB - most exhaustive
### check 'schema_users.py' for coherence and description
user_fields_admin_can_update = {
	"infos" 				: ["name", "surname", "email"], 
	"auth" 					: ["pwd", "conf_usr", "role", "refr_tok", "is_blacklisted"],
	# "preferences" 		: ["lang", "fav_list"],
	# "datasets" 			: doc_type_list,
	"datasets"				: [ ds+"_list" for ds in doc_type_list ],
	"profile" 				: ["lang", "usr_profiles"],
	"professional_infos"	: ["structure", "struct_profiles", "structure_url"]
}


user_fields_admin_can_update_list = [ ]
user_fields_dict 									= { }
for k,v in user_fields_admin_can_update.items() : 
	for i in v :
		user_fields_admin_can_update_list.append(i)
		user_fields_dict[i] = { "field" : k }


user_fields_client_can_update 				= deepcopy(user_fields_admin_can_update)
# user_fields_client_can_update["auth"] = ["pwd"]
del user_fields_client_can_update["auth"]

user_fields_client_can_update_list = [ ]
# user_fields_client_can_update_dict = { }
for k,v in user_fields_client_can_update.items() : 
	for i in v :
		user_fields_client_can_update_list.append(i)
		# user_fields_client_can_update_dict[i] = {"field" : k}



log.debug("user_fields_admin_can_update_list : \n %s", pformat(user_fields_admin_can_update_list))
log.debug("user_fields_dict : \n %s", pformat(user_fields_dict))
log.debug("user_fields_client_can_update_list : \n %s", pformat(user_fields_client_can_update_list))
# log.debug("user_fields_client_can_update_dict : \n %s", pformat(user_fields_client_can_update_dict))




### choices about user's profiles

user_profiles = [
	"helper",
	"analyst",
	"financer",
	"observer",
	"project_holder",
	"citizen",
	"other"
]

user_structure = [
	"association",
	"citizen_collective",
	"public_collective",
	"cooperative",
	"entreprise_more_50",
	"entreprise_50",
	"entreprise_10",
	"independant",
	"finance",
	"foundation",
	"mutual",
	"public_state",
	"public_other", 
	"other"
]
