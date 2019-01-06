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
			"f_code" 		: "geoloc_df",
			"f_object" 		: "geolocalize some dataframes",
			"f_comments" 	: "first recipe to be tested in solidata",
			"field_raw" 	: {	
				"params" : [
					"dmf_list_to_geocode",
					"dsi_list_to_geocode",
					"prj_list_to_geocode",
					"address_complement",
					"timeout",
					"delay",
				],
			},

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

	# GEOLOC RELATED
	{
		"infos" : {
			"title" 		: "address",
			"description" 	: "Location’s address."
		},
		"specs" : {
			"doc_type"		: "dmf",
			"is_standard" 	: True
		},
		"data_raw" : {
			"f_code" 		: "ADDRESS",
			"f_object" 		: "",
			"f_type" 		: "geoloc",
			"f_comments" 	: "",
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
			"f_code" 		: "LAT",
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
			"f_code" 		: "LONG",
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