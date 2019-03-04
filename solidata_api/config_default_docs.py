"""
config_default_docs.py  
- settings for the flask application object
"""

from log_config import log, pformat

### SYSTEM USER
default_system_user_list = [
	{
		"infos" : {
			"name" 		: "Solidata",
			"surname" 	: "Systems",
			"email"		: "solidata.system@solidata.com",
			"pseudo" 	: "system_user",
		},
		"specs" : {
			"doc_type"	: "usr",
		},
		"auth" : {
			"pwd" 		: "UNUSABLE_PASSWORD",
			"conf_usr" 	: True,
			"role"		: "system",
		}
	}
]

### DEFAULT REC
default_recipes_list = [
	{
		"infos" : {
			"title" 		: "geoloc",
			"description" 	: "geolocalize some columns and return new columns in DSI"
		},
		"specs" : {
			"doc_type"		: "rec",
			"is_standard" 	: True
		},
		"data_raw" : {
			"f_code" 			: "geoloc_ban_nominatim",
			"f_object" 		: "geolocalize some dataframes",
			"f_comments" 	: "first recipe to be tested in solidata",
			"field_raw" 	: {	
				"parameters" : [
					"dsi_to_geoloc", 		### dsi list to geoloc
					"new_dmfs_list", 		### dmf to add to dmt and dsis
					"dmf_list_to_geocode",	### 
					# "prj_list_to_geocode",
					"address_complement",
					"timeout",
					"delay",
				],
			},
		},
		"mapping" : {
			"map_func" : {
				"function_class" 	: "geoloc_prj",
				"function_runner" 	: "run_geoloc",
				"default_values" 	: {
					"timeout" 	: 20,
					"delay"		: 1
				}
			}

		}

	}
]

### DEFAULT TAGs
default_tag_list = [

	{
		"infos" : {
			"title" 		: "geoloc",
			"description" 	: ""
		},
		"specs" : {
			"doc_type"		: "tag",
			"is_standard" 	: True
		}

	},
	{
		"infos" : {
			"title" 		: "personal data",
			"description" 	: ""
		},
		"specs" : {
			"doc_type"		: "tag",
			"is_standard" 	: True
		}
	},
	{
		"infos" : {
			"title" 		: "government",
			"description" 	: ""
		},
		"specs" : {
			"doc_type"		: "tag",
			"is_standard" 	: True
		}
	},
	{
		"infos" : {
			"title" 		: "civic data",
			"description" 	: ""
		},
		"specs" : {
			"doc_type"		: "tag",
			"is_standard" 	: True
		}
	},
	{
		"infos" : {
			"title" 		: "climate change",
			"description" 	: ""
		},
		"specs" : {
			"doc_type"		: "tag",
			"is_standard" 	: True
		}
	},
]

