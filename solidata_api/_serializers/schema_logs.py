# -*- encoding: utf-8 -*-

"""
schema_logs.py  
- provides the model for LOGS definition in DB and Flask-Restplus
"""

from log_config import log, pformat

from flask_restplus import fields #, marshal

log.debug("... loading schema_logs.py ...")

from .schema_generic import *


### counts infos
count 					= fields.Integer( 
										description	= "count", 
										# attribute		= "count" ,
										required		= False, 
										default			= 0,
									)

### datetime infos
created_at 			= fields.DateTime( 
										description	= "date of creation", 
										attribute		= "created_at" ,
										required		= True, 
									)
modified_at			= fields.DateTime( 
										description	= "date of a modification", 
										attribute		= "modif_at" ,
										required		= True, 
									)
used_at 			= fields.DateTime( 
										description	= "date of use", 
										attribute		= "used_at" ,
										required		= True, 
									)
modified_for		= fields.String(	 
										description	= "action corresponding to a modification",
										attribute		= "modif_for" ,
										required		= True, 
									)
# modified_by			= fields.String(	 
# 										description	= "user doing the modification",
# 										attribute		= "modif_by" ,
# 										required		= False, 
# 									)
modified_val			= fields.String(	 
										description	= "value of the modification",
										attribute		= "modif_val" ,
										required		= False, 
									)
added_at 			= fields.DateTime( 
										description	= "date of addition", 
										attribute		= "added_at" ,
										required		= True, 
									)
# added_by		  = fields.String(	 
# 										description	= "added by an user",
# 										attribute		= "added_by" ,
# 										required		= True, 
# 									)

### FOR GENERIC MODELS
# modification = {
# 	"modif_at" 		: modified_at,
# 	"modif_for" 	: modified_for
# }

# modification_by = {
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