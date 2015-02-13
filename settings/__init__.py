# -*- coding: utf-8 -*-
"""
	Make a nice generic settings structure.
	
	!!!IMPORTANT!!!

	There may be 2 files living in this dir: 
		- development.py
		- production.py

	IF development.py exists it's methods will be imported.
	This is *NOT* appropriate for a production environment.
	If you are running in production you should not have 
	development.py file. It should be excluded from the 
	source when it is published. If it isn't for some
	reason, you should DELETE the development.py file!

	ONLY if the development.py file doesn't exist will
	production.py's methods be imported.

"""

from django import *
from production import *

try: 
    from development import *
except:
    pass    