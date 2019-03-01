# -*- encoding: utf-8 -*-

"""
endpoint_dsi_reload.py  
"""

from solidata_api.api import *

log.debug(">>> api_dataset_inputs ... creating api endpoints for DSI_RELOAD")

from . import api, document_type

### create namespace
ns = Namespace('reload', description='Dsi : reload a new dataset_input')

### import models 
from solidata_api._models.models_dataset_input import * 
from solidata_api._models.models_dataset_raw import * 
model_new_dsi	= NewDsi(ns).model

model_dsi			= Dsi_infos(ns)
model_dsi_in	= model_dsi.mod_complete_in
model_dsi_out	= model_dsi.mod_complete_out
model_dsi_out_min	= model_dsi.mod_minimum

model_dsr			= Dsr_infos(ns)
model_dsr_in	= model_dsr.mod_complete_in
model_dsr_out	= model_dsr.mod_complete_out
model_dsr_out_min	= model_dsr.mod_minimum

# model_dsi_ref		= create_model_dataset(ns, model_name="Dsi_ref", include_fav=True,schema="dsi")






### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 

# cf : https://stackoverflow.com/questions/40547670/python-restplus-api-to-upload-and-dowload-files




@ns.doc(security='apikey')
@ns.route('/<string:doc_id>')
@ns.response(404, 'document not found')
@ns.param('doc_id', 'The document unique identifier')
class DsiReload(Resource):

	@guest_required 
	@ns.expect(file_parser)   ### from "solidata_api._parsers.__init__.file_parser" loaded from "solidata.api.__init__"
	def post(self, doc_id):
		"""
		upload a file or external API value and reload an existing dsi in db
		"""

		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )

		### DEBUG check
		log.debug ("payload : \n{}".format(pformat(ns.payload)))

		df_is_created = False 
		roles_for_complete = ["admin"]

		### TO DO : reuse this function in all endpoints POST / GET / DELETE ...
		payload, is_form, files = return_payload(request, ns.payload)
		log.debug ("payload 	 : \n{}".format(pformat(payload)))


		### check if client is an admin or if is the current user
		### needs decorator @guest_required or @admin_required
		claims 	= get_jwt_claims() 
		log.debug("claims : \n %s", pformat(claims) )
		
		user_role = claims["auth"]["role"]
		user_id = claims["_id"] ### get the oid as str
		if user_role != "anonymous" : 
			user_oid = ObjectId(user_id)
			log.debug("user_oid : %s", user_oid )

		### retrieve DSI from db
		if ObjectId.is_valid(doc_id) : 
			doc_oid	= ObjectId(doc_id)
			document = mongo_datasets_inputs.find_one( {"_id": doc_oid } )
			# log.debug( "document : \n%s", pformat(document) )
		else :
			response_code	= 400
			document			= None

		### sum up all query arguments
		query_resume = {
			"document_type"			: document_type,	
			"doc_id" 						: doc_id,
			"user_id" 					: user_id,
			"user_role"					: user_role,
			"is_member_of_team" : False,
			"is_creator" 				: False,
		}

		if document : 

			### check doc's specs : public_auth, team...
			doc_open_level_edit = document["public_auth"]["open_level_edit"]
			log.debug( "doc_open_level_edit : %s", doc_open_level_edit )

			### get doc's owner infos
			created_by_oid = document["log"]["created_by"]
			log.debug( "created_by_oid : %s", str(created_by_oid) )

			### get doc's team infos
			if "team" in document : 
				team_oids = [ t["oid_usr"] for t in document["team"] ]
				log.debug( "team_oids : \n%s", pformat(team_oids) )

			# flag as member of doc's team
			if user_oid == created_by_oid :
				query_resume["is_creator"] = True

			# flag as member of doc's team
			if user_oid in team_oids :
				query_resume["is_member_of_team"] = True

			if user_role in roles_for_complete or user_oid in team_oids or user_oid == created_by_oid : 

				### marshall existing DSI with dsi complete model
				# dsi_to_reload = marshal( document , model_dsi_in )
				dsi_to_reload = document
				log.debug('dsi_to_reload (START): \n%s', pformat(dsi_to_reload) )  

				### DSR - copy dsr to prepare a dsr_to_reload
				# dsr_to_reload 		= marshal( document , model_dsr_in )
				# dsr_to_reload 		= document
				# log.debug('dsr_to_reload : \n%s', pformat(dsr_to_reload) )  

				### check for files (not an API reference)
				if payload["src_type"] != 'API' :

					log.debug('payload contains a file... ' )  

					### load file from request - data_file
					args 			= file_parser.parse_args()
					uploaded_file 	= args['data_file']  # This is a FileStorage instance
					log.debug("uploaded_file (from args['data_file']) : \n %s", uploaded_file )
					
					### load file from request - form_file
					if not uploaded_file : 
						uploaded_file 	= files['form_file']  # This is a FileStorage instance
						log.debug("uploaded_file (from files) : \n %s", uploaded_file )

					### check extension and mimetype
					if uploaded_file and allowed_file(uploaded_file.filename) : 
						
						### create a secure filename
						filename = secure_filename(uploaded_file.filename)
						log.debug("filename : %s", filename)

						### save data if file is allowed # and not already existing 
						# if existing_dsi is None and allowed_file(filename) : 
						if allowed_file(filename) : 

							### get file extension from file itself
							file_extension = get_file_extension(filename)
							log.debug("file_extension : %s", file_extension)

							### correct file_extension if different
							if file_extension != payload["src_type"] :
								dsi_to_reload["specs"]["src_type"] = file_extension
								# dsr_to_reload["specs"]["src_type"] = file_extension

							### delete scr_parser info
							dsi_to_reload["specs"]["src_parser"] = None
							# dsr_to_reload["specs"]["src_parser"] = None

							### create dataframe by reading file with pandas
							sep = payload['src_sep']
							log.debug("trying to read file / sep : %s", sep)
							df = read_file_with_pd(uploaded_file, file_extension, sep=sep )
							df_is_created = True
							
							### add src_sep info
							dsi_to_reload["specs"]["src_sep"] = payload['src_sep']
							# dsr_to_reload["specs"]["src_sep"] = payload['src_sep']

						### file not permited
						else : 
							log.info("-!- filename not permited...")
							response_code	= 401
							message 			= "your file '{}' format is not permited...".format(filename)
							document_out  = None

					### no file detected
					else : 
						log.info("-!- no file detected ...")
						response_code	= 401
						message 			= " no file detected"
						document_out  = None

				### get data from API 
				# if payload["src_type"] == 'API' : 
				else :

					log.debug('payload contains an API reference... ' )  

					### load url
					url = filename = payload["src_link"]
					log.debug('API / url : {}'.format(url) )  

					### get the data from API
					api_response = requests.get(url)
					log.debug('API / api_response : %s', pformat(api_response))  

					if(api_response.ok):
							
						log.debug('API / api_response.ok : %s', api_response.ok )  
						# api_data = json.loads(api_response.content)
						api_data = api_response.json()
						# log.debug('API / api_data : \n%s', pformat(api_data) )  

						### get to the field containing the records
						api_parser = payload.get("src_parser", "/")
						log.debug('API / api_parser : %s', api_parser )  
						if api_parser != "/" : 
							api_parser = api_parser.split("/")
							for i in api_parser[1:] :
								api_data = api_data[i]
						log.debug('API / api_data[:2] : \n%s', pformat(api_data[:2]) )  

						### create dataframe
						df = read_dict_with_pd(api_data)
						df_is_created = True

						### delete src_sep info
						dsi_to_reload["specs"]["src_sep"] = None
						# dsr_to_reload["specs"]["src_sep"] = None

						### add src_parser info
						dsi_to_reload["specs"]["src_parser"] = api_parser
						# dsr_to_reload["specs"]["src_parser"] = api_parser

					### no data detected | API request failed
					else : 
						log.info("-!- request to API failed ...")
						response_code	= 401
						message = "request to API failed"
						document_out = None

				### manage dataframe, DSI, and DSR
				if df_is_created : 

					### df is created
					log.debug("finish to read file... ")
					print (df.head(5)) 

					### get columns headers and prepare data
					df_headers = df.columns.values.tolist()
					df_headers = [ { 
						"f_coll_header_val" 	: header,
						"f_coll_header_text" 	: header,
					} for header in df_headers ]
					log.debug("df_headers : %s", pformat(df_headers))

					### clean data from nan rows and change Nan to None
					df = df.dropna(how="all")
					df = df.replace({np.nan:None})
					print ("\n", df.head(5)) 

					### get data as records
					# df_col_dict = df.to_dict(orient="list")
					df_col_dict = df.to_dict(orient="records")
					log.debug("df_col_dict (head(3)) : \n %s", pformat(df.head(3).to_dict(orient="records")) )

					### copy records to DSI and DSR : ["data_raw"]["f_data"]
					# dsi_to_reload["data_raw"]["f_data"] = df_col_dict
					dsi_to_reload["data_raw"]["f_col_headers"] = df_headers

					# dsr_to_reload["data_raw"]["f_data"] = df_col_dict
					# dsr_to_reload["data_raw"]["f_col_headers"] = df_headers

					### UPDATE DSI IN DB
					log.info("dsi_to_reload (END): \n%s", pformat(dsi_to_reload))
					mongo_datasets_inputs.replace_one({'_id': doc_oid}, dsi_to_reload)
					log.info("dsi_to_reload is saved in db... ")

					### UPDATE DSR IN DB (FOR FURTHER RESET)
					# mongo_datasets_raws.replace_one({'_id': doc_oid}, dsr_to_reload)
					# log.info("dsr_to_reload is saved in db... ")
					# document_out  = marshal( document , model_dsr_out_min )

					### DSI_DOCS - INSERT MANY
					df_ = df.copy()
					df_["oid_dsi"] = doc_oid
					df_col_dict_ = df_.to_dict(orient="records")
					
					### delete previous documents from mongo_datasets_inputs_docs
					log.info("deleting documents related to dsi in mongo_datasets_inputs_docs ...")
					try :
						mongo_datasets_inputs_docs.delete_many({ 'oid_dsi' : oid_dsi_ })
					except : 
						pass

					### insert many docs in dso_docs for every entry of df_col_dict
					log.info("inserting documents related to dsi in mongo_datasets_inputs_docs ...")
					if len(df_col_dict_) > 0 and len(df_col_dict_) < 2 :
						mongo_datasets_inputs_docs.insert_one( df_col_dict_ )
					else :
						mongo_datasets_inputs_docs.insert_many( df_col_dict_ )


					response_code	= 200
					message				= "your file '{}' has been correctly uploaded...".format(filename)
					document_out  = None

				### no dataframe detected
				else : 

					log.info("-!- dataframe failed to be created ...")

					### delete previously inserted dsr and dsi docs
					# mongo_datasets_inputs.delete_one({"_id" : ObjectId(oid_dsi_) })
					# mongo_datasets_raws.delete_one({"_id" : ObjectId(oid_dsr_) })

					### send message
					response_code	= 401
					message				= "dataframe failed to be created"
					document_out  = None

			### no credentials
			else : 
				### send message
				response_code	= 401
				message				= "dear user, you don't have the credentials to reload this document"
				document_out  = None

		### no document / empty response
		else : 
			response_code	= 404
			message 			= "dear user, there is no document with this oid "
			document_out  = None

		### return response
		log.debug( "message : %s", message )
		log.debug( "query_resume : %s", pformat(query_resume) )
		return {
					"msg" 	: message,
					"data"	: document_out,
					"query"	: query_resume,
				}, response_code