# -*- encoding: utf-8 -*-

"""
endpoint_dsi_create.py  
- provides the API endpoints for consuming and producing
	REST requests and responses
"""

from solidata_api.api import *

log.debug(">>> api_dataset_inputs ... creating api endpoints for DSI_CREATE")

### create namespace
ns = Namespace('create', description='Projects : create a new dataset_input')

### import models 
from solidata_api._models.models_dataset_input import * 
model_dsi_in		= Dsi_infos(ns).mod_complete_in


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 

# cf : https://stackoverflow.com/questions/40547670/python-restplus-api-to-upload-and-dowload-files


### ROUTES
@ns.route('/')
class DsiCreate(Resource):

	# @api.marshal_with(project_model, envelope="projects_list")
	@guest_required 
	# @current_user_required
	@ns.expect(file_parser)
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

		### check extension and mimetype
		if uploaded_file and allowed_file(uploaded_file.filename) : 
			
			### create a secure filename
			filename = secure_filename(uploaded_file.filename)
			log.debug("filename : %s", filename)


			### read file with pandas
			df = pd.read_csv(uploaded_file)
			print (df.head(5)) 


			### trim columns' titles and save them as col_code + col_oid
			df_col_dict = df.to_dict()

			### check if file already exists in uploads


			### save file in uploads folder if file doesn't exist
			# destination = os.path.join(app.config["UPLOADS_DATA"])
			destination = app.config["UPLOADS_DATA"]
			log.debug("destination : %s", destination)
			if not os.path.exists(destination):
				os.makedirs(destination)
			
			file_path = "{}{}".format( destination, filename )
			log.debug("file_path : %s", file_path)

			uploaded_file.save(file_path)
			log.debug("uploaded_file '{}' saved at file_path : {}".format(uploaded_file, file_path) )
			



			### create new dsi object
			new_dsi_info = {
				"log" : {
					"created_at" : datetime.utcnow(),
					"created_by" : claims["_id"],
				},
				"specs" : { 
					"doc_type" : "dsi",
					"src_type" : get_file_extension(filename), 
					"src_link" : filename,
					}
			}
			log.debug("new_dsi_info : \n %s" , pformat(new_dsi_info))

			new_dsi 	= marshal( new_dsi_info , model_dsi_in)
			log.debug("new_dsi : \n %s" , pformat(new_dsi))



			### save dsi object to db 
			mongo_datasets_inputs.save(new_dsi)
			log.info("new_dsi is saved in db ")


			# args = file_parser.parse_args()
			# if args['data_file'].mimetype in authorized_mimetype :
			# 		destination = os.path.join(app.config.get('DATA_FOLDER'), 'uploads/data_files/')
			# 		if not os.path.exists(destination):
			# 				os.makedirs(destination)
			# 		xls_file = '%s%s' % (destination, 'data_file.xls')
			# 		args['data_file'].save(xls_file)
			# else:
			# 		abort(404)

			return {
									"msg"			: "your file has been correctly uploaded...",
								}, 200