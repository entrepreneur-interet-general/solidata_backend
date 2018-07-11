# -*- encoding: utf-8 -*-

"""
schema_logs.py  
- provides the model for LOGS definition in DB and Flask-Restplus
"""

from log_config import log, pformat

from flask_restplus import fields #, marshal


log.debug("... loading schema_logs.py ...")


### counts infos
count 					= fields.Integer( 
										description	= "count", 
										attribute		= "count" ,
										required		= False, 
										default			= 0,
									)

### datetime infos
created_at 			= fields.DateTime( 
										description	= "creation date", 
										attribute		= "created_at" ,
										required		= False, 
									)
modified_at			= fields.DateTime( 
										description	= "modification date", 
										attribute		= "modif_at" ,
										required		= False, 
									)
modified_for		= fields.String(	 
										description	= "modification action",
										attribute		= "modif_for" ,
										required		= False, 
									)


### FOR GENERIC MODELS
modification = {
	"modif_at" 		: modified_at,
	"modif_for" 	: modified_for
}
