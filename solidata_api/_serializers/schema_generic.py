# -*- encoding: utf-8 -*-

"""
schema_generic.py  
- provides the model for GENERIC DATA definition in DB and Flask-Restplus
"""

from log_config import log, pformat

from flask_restplus import fields #, marshal


log.debug("... loading schema_generic.py ...")

from solidata_api._choices import *


### totaly raw field
class RawData(fields.Raw):
	def format(self, value):
		return value


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### generic info for updates
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
generic_data 		= fields.String(
										description		= "data about a document",
										attribute		= "data",
										example			= "new data",
										default			= 'a new data',
										required		= True,
									)
url_link			= fields.String(
										description		= "generic url_link",
										attribute		= "url_link",
										example			= "my-url-link",
										default			= '',
										required		= False,
									)

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### for document updates
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
field_raw 			= fields.Raw(
										description		= "raw data about a document",
										attribute		= "field_raw",
										example			= "raw data",
										default			= 'a new raw data',
										required		= True,
									)
field_value 		= fields.Raw(
										description		= "data about a document",
										attribute		= "data",
										example			= "new data",
										default			= 'a new data',
										required		= True,
									)
field_to_update		= fields.String(
										description		= "data about a document",
										attribute		= "field_to_update",
										example			= "infos.title",
										default			= 'a new data',
										required		= True,
									)
add_to_list			= fields.String(
										description		= "data about a document",
										attribute		= "add_to_list",
										example			= False,
										enum			= update_types_list,
										default			= False,
									)

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### basic informations about a document : project / licence / oid ...
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
title				= fields.String(
										description		= "title of the document",
										attribute		= "title",
										example			= "my-title",
										default			= 'title',
										required		= True,
									)
descript 			= fields.String(
										description		= "description of the document",
										attribute		= "description",
										example			= "my-description",
										default			= 'description',
										required		= False,
									)
licence 			= fields.String(
										description		= "licence of the document",
										attribute		= "licence",
										example			= "MIT",
										default			= 'MIT',
										enum			= licences_options,
										required		= True,
									)
open_level 			= fields.String(
										description		= "open level of the document",
										attribute		= "open_level",
										example			= "commons",
										default			= 'open_data',
										enum			= open_level_choices,
										required		= False,
									)
open_level_edit 	= fields.String(
										description		= "open level of the document for edit",
										attribute		= "open_level_edit",
										example			= "collective",
										default			= 'collective',
										enum			= open_level_choices,
										required		= True,
									)
open_level_show 	= fields.String(
										description		= "open level of the document for show",
										attribute		= "open_level_show",
										example			= "commons",
										default			= 'open_data',
										enum			= open_level_choices,
										required		= True,
									)
is_standard			= fields.Boolean(
										description		= "is it standard document ?",
										attribute		= "is_standard",
										example			= True,
										required		= False,
										default			= False,
									)

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### multilanguage
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
locale 				= fields.String(
										description		= "locale language code",
										attribute		= "locale",
										example			= "fr",
										default			= 'en',
										required		= False,
									)
field_to_translate 	= fields.String(
										description		= "code of the field to translatee",
										attribute		= "field_to_translate",
										example			= "infos.title",
										default			= 'infos.title',
										required		= False,
									)
text_translated		= fields.String(
										description		= "text to translate",
										attribute		= "text_translated",
										example			= "my-translation",
										default			= '',
										required		= False,
									)

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### sources DSI
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
src_link 			= fields.String(
										description		= "source link of the document",
										attribute		= "src_link",
										example			= "my-link-to-my-source",
										default			= '',
										required		= False,
									)
src_type 			= fields.String(
										description		= "source type of the document",
										attribute		= "src_type",
										example			= "csv",
										default			= "",
										required		= False,
									)
src_parser 			= fields.String(
										description		= "parser for an API response",
										attribute		= "src_parser",
										example			= "/example/of/path",
										default			= "/",
										required		= False,
									)
src_sep 			= fields.String(
										description		= "separator for a CSV file",
										attribute		= "src_sep",
										example			= ",",
										default			= ",",
										enum			= authorized_separators,
										required		= False,
									)

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### tags
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
tag 				= fields.String(
										description		= "tag about the document",
										attribute		= "tag",
										example			= "my-tag",
										# default			= '',
										required		= False,
									)
tags_list 			= fields.List(
										tag, 
										description		= "list of tags about the document",
										attribute		= "tags_list", 
										default			= [] 
									)

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### object ids
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

### custom field for objectId values
class IdField(fields.Raw):
	def format(self, value):
		return str(value)

oid_field			= IdField(
										description		= "data about a document",
										attribute		= "_id",
										example			= "ObjectId('5b841ac70a82863ff21fd4d7')",
									)
