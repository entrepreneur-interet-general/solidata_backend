# -*- encoding: utf-8 -*-

"""
_core/emailing/__init__.py  
- provides the EMAILING 
"""

from log_config import log, pformat
print()
log.debug(">>> _core.emailing.__init__.py ..." )
log.debug(">>> emailing ... loading emailing functions as global variables")

from flask_mail import Message

from flask import current_app as app

from solidata_api.application import mail


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### EMAILING FUNCTIONS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###


def send_email( subject, 
								to, 
								sender = app.config["MAIL_DEFAULT_SENDER"], 
								template = None ) :
	"""
	generic function to send an email 
	"""
	
	log.debug("... sending email...")

	email_msg 			= Message( 
		subject, 
		recipients	= [to], 
		sender			= sender, 
		html				= template,
	)
	mail.send(email_msg)