# -*- encoding: utf-8 -*-

"""
schema_datamodels.py  
- provides the model for DATAMODEL definition in DB and Flask-Restplus
"""

from log_config import log, pformat

log.debug("... loading schema_datamodels.py ...")

from flask_restplus import fields

from .schema_generic import *
from .schema_logs import *
from .schema_users import *