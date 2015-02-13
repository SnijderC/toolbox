# -*- coding: utf-8 -*-
"""
                                                                                    
     ______ _______ _______      _______               __ __                
    |   __ \       |    ___|    |_     _|.-----.-----.|  |  |--.-----.--.--.
    |   __ <   -   |    ___|      |   |  |  _  |  _  ||  |  _  |  _  |_   _|
    |______/_______|___|          |___|  |_____|_____||__|_____|_____|__.__|
                                                                            
            ______    ______                                                
    .--.--.|      |  |  __  |                                               
    |  |  ||  --  |__|__    |                                               
     \___/ |______|__|______|     


"""

import settings
import setup   

from django.conf.urls import patterns, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from toolbox.views import index, static_doc, search, errorhandlers

admin.autodiscover()

if settings.DEBUG:
    # For debugging error pages..
    urlpatterns = patterns('',
                    (r'^error/(?P<code>[0-9]{3})/$', errorhandlers.commonhandler)
                  )
    urlpatterns += staticfiles_urlpatterns()
else:
    urlpatterns = []

urlpatterns += [
    # Static landing page: landing.jade
    url(r'^$', static_doc.doc, {"filename":"landing", "strformat":"jade"}),
    # Django admin site
    url(r'^admin/', admin.site.urls),
    # Static docs (jade and markdown..)
    url(r'^doc/([a-zA-Z0-9\-]{1,40})/$', static_doc.doc, {"strformat":"markdown"}),
    # Static docs, licenses dir (jade and markdown..)
    url(r'^doc/(licenses/[a-zA-Z0-9\-]{1,40})/$', static_doc.doc, {"strformat":"markdown"}),
    # Search queries. (max 120 chars, input allows 40, every char may be "%20"
    url(r'^search/(?P<query>.{2,120})/$', search.query),
    # Dynamic pages based on custom slugs functions in views/helpers/navigation.py    
    url(r'^([a-zA-Z0-9\-\/]{1,2000}/)?$', index.indexpage),
    ]

handler404 = "toolbox.views.errorhandlers.handler404"
handler400 = "toolbox.views.errorhandlers.handler400"
handler500 = "toolbox.views.errorhandlers.handler500"
handler403 = "toolbox.views.errorhandlers.handler403"
handler502 = "toolbox.views.errorhandlers.handler502"


# ASCII Art generator
# http://patorjk.com/software/taag/#p=testall&f=Spliff&t=BOF%20Toolbox%0Av0.9