oid 				= IdField(
# oid 				= fields.String(
										description 	= "oid of a document",
										attribute		= "oid",
										example			= "ObjectId('5b841ac70a82863ff21fd4d7')",
										required		= True,
									)
doc_id 				= fields.String(
										description 	= "oid of a document as string",
										attribute		= "doc_id",
										example			= "5b841ac70a82863ff21fd4d7",
										required		= True,
									)
oid_usr 			= IdField(
# oid_usr 			= fields.String(
										description 	= "oid of an user",
										attribute		= "oid_usr",
										example			= "ObjectId('5b841ac70a82863ff21fd4d7')",
										required		= True,
									)
created_by 			= IdField(
# created_by 			= fields.String(
										description 	= "oid of an user",
										attribute		= "created_by",
										example			= "ObjectId('5b841ac70a82863ff21fd4d7')",
										required		= True,
									)
used_by 			= IdField(
# used_by 			= fields.String(
										description 	= "oid of a document",
										attribute		= "used_by",
										example			= "ObjectId('5b841ac70a82863ff21fd4d7')",
										required		= True,
									)
modified_by 		= IdField(
# modified_by 		= fields.String(
										description 	= "oid of an user",
										attribute		= "modified_by",
										example			= "ObjectId('5b841ac70a82863ff21fd4d7')",
										required		= True,
									)
added_by 			= IdField(
# added_by 			= fields.String(
										description 	= "oid of an user",
										attribute		= "added_by",
										example			= "ObjectId('5b841ac70a82863ff21fd4d7')",
										required		= True,
									)

used_as 			= fields.String(
										description 	= "category of use",
										attribute		= "used_as",
										enumerate   	= doc_type_list,
										example			= "prj",
										required		= True,
									)

oid_prj 			= IdField(
# oid_prj 			= fields.String(
										description 	= "oid of a project",
										attribute		= "oid_prj",
										example			= "ObjectId('5b841ac70a82863ff21fd4d7')",
										required		= True,
									)
oid_dmf 			= IdField(
# oid_dmf 			= fields.String(
										description 	= "oid of a datamodel field",
										attribute		= "oid_dmf",
										example			= "ObjectId('5b841ac70a82863ff21fd4d7')",
										required		= True,
									)
oid_dmt 			= IdField(
# oid_dmt 			= fields.String(
										description 	= "oid of a datamodel template",
										attribute		= "oid_dmt",
										example			= "ObjectId('5b841ac70a82863ff21fd4d7')",
										required		= True,
									)
oid_dsi 			= IdField(
# oid_dsi 			= fields.String(
										description 	= "oid of a dataset input",
										attribute		= "oid_dsi",
										example			= "ObjectId('5b841ac70a82863ff21fd4d7')",
										required		= True,
									)
oid_dsr 			= IdField(
# oid_dsr 			= fields.String(
										description 	= "oid of a dataset raw",
										attribute		= "oid_dsr",
										example			= "ObjectId('5b841ac70a82863ff21fd4d7')",
										required		= True,
									)
oid_dso 			= IdField(
# oid_dso 			= fields.String(
										description 	= "oid of a dataset output",
										attribute		= "oid_dso",
										example			= "ObjectId('5b841ac70a82863ff21fd4d7')",
										required		= True,
									)
oid_rec 			= IdField(
# oid_rec 			= fields.String(
										description 	= "oid of a recipe",
										attribute		= "oid_rec",
										example			= "ObjectId('5b841ac70a82863ff21fd4d7')",
										required		= True,
									)
oid_tag 			= IdField(
# oid_tag 			= fields.String(
										description 	= "oid of a tag",
										attribute		= "oid_tag",
										example			= "ObjectId('5b841ac70a82863ff21fd4d7')",
										required		= True,
									)
oid_fld 			= IdField(
# oid_fld 			= fields.String(
										description 	= "oid of a field",
										attribute		= "oid_fld",
										example			= "ObjectId('5b841ac70a82863ff21fd4d7')",
										required		= True,
									)
oid_func 			= IdField(
# oid_func 			= fields.String(
										description 	= "oid of a function",
										attribute		= "oid_func",
										example			= "ObjectId('5b841ac70a82863ff21fd4d7')",
										required		= True,
									)

