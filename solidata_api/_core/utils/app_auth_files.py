# -*- encoding: utf-8 -*-

"""
app_auth_files.py  
"""


from log_config import log, pformat

log.debug("... loading app_auth_files.py ...")

from werkzeug.utils import secure_filename
from solidata_api._choices import *


def get_file_extension(filename) : 
	return filename.rsplit('.', 1)[-1].lower()


def allowed_file(filename):
	return '.' in filename and \
		get_file_extension(filename) in authorized_filetypes