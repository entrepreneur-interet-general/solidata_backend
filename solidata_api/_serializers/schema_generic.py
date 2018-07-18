# -*- encoding: utf-8 -*-

"""
schema_generic.py  
- provides the model for GENERIC DATA definition in DB and Flask-Restplus
"""

from log_config import log, pformat

from flask_restplus import fields #, marshal


log.debug("... loading schema_generic.py ...")

from ._choices_licences import *

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
										example			= "MIT",
										default			= 'MIT',
										enum				= licences_options,
										required		= True,
									)


### object ids
oid 						= fields.String(
										description = "oid of a document",
										attribute		= "oid",
										example			= "5b461ed90a82867e7b114f44",
										required		= True,
									)
oid_usr 				= fields.String(
										description = "oid of an user",
										attribute		= "oid_usr",
										example			= "5b461ed90a82867e7b114f44",
										required		= True,
									)
oid_prj 				= fields.String(
										description = "oid of a project",
										attribute		= "oid_proj",
										example			= "5b461ed90a82867e7b114f44",
										required		= True,
									)
oid_dmf 				= fields.String(
										description = "oid of a datamodel field",
										attribute		= "oid_dm_f",
										example			= "5b461ed90a82867e7b114f44",
										required		= True,
									)
oid_dmt 				= fields.String(
										description = "oid of a datamodel template",
										attribute		= "oid_dm_t",
										example			= "5b461ed90a82867e7b114f44",
										required		= True,
									)
oid_dsi 				= fields.String(
										description = "oid of a dataset input",
										attribute		= "oid_ds_i",
										example			= "5b461ed90a82867e7b114f44",
										required		= True,
									)
oid_dso 				= fields.String(
										description = "oid of a dataset output",
										attribute		= "oid_ds_o",
										example			= "5b461ed90a82867e7b114f44",
										required		= True,
									)
oid_rec 				= fields.String(
										description = "oid of a recipe",
										attribute		= "oid_rec",
										example			= "5b461ed90a82867e7b114f44",
										required		= True,
									)

oid_dict = {
	"oid" : { "field" : oid , 		"fullname" : "oid" } ,
	"usr" : { "field" : oid_usr ,	"fullname" : "user" } ,
	"prj" : { "field" : oid_prj , "fullname" : "project" } ,
	"dmt" : { "field" : oid_dmt , "fullname" : "datamodel_template" } ,
	"dmf" : { "field" : oid_dmf , "fullname" : "datamodel_field" } ,
	"dsi" : { "field" : oid_dsi , "fullname" : "dataset_input" } ,
	"rec" : { "field" : oid_rec , "fullname" : "recipe" } ,
	"dso" : { "field" : oid_dso , "fullname" : "dataset_output" } ,
}

doc_categ_list = [ "usr", "prj", "dmt", "dmf", "dsi", "rec", "dso" ]
doc_categ 			= fields.String(
										description	= "category of a document",
										attribute		= "doc_categ",
										enum 				= doc_categ_list,
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