### store a correspondance dict of oids...
oid_dict = {
	"oid"	: { "field" : oid , 	"fullname" : "oid" } ,
	"usr" 	: { "field" : oid_usr , "fullname" : "user" } ,
	"prj"	: { "field" : oid_prj , "fullname" : "project" } ,
	"dmt" 	: { "field" : oid_dmt , "fullname" : "datamodel_template" } ,
	"dmf"	: { "field" : oid_dmf , "fullname" : "datamodel_field" } ,
	"dsi" 	: { "field" : oid_dsi , "fullname" : "dataset_input" } ,
	"dsr" 	: { "field" : oid_dsr , "fullname" : "dataset_raw" } ,
	"rec" 	: { "field" : oid_rec , "fullname" : "recipe" } ,
	"func" 	: { "field" : oid_func ,"fullname" : "function" } ,
	"dso" 	: { "field" : oid_dso , "fullname" : "dataset_output" } ,
	"fld"	: { "field" : oid_fld , "fullname" : "field" } ,
	"tag" 	: { "field" : oid_tag , "fullname" : "tag" } ,
}





### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### for mappings
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
dsi_header 			= fields.String(
										description 	= "index of a column within a dataset input",
										attribute		= "dsi_header",
										example			= "my_dsi_header",
										required		= False,
									)

is_mapping		= fields.Boolean(
										description		= "is it an update in mapping field ?",
										attribute		= "is_mapping",
										example			= True,
										required		= False,
										default			= False,
									)
del_mapping		= fields.Boolean(
										description		= "is it to delete an entry from mapping ?",
										attribute		= "del_mapping",
										example			= True,
										required		= False,
										default			= False,
									)

mapping_field		= fields.String(
										description		= "field to map",
										attribute		= "mapping_field",
										example			= False,
										enum			= mapping_fields,
										default			= False,
									)
id_dmt 				= fields.String(
										description 	= "oid of a document dmt as string",
										attribute		= "id_dmt",
										example			= "5b841ac70a82863ff21fd4d7",
										required		= False,
									)
id_dmf 				= fields.String(
										description 	= "oid of a document dmf as string",
										attribute		= "id_dmf",
										example			= "5b841ac70a82863ff21fd4d7",
										required		= False,
									)
id_dsi 				= fields.String(
										description 	= "oid of a document dsi as string",
										attribute		= "id_dsi",
										example			= "5b841ac70a82863ff21fd4d7",
										required		= False,
									)
id_rec 				= fields.String(
										description 	= "oid of a document rec as string",
										attribute		= "id_rec",
										example			= "5b841ac70a82863ff21fd4d7",
										required		= False,
									)
id_func 				= fields.String(
										description 	= "oid of a document func as string",
										attribute		= "id_func",
										example			= "5b841ac70a82863ff21fd4d7",
										required		= False,
									)

update_mapping 		= {
	"is_mapping"		: is_mapping,
	"del_mapping"		: del_mapping,
	"field_to_update"	: field_to_update,
	# "mapping_field"		: mapping_field,
	"id_dmt" 			: id_dmt,
	"id_dmf" 			: id_dmf,
	"id_dsi" 			: id_dsi,
	"id_rec" 			: id_rec,
	"id_func" 			: id_func,
	"open_level_show" 	: open_level_show,
	"dsi_header"		: dsi_header,

}

mapping_oid_dict 	= {

	"dmf_to_open_level" : {
		### target dmf
		"oid_dmf" 			: oid_dmf,
		### target open_level
		"open_level_show" 	: open_level_show,
	},
	"dsi_to_dmf"	: {
		### src dsi
		"oid_dsi" 		: oid_dsi,
		"dsi_header"	: dsi_header,
		### target dmf
		"oid_dmf" 	: oid_dmf,
	} , 
	"dmf_to_rec"	: {
		### src rec
		"oid_rec" 	: oid_rec,
		### target dmf
		"oid_dmf" 	: oid_dmf,
		### rec_params : {}
		# TO DO 
	} , 
	"rec_to_func"	: {
		### rec_params : {}
		"oid_func" 	: oid_func,
	} ,

}

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### edit auth for a document
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
guests_can_see		= fields.Boolean(
										description		= "can guests see the document ?",
										attribute		= "guests_can_see",
										example			= True,
										required		= True,
										default			= True,
									)
guests_can_edit		= fields.Boolean(
										description		= "can guests edit the document ?",
										attribute		= "guests_can_edit",
										example			= False,
										required		= True,
										default			= False,
									)
edit_auth			= fields.String(
										description 	= "edit auth of an user",
										enum			= user_edit_auth,
										example			= "owner",
										required		= False,
										attribute		= "edit_auth", 
										default			= "editor" 
									)
									
# public_auth 		= {
# 	"open_level"		: open_level,
# 	"guests_can_see" 	: guests_can_see,
# 	"guests_can_edit"	: guests_can_edit
# }
public_auth 		= {
	"open_level_edit"	: open_level_edit,
	"open_level_show" 	: open_level_show,
}

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### data_raw for dsi - dso - dmf - tag 
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
f_cell 				= fields.String(
										description 	= "content of a field",
										attribute		= "f_cell",
										example			= "data",
										required		= False,
									)
