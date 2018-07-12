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

### basic informations about a document : project / licence / oid ...
title 					= fields.String(
										description	= "title of the document",
										attribute		= "title",
										example			= "my-title",
										default			= 'title',
										required		= True,
									)
descript 					= fields.String(
										description	= "description of the document",
										attribute		= "description",
										example			= "my-description",
										default			= 'description',
										required		= False,
									)
licence 				= fields.String(
										description	= "licence of the document",
										attribute		= "licence",
										example			= "my-licence",
										default			= 'licence',
										required		= True,
									)
oid 						= fields.String(
										description = "oid of a document",
										attribute		= "oid",
										example			= "5b461ed90a82867e7b114f44",
										required		= True,
									)
doc_categ 			= fields.String(
										description	= "category of a document : usr, dm_t, dm_p, dsi, cd, rec ...",
										attribute		= "doc_categ",
										example			= "usr",
										default			= 'usr',
										required		= True,
									)

### preformat some generic fields
doc_basics = {
	"title" 				: title,
	"licence"				: licence,
	"description"		: descript,
}