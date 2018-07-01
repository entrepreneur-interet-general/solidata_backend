# -*- encoding: utf-8 -*-

"""
_core/async_tasks/__init__.py  
- provides ASYNC FUNCTIONS | DECORATORS 
"""

from log_config import log, pformat
print()
log.debug(">>> _core.async_tasks.__init__.py ..." )
log.debug(">>> async ... loading async functions as global variables")

from threading import Thread

# from flask import current_app 



### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ASYNC FUNCTIONS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
# cf : https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xi-email-support 


def async(f):
	"""
	async decorator to run a function as a thread
	"""
	def wrapper(*args, **kwargs):
		thr = Thread(target=f, args=args, kwargs=kwargs)
		thr.start()
	return wrapper