f_code 				= fields.String(
										description 	= "code of the field",
										attribute		= "f_code",
										example			= "data code",
										required		= False,
									)
f_object 			= fields.String(
										description 	= "object of the field",
										attribute		= "f_object",
										example			= "data object",
										required		= False,
									)
f_type 				= fields.String(
										description 	= "type of the field",
										attribute		= "f_type",
										example			= "data type",
										required		= False,
									)
f_comments 			= fields.String(
										description 	= "comments about the field",
										attribute		= "f_comments",
										example			= "data comments",
										required		= False,
									)
f_is_required		= fields.Boolean(
										description		= "is the field required ?",
										attribute		= "f_is_required",
										example			= False,
										required		= False,
										default			= False,
									)

f_coll_header_val		= fields.String(
										description		= "columns headers value",
										attribute		= "f_coll_header_val",
									)
f_coll_header_text		= fields.String(
										description		= "columns headers text",
										attribute		= "f_coll_header_text",
									)
# f_coll_headers		= fields.List(
# 										f_coll_header,
# 										example			= ["my_header"],
# 										attribute		= "f_coll_headers",	
# 										default			= []
# 									)
f_data 					= fields.Raw(
										description		= "raw data about a document",
										attribute		= "f_data",
										example			= "raw data",
										default			= 'a new raw data',
										required		= True,
									)

f_basics_tag 		= {
	"f_code" 		: f_code,
	"f_object" 		: f_object,
	"f_comments" 	: f_comments,
}
f_basics_dmf 		= {
	"f_code" 		: f_code,
	"f_object" 		: f_object,
	"f_type" 		: f_type,
	"f_comments" 	: f_comments,
	"f_is_required" : f_is_required,
}
f_headers_ds 		= {
	"f_coll_header_val"		: f_coll_header_val,
	"f_coll_header_text"	: f_coll_header_text,
}
f_headers_dso 		= {
	"f_coll_header_val"		: f_coll_header_val,
	"f_coll_header_text"	: f_coll_header_text,
	"open_level_show" 		: open_level_show,
	"oid_dmf" 				: oid_dmf,
}

f_basics_rec 		= {
	"f_code" 		: f_code,
	"f_object" 		: f_object,
	"f_comments" 	: f_comments,
	"field_raw" 	: field_raw,
}

# f_basics_dsi_dsr_dso 		= {
# 	"f_data" 		: f_code,
# 	"f_col_headers" : f_code,
# }
# f_basics_dsr 		= {
# 	"f_data" 		: f_code,
# 	"f_col_headers" : f_code,
# }
# f_basics_dso 		= {
# 	"f_data" 		: f_code,
# 	"f_col_headers" : f_code,
# }

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### log basics
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
is_running			= fields.Boolean(
										description		= "is the project currently running ?",
										attribute		= "is_running",
										example			= False,
										required		= True,
										default			= False,
									)

is_loaded			= fields.Boolean(
										description		= "is the project currently loaded ?",
										attribute		= "is_loaded",
										example			= False,
										required		= False,
										default			= False,
									)

is_linked_to_src	= fields.Boolean(
										description		= "is the project currently linked to the source ?",
										attribute		= "is_linked_to_src",
										example			= False,
										required		= False,
										default			= False,
									)

doc_type 			= fields.String(
										description		= "category of a document",
										attribute		= "doc_type",
										enum			= doc_type_list,
										example			= "usr",
										# default		= 'usr',
										required		= True,
									)

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### preformat some generic fields
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
doc_oid 						= {
	"_id" 		: oid_field,
}

doc_basics		 				= {
	"title" 		: title,
	"description"	: descript,
}

doc_basics_licence				= {
	"title" 		: title,
	"licence"		: licence,
	"description"	: descript,
}

# doc_basics_openlevel 			= {
# 	"title" 		: title,
# 	"open_level" 	: open_level,
# 	"description"	: descript,
# }

# doc_basics_licence_openlevel 	= {
# 	"title" 		: title,
# 	"licence"		: licence,
# 	"open_level" 	: open_level,
# 	"description"	: descript,
# }

open_level_edit_show 		= {
	"open_level_edit"	: open_level_edit,
	"open_level_show" 	: open_level_show,
}
open_level_edit_ 			= {
	"open_level_edit"	: open_level_edit,
}



### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### preformat some generic fields
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
update_field		= {
	"edit_auth"			: edit_auth,
	"doc_type"			: doc_type,
	"add_to_list"		: add_to_list,
	
	"field_to_update"	: field_to_update,
	"field_value" 		: field_value,
}
