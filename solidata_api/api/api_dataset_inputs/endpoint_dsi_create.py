# -*- encoding: utf-8 -*-

"""
endpoint_dsi_create.py  
"""

from solidata_api.api import *

log.debug(">>> api_dataset_inputs ... creating api endpoints for DSI_CREATE")

from . import api, document_type

### create namespace
ns = Namespace('create', description='Dsi : create a new dataset_input')

### import models 
from solidata_api._models.models_dataset_input import * 
from solidata_api._models.models_dataset_raw import * 
model_new_dsi  	= NewDsi(ns).model

model_dsi		= Dsi_infos(ns)
model_dsi_in	= model_dsi.mod_complete_in
model_dsi_out	= model_dsi.mod_complete_out

model_dsr		= Dsr_infos(ns)
model_dsr_in	= model_dsr.mod_complete_in
model_dsr_out	= model_dsr.mod_complete_out

# model_dsi_ref		= create_model_dataset(ns, model_name="Dsi_ref", include_fav=True,schema="dsi")






### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 

# cf : https://stackoverflow.com/questions/40547670/python-restplus-api-to-upload-and-dowload-files




@ns.doc(security='apikey')
@ns.route('/')
class DsiCreate(Resource):

	# @current_user_required
	@guest_required 
	@ns.expect(file_parser)   ### from "solidata_api._parsers.__init__.file_parser" loaded from "solidata.api.__init__"
	# @ns.marshal_with(model_dsi_in) #, envelope="new_dsi", code=201)
	def post(self):
		"""
		upload a file or external API value and create a new dsi in db
		"""

		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )

		df_is_created = False 

		### TO DO : reuse this function in all endpoints POST / GET / DELETE ...
		payload, is_form, files = return_payload(request, ns.payload)
		log.debug ("payload 	 : \n{}".format(pformat(payload)))

		### DSI - get data from form and preload for marshalling
		new_dsi_infos = { 
			"infos" 		: payload,
			"public_auth" 	: payload,
			"specs"			: {
				"doc_type" : "dsi",
				"src_type" : payload["src_type"],
				"src_link" : payload["src_link"],
			},
		}
		### marshall infos with dsi complete model
		new_dsi 		= marshal( new_dsi_infos , model_dsi_in )
		log.debug('new_dsi : \n%s', pformat(new_dsi) )  

		### DSR - copy dsi to prepare a new_dsr
		new_dsr 		= marshal( new_dsi_infos , model_dsr_in )
		new_dsr["specs"]["doc_type"] = "dsr"
		log.debug('new_dsr : \n%s', pformat(new_dsr) )  


		### check if client is an admin or if is the current user
		### needs decorator @guest_required or @admin_required
		claims 	= get_jwt_claims() 
		log.debug("claims : \n %s", pformat(claims) )
		oid_usr_ = ObjectId(claims["_id"])

		### add log infos
		log_ds =  {
			"created_at" 	: datetime.utcnow(),
			"created_by" 	: oid_usr_,
		}
		team_ds	= [ 
			{
				'oid_usr'	: oid_usr_,
				'edit_auth'	: "owner",
				'added_at'  : datetime.utcnow(),
				'added_by'  : oid_usr_,
			}
		]
		new_dsi["log"] = new_dsr["log"] = log_ds
		new_dsi["team"] = new_dsr["team"] = team_ds
		log.debug("new_dsi : \n %s" , pformat(new_dsi))



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

				### check if file already exists in db
				# existing_dsi = mongo_datasets_inputs.find_one({"specs.src_link" : filename})

				### save data if file is allowed # and not already existing 
				# if existing_dsi is None and allowed_file(filename) : 
				if allowed_file(filename) : 

					### get file extension from file itself
					file_extension = get_file_extension(filename)
					log.debug("file_extension : %s", file_extension)

					### correct file_extension if different
					if file_extension != payload["src_type"] :
						new_dsi["specs"]["src_type"] = file_extension
						new_dsr["specs"]["src_type"] = file_extension

					### delete scr_parser info
					new_dsi["specs"]["src_parser"] = None
					new_dsr["specs"]["src_parser"] = None

					### create dataframe by reading file with pandas
					sep = payload['csv_sep']
					log.debug("trying to read file / sep : %s", sep)
					df = read_file_with_pd(uploaded_file, file_extension, sep=sep )
					df_is_created = True
					
					### add src_sep info
					new_dsi["specs"]["src_sep"] = payload['csv_sep']
					new_dsr["specs"]["src_sep"] = payload['csv_sep']

				### DSI already exists
				else : 
					log.info("-!- filename not permited...")
					# existing_dsi_oid = existing_dsi["_id"]
					return {
								# "msg"		: "your file '{}' already exists in dsi db / try update instead ...".format(filename),
								"msg"		: "your file '{}' format is not permited...".format(filename),
								"data"		: {
									"filename" 	: filename,
									# "_id" 		: str(existing_dsi_oid)
								}
							}, 401

				"""
				### loop through df_col_dict to save each column in mongo_datasets_raws
				for col_key, col_values in df_col_dict.items() : 

				### create new empty dsr object
				new_dsr_infos = {
					"infos" : {
						"title" 		: col_key,
						"licence"		: "private_use_only",
						"description"	: "column '{}' of '{}' file".format(col_key,filename)
					},
					"public_auth" : {
						"guests_can_see" : False,
					},
					"log" : {
						"created_at" 	: datetime.utcnow(),
						"created_by" 	: oid_usr_,
					},
					"specs" : { 
						"doc_type"		: "dsr",
						"src_type"		: get_file_extension(filename), 
						"src_link"		: filename,
					},
					"uses"	: {
						"by_dsi" 			: {
							"used_by" : oid_dsi_ 
						}
					}
				}
				### fill new_dsi_info with the data
				new_dsr 			= marshal( new_dsr_infos , model_dsr_in)
				new_dsr["data_raw"] = col_values

				### save dsr object to db 
				new_dsr_doc 		= mongo_datasets_raws.insert(new_dsr)

				### keep track of new_dsr_doc oid 
				oid_dsr_			= str(new_dsr_doc)
				
				log.info("new_dsr '{}' is saved in db... / oid_dsr_ : {} ".format(col_key, oid_dsr_) )


				### add dsr ref to dsi 
				add_to_datasets(	coll 			= "mongo_datasets_inputs", 
									target_doc_oid	= oid_dsi_, 
									doc_type		= "dsr", 
									oid_by			= oid_usr_, 
									oid_to_add		= oid_dsr_, 
								)

				# args = file_parser.parse_args()
				# if args['data_file'].mimetype in authorized_mimetype :
				# 		destination = os.path.join(app.config.get('DATA_FOLDER'), 'uploads/data_files/')
				# 		if not os.path.exists(destination):
				# 				os.makedirs(destination)
				# 		xls_file = '%s%s' % (destination, 'data_file.xls')
				# 		args['data_file'].save(xls_file)
				# else:
				# 		abort(404)

			
				""" 
			

			### no file detected
			else : 
				log.info("-!- no file detected ...")
				return {
							"msg"		: " no file detected",
						}, 401
			

		### get data from API 
		# if payload["src_type"] == 'API' : 
		else :

			log.debug('payload contains an API reference... ' )  

			### load url
			url = filename = payload["src_link"]
			log.debug('API / url : {}'.format(url) )  

			### check if file already exists in db
			existing_dsi = mongo_datasets_inputs.find_one({"specs.src_link" : filename})

			### save data if file is not already existing 
			if existing_dsi is None : 

				### get the data
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
					new_dsi["specs"]["src_sep"] = None
					new_dsr["specs"]["src_sep"] = None

				### no data detected | API request failed
				else : 
					log.info("-!- request to API failed ...")
					return {
								"msg"		: "request to API failed",
							}, 401

			### DSI already exists
			else : 
				log.info("-!- dsi already exists...")
				existing_dsi_oid = existing_dsi["_id"]
				return {
							"msg"		: "your file '{}' already exists in dsi db / try update instead ...".format(filename),
							"data"		: {
								"filename" 	: filename,
								"_id" 		: str(existing_dsi_oid)
							}
						}, 401


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
			# df = df.fillna(value="")
			df = df.replace({np.nan:None})
			print ("\n", df.head(5)) 

			### get data as records
			# df_col_dict = df.to_dict(orient="list")
			df_col_dict = df.to_dict(orient="records")
			log.debug("df_col_dict (head(3)) : \n %s", pformat(df.head(3).to_dict(orient="records")) )

			### copy records to DSI and DSR : ["data_raw"]["f_data"]
			new_dsi["data_raw"]["f_data"] = df_col_dict
			new_dsi["data_raw"]["f_col_headers"] = df_headers

			new_dsr["data_raw"]["f_data"] = df_col_dict
			new_dsr["data_raw"]["f_col_headers"] = df_headers

			# new_dsi 	= marshal( new_dsi_infos , model_dsi_in)
			# log.debug("new_dsi : \n %s" , pformat(new_dsi))


			### DSI - ORIGNAL VALUES - save dsi object to db 
			new_dsi_doc = mongo_datasets_inputs.insert(new_dsi)
			log.info("new_dsi is saved in db... ")
			### keep track of new_dsi_doc oid 
			oid_dsi_		= new_dsi_doc
			log.info("oid_dsi_ : %s ", str(oid_dsi_) )

			### DSR - VALUES COPIES - save dsr object to db 
			new_dsr_doc = mongo_datasets_raws.insert(new_dsr)
			log.info("new_dsr is saved in db... ")
			### keep track of new_dsr_doc oid 
			oid_dsr_		= new_dsr_doc
			log.info("oid_dsr_ : %s ", str(oid_dsr_) )



			### DSI - add dsi ref to user 
			add_to_datasets(	coll			= "mongo_users", 
								target_doc_oid	= oid_usr_, 
								doc_type		= "dsi", 
								oid_by			= oid_usr_, 
								oid_to_add		= oid_dsi_, 
								include_is_fav	= True
							)

			### DSI - add dsr ref to dsi 
			add_to_datasets(	coll 			= "mongo_datasets_inputs", 
								target_doc_oid	= oid_dsi_, 
								doc_type		= "dsr", 
								oid_by			= oid_usr_, 
								oid_to_add		= oid_dsr_, 
							)

			### DSR - add dsi ref to dsr 
			add_to_uses(		coll 			= "mongo_datasets_raws", 
								target_doc_oid	= oid_dsr_, 
								doc_type		= "dsi", 
								oid_by			= oid_dsi_, 
							)

			### save file in uploads folder if file doesn't exist
			# destination = app.config["UPLOADS_DATA"]
			# log.debug("destination : %s", destination)
			# if not os.path.exists(destination):
			# 	os.makedirs(destination)
			
			# file_path = "{}{}".format( destination, filename )
			# log.debug("file_path : %s", file_path)

			### save file in uploads
			# uploaded_file.save(file_path)
			# log.debug("uploaded_file '{}' saved at file_path : {}".format(uploaded_file, file_path) )

			log.info("--- dsi and dsr are created...")
			return {
						"msg"		: "your file '{}' has been correctly uploaded...".format(filename),
						"data"		: {
							"src_link" 	: payload["src_link"],
							"filename" 	: filename,
							"_id" 		: str(oid_dsi_)
						}
					}, 200


		### no dataframe detected
		else : 

			log.info("-!- dataframe failed to be created ...")

			### delete previously inserted dsr and dsi docs
			mongo_datasets_inputs.delete_one({"_id" : ObjectId(oid_dsi_) })
			mongo_datasets_raws.delete_one({"_id" : ObjectId(oid_dsr_) })

			### send message
			return {
						"msg"		: "dataframe failed to be created",
					}, 401