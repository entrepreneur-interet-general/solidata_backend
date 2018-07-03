# -*- encoding: utf-8 -*-


### TO DO : MULTI LANGUAGE FOR ALL CHOICES 

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### CHOICES ONLY FOR ADMIN
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

user_roles = [
	"admin", 
	"staff", 
	"collective", 
	"registred", 
	"guest",
	"anonymous"
]

bad_passwords = [ 
	'test', 
	'password', 
	'12345' 
]

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### CHOICES FOR USERS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###


user_fields_client_can_update = {
	"infos" 				: ["name", "surname", "email"], 
	"auth" 					: ["pwd"],
	"preferences" 	: ["language"],
	"datasets" 			: ["projects", "datamodels", "datasets_inputs", "datasets_outputs", "recipes"],
	"profile" 			: ["profiles"],
	"professional" 	: ["structures", "structures_profiles"]
}

user_profiles = [
	"helper",
	"analyst",
	"financer",
	"observer",
	"project_holder",
	"citizen",
	"other"
]

user_structure = [
	"association",
	"citizen_collective",
	"public_collective",
	"cooperative",
	"entreprise_more_50",
	"entreprise_50",
	"entreprise_10",
	"independant",
	"finance",
	"foundation",
	"mutual",
	"public_state",
	"public_other", 
	"other"
]