### DEFAULT DMFs
default_dmf_list = [

	# SYSTEM RELATED
	{
		"infos" : {
			"title" 		: "solidata_id",
			"description" : "a data's ID in Solidata"
		},
		"specs" : {
			"doc_type"		: "dmf",
			"is_standard" 	: True
		},
		"data_raw" : {
			"f_code" 		: "SOLIDATA_ID",
			"f_object" 	: "",
			"f_type" 		: "id",
			"f_comments" 	: "",
			"f_is_required" : False,
		}
	},
	{
		"infos" : {
			"title" 		: "sd_id",
			"description" : "a data's ID in Solidata"
		},
		"specs" : {
			"doc_type"		: "dmf",
			"is_standard" 	: True
		},
		"data_raw" : {
			"f_code" 		: "SD_ID",
			"f_object" 	: "",
			"f_type" 		: "id",
			"f_comments" 	: "",
			"f_is_required" : False,
		}
	},
	# USER RELATED
	{
		"infos" : {
			"title" 		: "email",
			"description" 	: "a person's email"
		},
		"specs" : {
			"doc_type"		: "dmf",
			"is_standard" 	: True
		},
		"data_raw" : {
			"f_code" 		: "EMAIL",
			"f_object" 	: "",
			"f_type" 		: "email",
			"f_comments" 	: "",
			"f_is_required" : False,
		}
	},

	# GEOLOC RELATED
	{
		"infos" : {
			"title" 		: "address",
			"description" : "Location’s address."
		},
		"specs" : {
			"doc_type"		: "dmf",
			"is_standard" : True
		},
		"data_raw" : {
			"f_code" 		: "ADDRESS",
			"f_object" 	: "",
			"f_type" 		: "geoloc",
			"f_comments" : "",
			"f_is_required" : False,
		}
	},
	{
		"infos" : {
			"title" 		: "latitude",
			"description" 	: "Location’s latitude."
		},
		"specs" : {
			"doc_type"		: "dmf",
			"is_standard" 	: True
		},
		"data_raw" : {
			"f_code" 		: "LATITUDE",
			"f_object" 		: "",
			"f_type" 		: "geoloc",
			"f_comments" 	: "",
			"f_is_required" : False,
		}
	},
	{
		"infos" : {
			"title" 		: "longitude",
			"description" 	: "Location’s longitude."
		},
		"specs" : {
			"doc_type"		: "dmf",
			"is_standard" 	: True
		},
		"data_raw" : {
			"f_code" 		: "LONGITUDE",
			"f_object" 		: "",
			"f_type" 		: "geoloc",
			"f_comments" 	: "",
			"f_is_required" : False,
		}
	},
	{
		"infos" : {
			"title" 		: "lat",
			"description" 	: "Location’s latitude."
		},
		"specs" : {
			"doc_type"		: "dmf",
			"is_standard" 	: True
		},
		"data_raw" : {
			"f_code" 		: "LAT",
			"f_object" 		: "",
			"f_type" 		: "geoloc",
			"f_comments" 	: "",
			"f_is_required" : False,
		}
	},
	{
		"infos" : {
			"title" 		: "lon",
			"description" 	: "Location’s longitude."
		},
		"specs" : {
			"doc_type"		: "dmf",
			"is_standard" 	: True
		},
		"data_raw" : {
			"f_code" 		: "LON",
			"f_object" 		: "",
			"f_type" 		: "geoloc",
			"f_comments" 	: "",
			"f_is_required" : False,
		}
	},
	{
		"infos" : {
			"title" 		: "point",
			"description" 	: "Location’s point."
		},
		"specs" : {
			"doc_type"		: "dmf",
			"is_standard" 	: True
		},
		"data_raw" : {
			"f_code" 		: "POINT",
			"f_object" 		: "",
			"f_type" 		: "geoloc",
			"f_comments" 	: "",
			"f_is_required" : False,
		}
	},
	{
		"infos" : {
			"title" 		: "raw",
			"description" 	: "Location’s raw data."
		},
		"specs" : {
			"doc_type"		: "dmf",
			"is_standard" 	: True
		},
		"data_raw" : {
			"f_code" 		: "RAW_LOC",
			"f_object" 		: "",
			"f_type" 		: "geoloc",
			"f_comments" 	: "",
			"f_is_required" : False,
		}
	},
	{
		"infos" : {
			"title" 			: "city",
			"description" : "City’s data."
		},
		"specs" : {
			"doc_type"		: "dmf",
			"is_standard" 	: True
		},
		"data_raw" : {
			"f_code" 		: "CITY_LOC",
			"f_object" 		: "",
			"f_type" 		: "geoloc",
			"f_comments" 	: "",
			"f_is_required" : False,
		}
	},
	# CATEGORIES RELATED
	{
		"infos" : {
			"title" 			: "tag",
			"description" : "Tags about a data."
		},
		"specs" : {
			"doc_type"		: "dmf",
			"is_standard" 	: True
		},
		"data_raw" : {
			"f_code" 		: "TAG",
			"f_object" 		: "",
			"f_type" 		: "tag",
			"f_comments" 	: "",
			"f_is_required" : False,
		}
	},
	{
		"infos" : {
			"title" 			: "category",
			"description" : "Category related a data."
		},
		"specs" : {
			"doc_type"		: "dmf",
			"is_standard" 	: True
		},
		"data_raw" : {
			"f_code" 		: "CATEGORY",
			"f_object" 		: "",
			"f_type" 		: "category",
			"f_comments" 	: "",
			"f_is_required" : False,
		}
	},
	# MEDIA RELATED
	{
		"infos" : {
			"title" 		: "website",
			"description" : "Website related to a data."
		},
		"specs" : {
			"doc_type"		: "dmf",
			"is_standard" 	: True
		},
		"data_raw" : {
			"f_code" 		: "WEBSITE",
			"f_object" 		: "",
			"f_type" 		: "hyperlink",
			"f_comments" 	: "",
			"f_is_required" : False,
		}
	},
	{
		"infos" : {
			"title" 		: "email",
			"description" 	: "Email related to a data."
		},
		"specs" : {
			"doc_type"		: "dmf",
			"is_standard" 	: True
		},
		"data_raw" : {
			"f_code" 		: "EMAIL",
			"f_object" 		: "",
			"f_type" 		: "email",
			"f_comments" 	: "",
			"f_is_required" : False,
		}
	},
	{
		"infos" : {
			"title" 		: "image",
			"description" : "Image related to a data."
		},
		"specs" : {
			"doc_type"		: "dmf",
			"is_standard" 	: True
		},
		"data_raw" : {
			"f_code" 		: "IMAGE",
			"f_object" 		: "",
			"f_type" 		: "media_link",
			"f_comments" 	: "",
			"f_is_required" : False,
		}
	},
	{
		"infos" : {
			"title" 		: "video",
			"description" : "Image related to a data."
		},
		"specs" : {
			"doc_type"		: "dmf",
			"is_standard" 	: True
		},
		"data_raw" : {
			"f_code" 		: "VIDEO",
			"f_object" 		: "",
			"f_type" 		: "media_link",
			"f_comments" 	: "",
			"f_is_required" : False,
		}
	},
	# PERSONNAL INFOS
	{
		"infos" : {
			"title" 		: "name",
			"description" 	: "Person's name."
		},
		"specs" : {
			"doc_type"		: "dmf",
			"is_standard" 	: True
		},
		"data_raw" : {
			"f_code" 		: "NAME",
			"f_object" 		: "",
			"f_type" 		: "text",
			"f_comments" 	: "",
			"f_is_required" : False,
		}
	},

	{
		"infos" : {
			"title" 		: "surname",
			"description" 	: "Person's surname"
		},
		"specs" : {
			"doc_type"		: "dmf",
			"is_standard" 	: True
		},
		"data_raw" : {
			"f_code" 		: "SURNAME",
			"f_object" 		: "",
			"f_type" 		: "text",
			"f_comments" 	: "",
			"f_is_required" : False,
		}
	},
]