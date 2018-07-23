# -*- encoding: utf-8 -*-

"""
schema_generic.py  
- provides the model for GENERIC DATA definition in DB and Flask-Restplus
"""

from log_config import log, pformat

from flask_restplus import fields #, marshal


log.debug("... loading schema_generic.py ...")

from solidata_api._choices import *

### generic info for updates
generic_data 		= fields.String(
										description	= "data about a document",
										attribute		= "data",
										example			= "new data",
										default			= 'a new data',
										required		= True,
									)
url_link 				= fields.String(
										description	= "generic url_link",
										attribute		= "url_link",
										example			= "my-url-link",
										default			= '',
										required		= False,
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
open_level 				= fields.String(
										description	= "open level of the document",
										attribute		= "open_level",
										example			= "commons",
										default			= 'open_data',
										enum				= open_level_choices,
										required		= False,
									)
src_link 				= fields.String(
										description	= "source link of the document",
										attribute		= "src_link",
										example			= "my-link-to-my-source",
										default			= '',
										required		= False,
									)
src_type 				= fields.String(
										description	= "source type of the document",
										attribute		= "src_type",
										example			= "csv",
										default			= "",
										required		= False,
									)
tag 						= fields.String(
										description	= "tag about the document",
										attribute		= "tag",
										example			= "my-tag",
										# default			= '',
										required		= False,
									)
tags_list 			= fields.List(
										tag, 
										description = "list of tags about the document",
										attribute		= "tags_list", 
										default			= [] 
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
created_by 			= fields.String(
										description = "oid of an user",
										attribute		= "created_by",
										example			= "5b461ed90a82867e7b114f44",
										required		= True,
									)
used_by 				= fields.String(
										description = "oid of a document",
										attribute		= "used_by",
										example			= "5b461ed90a82867e7b114f44",
										required		= True,
									)
used_as 				= fields.String(
										description = "category of use",
										attribute		= "used_as",
										enumerate   = doc_type_list,
										example			= "prj",
										required		= True,
									)
modified_by 		= fields.String(
										description = "oid of an user",
										attribute		= "modified_by",
										example			= "5b461ed90a82867e7b114f44",
										required		= True,
									)
added_by 				= fields.String(
										description = "oid of an user",
										attribute		= "added_by",
										example			= "5b461ed90a82867e7b114f44",
										required		= True,
									)

oid_prj 				= fields.String(
										description = "oid of a project",
										attribute		= "oid_prj",
										example			= "5b461ed90a82867e7b114f44",
										required		= True,
									)
oid_dmf 				= fields.String(
										description = "oid of a datamodel field",
										attribute		= "oid_dmf",
										example			= "5b461ed90a82867e7b114f44",
										required		= True,
									)
oid_dmt 				= fields.String(
										description = "oid of a datamodel template",
										attribute		= "oid_dmt",
										example			= "5b461ed90a82867e7b114f44",
										required		= True,
									)
oid_dsi 				= fields.String(
										description = "oid of a dataset input",
										attribute		= "oid_dsi",
										example			= "5b461ed90a82867e7b114f44",
										required		= True,
									)
oid_dsr 				= fields.String(
										description = "oid of a dataset raw",
										attribute		= "oid_dsr",
										example			= "5b461ed90a82867e7b114f44",
										required		= True,
									)
oid_dso 				= fields.String(
										description = "oid of a dataset output",
										attribute		= "oid_dso",
										example			= "5b461ed90a82867e7b114f44",
										required		= True,
									)
oid_rec 				= fields.String(
										description = "oid of a recipe",
										attribute		= "oid_rec",
										example			= "5b461ed90a82867e7b114f44",
										required		= True,
									)
oid_tag 				= fields.String(
										description = "oid of a tag",
										attribute		= "oid_tag",
										example			= "5b461ed90a82867e7b114f44",
										required		= True,
									)
oid_fld 				= fields.String(
										description = "oid of a field",
										attribute		= "oid_fld",
										example			= "5b461ed90a82867e7b114f44",
										required		= True,
									)
oid_func 				= fields.String(
										description = "oid of a function",
										attribute		= "oid_func",
										example			= "5b461ed90a82867e7b114f44",
										required		= True,
									)

### store a correspondance dict of oids...
oid_dict = {
	"oid" : { "field" : oid , 		"fullname" : "oid" } ,
	"usr" : { "field" : oid_usr ,	"fullname" : "user" } ,
	"prj" : { "field" : oid_prj , "fullname" : "project" } ,
	"dmt" : { "field" : oid_dmt , "fullname" : "datamodel_template" } ,
	"dmf" : { "field" : oid_dmf , "fullname" : "datamodel_field" } ,
	"dsi" : { "field" : oid_dsi , "fullname" : "dataset_input" } ,
	"dsr" : { "field" : oid_dsr , "fullname" : "dataset_raw" } ,
	"rec" : { "field" : oid_rec , "fullname" : "recipe" } ,
	"dso" : { "field" : oid_dso , "fullname" : "dataset_output" } ,
	"fld" : { "field" : oid_fld , "fullname" : "field" } ,
	"tag" : { "field" : oid_tag , "fullname" : "tag" } ,
}


### for mappings
col_index 				= fields.String(
										description = "index of a column within a dataset input",
										attribute		= "col_index",
										example			= "my_col_index",
										required		= True,
									)

mapping_oid_dict = {

	"dsi_to_dmf"	: {
		### src dsi
		"oid_dsi" 	: oid_dsi,
		"col_index"	: col_index,
		### target dmf
		"oid_dmt" 	: oid_dmt,
		"oid_dmf" 	: oid_dmf,
	} , 

	"rec_to_dmf"	: {
		### src rec
		"oid_rec" 	: oid_rec,
		"oid_func" 	: oid_func,
		### target dmf
		"oid_dmt" 	: oid_dmt,
		"oid_dmf" 	: oid_dmf,
		### rec_params : {}
	} , 
	"rec_to_func"	: {
		"oid_func" 	: oid_func,
		### rec_params : {}
	} 
}

### edit auth for a document
guests_can_see		= fields.Boolean(
										description	= "guests can see the document ?",
										attribute		= "guests_can_see",
										example			= True,
										required		= True,
										default			= True,
									)
guests_can_edit		= fields.Boolean(
										description	= "guests can edit the document ?",
										attribute		= "guests_can_edit",
										example			= False,
										required		= True,
										default			= False,
									)
									
public_auth 			= {
	"guests_can_see" 	: guests_can_see,
	"guests_can_edit"	: guests_can_edit
}


### data_raw for dsi - dso - dmf
f_cell = fields.String(
										description = "content of a cell",
										attribute		= "f_cell",
										example			= "data",
										required		= False,
									)

### log basics
is_running		= fields.Boolean(
										description	= "is the project currently running ?",
										attribute		= "is_running",
										example			= False,
										required		= True,
										default			= False,
									)

is_loaded					= fields.Boolean(
										description	= "is the project currently loaded ?",
										attribute		= "is_loaded",
										example			= False,
										required		= False,
										default			= False,
									)

is_linked_to_src	= fields.Boolean(
										description	= "is the project currently linked to the source ?",
										attribute		= "is_linked_to_src",
										example			= False,
										required		= False,
										default			= False,
									)



doc_type 			= fields.String(
										description	= "category of a document",
										attribute		= "doc_type",
										enum 				= doc_type_list,
										# example			= "usr",
										# default			= 'usr',
										required		= True,
									)

### preformat some generic fields
doc_basics 	= {
	"title" 				: title,
	"licence"				: licence,
	"description"		: descript,
}
