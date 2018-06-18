# -*- encoding: utf-8 -*-

"""
authorizations.py  
- describe authorizations
"""

from log_config import log, pprint, pformat
log.debug ("... loading authorizations ...")

authorizations = {
    'apikey': {
        'type'  : 'apiKey',
        'in'    : 'header',
        'name'  : 'X-API-KEY'
    }
}