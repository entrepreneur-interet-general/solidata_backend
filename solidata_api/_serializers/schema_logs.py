# -*- encoding: utf-8 -*-

"""
schema_logs.py  
- provides the model for LOGS definition in DB and Flask-Restplus
"""

from log_config import log, pformat

from flask_restplus import fields #, marshal

log.debug("... loading schema_logs.py ...")

from .schema_generic import *


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### counts infos
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
count 				= fields.Integer( 
										description		= "count", 
										# attribute		= "count" ,
										required		= False, 
										default			= 0,
									)

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### datetime infos
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
created_at 			= fields.DateTime( 
										description		= "date of creation", 
										attribute		= "created_at" ,
										required		= True, 
										# dt_format		= "rfc822"
									)
modified_at			= fields.DateTime( 
										description		= "date of a modification", 
										attribute		= "modif_at" ,
										required		= True, 
										# dt_format		= "rfc822"
									)
used_at 			= fields.DateTime( 
										description		= "date of use", 
										attribute		= "used_at" ,
										required		= True, 
										# dt_format		= "rfc822"
									)
at 					= fields.DateTime( 
										description		= "date", 
										# attribute		= "at" ,
										required		= True, 
										# dt_format		= "rfc822"
									)
added_at 			= fields.DateTime( 
										description		= "date of addition", 
										attribute		= "added_at" ,
										required		= True, 
										# dt_format		= "rfc822"
									)

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### modified values
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
modified_for		= fields.String(	 
										description		= "action corresponding to a modification",
										attribute		= "modif_for" ,
										required		= True, 
									)

modified_val		= fields.String(	 
										description		= "value of the modification",
										attribute		= "modif_val" ,
										required		= False, 
									)

# used_by 			= fields.String(
# 										description 	= "oid of a document",
# 										attribute		= "used_by",
# 										example			= "5b461ed90a82867e7b114f44",
# 										required		= True,
# 									)
# modified_by 		= fields.String(
# 										description 	= "oid of an user",
# 										attribute		= "modified_by",
# 										example			= "5b461ed90a82867e7b114f44",
# 										required		= True,
# 									)
# added_by 			= fields.String(
# 										description 	= "oid of an user",
# 										attribute		= "added_by",
# 										example			= "5b461ed90a82867e7b114f44",
# 										required		= True,
# 									)


### FOR GENERIC MODELS
# modification 		= {
# 	"modif_at" 		: modified_at,
# 	"modif_for" 	: modified_for
# }

# modification_by 	= {
# 	"modif_at" 		: modified_at,
# 	"modif_for" 	: modified_for,
# 	"modif_by" 		: oid_usr
# }

modification_full = {
	"modif_at" 		: modified_at,
	"modif_for" 	: modified_for,
	"modif_by" 		: oid_usr,
	"modif_val" 	: modified_val,
}

# doc_uses 		= {
# 	"used_by" : used_by,
# 	"used_at"	: used_at,
# }