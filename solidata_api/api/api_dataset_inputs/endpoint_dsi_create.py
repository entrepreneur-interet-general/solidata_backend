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
model_dsr		= Dsr_infos(ns)
model_dsi_in	= model_dsi.mod_complete_in
model_dsr_in	= model_dsr.mod_complete_in
# model_dsi_ref		= create_model_dataset(ns, model_name="Dsi_ref", include_fav=True,schema="dsi")






### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 

# cf : https://stackoverflow.com/questions/40547670/python-restplus-api-to-upload-and-dowload-files




@ns.doc(security='apikey')
@ns.route('/')
class DsiCreate(Resource):

	# @api.marshal_with(project_model, envelope="projects_list")
	# @current_user_required
	@guest_required 
	@ns.expect(file_parser)
	# @ns.marshal_with(model_dsi_in) #, envelope="new_user", code=201)
	def post(self):
		"""
		upload a file and create a new dsi in db
		"""

		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )

		### load file from request
		args 					= file_parser.parse_args()
		uploaded_file = args['data_file']  # This is FileStorage instance
		log.debug("uploaded_file : \n %s", uploaded_file )

		### check if client is an admin or if is the current user
		claims 	= get_jwt_claims() 
		log.debug("claims : \n %s", pformat(claims) )
		oid_usr_ = claims["_id"]

		### check extension and mimetype
		if uploaded_file and allowed_file(uploaded_file.filename) : 
			
			### create a secure filename
			filename = secure_filename(uploaded_file.filename)
			log.debug("filename : %s", filename)


			### check if file already exists in db
			existing_dsi = mongo_datasets_inputs.find_one({"specs.src_link" : filename})

			if existing_dsi is None and allowed_file(filename) : 

				file_extension = get_file_extension(filename)


				### read file with pandas
				df = read_file_with_pd(uploaded_file,file_extension )

				### drop rows where all values are nan
				df = df.dropna(how="all")
				print (df.head(5)) 

				### trim columns' titles 
				df_col_dict = df.to_dict(orient="list")
				log.debug("df.to_dict(orient='list') : \n %s", pformat(df.head(5).to_dict(orient="list")) )

				### save file in uploads folder if file doesn't exist
				destination = app.config["UPLOADS_DATA"]
				log.debug("destination : %s", destination)
				if not os.path.exists(destination):
					os.makedirs(destination)
				
				file_path = "{}{}".format( destination, filename )
				log.debug("file_path : %s", file_path)

				### save file in uploads
				uploaded_file.save(file_path)
				log.debug("uploaded_file '{}' saved at file_path : {}".format(uploaded_file, file_path) )
				

				### create new empty dsi object
				new_dsi_infos = {
					"infos" : {
						"title" 		: filename,
					},
					"log" : {
						"created_at" 	: datetime.utcnow(),
						"created_by" 	: oid_usr_,
					},
					"specs" : { 
						"doc_type" 		: "dsi",
						"src_type" 		: file_extension, 
						"src_link" 		: filename,
					},
				}
				log.debug("new_dsi_infos : \n %s" , pformat(new_dsi_infos))

				new_dsi 	= marshal( new_dsi_infos , model_dsi_in)
				log.debug("new_dsi : \n %s" , pformat(new_dsi))

				### save dsi object to db 
				new_dsi_doc = mongo_datasets_inputs.insert(new_dsi)
				log.info("new_dsi is saved in db... ")

				### keep track of new_dsi_doc oid 
				oid_dsi_		= str(new_dsi_doc)
				log.info("oid_dsi_ : %s ", oid_dsi_ )



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



				### add dsi ref to user 
				add_to_datasets(	coll			= "mongo_users", 
									target_doc_oid	= oid_usr_, 
									doc_type		= "dsi", 
									oid_by			= oid_usr_, 
									oid_to_add		= oid_dsi_, 
									include_is_fav	= True
								)


				return {
							"msg"				: "your file '{}' has been correctly uploaded...".format(filename),
							"filename" 	: filename,
							"oid_dsi" 	: str(oid_dsi_)
						}, 200
			
			else : 
				existing_dsi_oid = existing_dsi["_id"]
				return {
							"msg"		: "your file '{}' already exists in dsi db / try update instead ...".format(filename),
							"filename" 	: filename,
							"oid_dsi" 	: str(existing_dsi_oid)
						}, 401