# -*- encoding: utf-8 -*-

"""
schema_generic.py  
- provides the model for GENERIC DATA definition in DB and Flask-Restplus
"""

from log_config import log, pformat

from flask_restplus import fields #, marshal


log.debug("... loading schema_generic.py ...")


### generic info for updates
generic_data 		= fields.String(
										description	= "data about a document",
										attribute		= "data",
										example			= "example",
										default			= 'a new data',
										required		= True,
									)

### basic informations about a document : project / dataset / ...
title 					= fields.String(
										description	= "title of the document",
										attribute		= "title",
										example			= "my-title",
										default			= 'title',
										required		= True,
									)
oid 						= fields.String(
										description = "oid of a document",
										attribute		= "oid",
										example			= "5b461ed90a82867e7b114f44",
										required		= True,
									)
edit_auth				= fields.String(
										description = "authorization level for edition",
										attribute		= "owner_oid",
										example			= "can_edit",
										required		= True,
										default			= 'title',
									)


