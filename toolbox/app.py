# -*- coding: utf-8 -*-
"""

 _____  _____  _____    ____  _____  _____  ____   _____  _____  __  __
/  _  \/  _  \/   __\  /    \/  _  \/  _  \/  _/  /  _  \/  _  \/  \/  \
|  _  <|  |  ||   __|  \-  -/|  |  ||  |  ||  |---|  _  <|  |  |>-    -<
\_____/\_____/\__/      |__| \_____/\_____/\_____/\_____/\_____/\__/\__/

 __ __  _____     _____     _____
/  |  \/  _  \   /  _  \   |  ___|
\  |  /|  |  | _ \___  | _ |___  \
 \___/ \_____/<_>|_____/<_><_____/

"""

from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url
from django.contrib import admin
from toolbox import views

admin.autodiscover()

urlpatterns = [
    # Static landing page: landing.jade
    url(
        r'^$',
        views.static_doc.doc,
        {
            "filename": "landing",
            "strformat": "jade"
        }
    ),
    # Django admin site
    url(
        r'^admin/',
        admin.site.urls
    ),
    # Static docs (jade and markdown..)
    url(
        r'^doc/([a-zA-Z0-9\-]{1,40})/$',
        views.static_doc.doc,
        {"strformat": "markdown"}
    ),
    # Static docs, licenses dir (jade and markdown..)
    url(
        r'^doc/(licenses/[a-zA-Z0-9\-]{1,40})/$',
        views.static_doc.doc,
        {"strformat": "markdown"}
    ),
    # Search queries. (max 120 chars, input allows 40, every char may be "%20"
    url(
        r'^search/(?P<query>.{2,120})/$',
        views.search.query
    ),
    # FAQ
    url(
        r'^faq/$',
        views.faq.faq
    ),
    # Playlists selection
    url(
        r'^playlist/(?P<playlist>[a-zA-Z0-9\-]{2,40})/$',
        views.playlist.playlist
    ),
    # Playlists page selection
    url(
        r'^playlist/(?P<playlist>[a-zA-Z0-9\-]{2,40})/(?P<item>[0-9]{1,3})/$',
        views.playlist.playlist_item
    ),
    # Dynamic pages based on custom slugs functions in
    # views/helpers/navigation.py
    url(
        r'^([a-zA-Z0-9\-\/]{1,2000}/)?$',
        views.index.indexpage
    ),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

handler404 = "toolbox.views.errorhandlers.handler404"
handler400 = "toolbox.views.errorhandlers.handler400"
handler500 = "toolbox.views.errorhandlers.handler500"
handler403 = "toolbox.views.errorhandlers.handler403"
handler502 = "toolbox.views.errorhandlers.handler502"


# ASCII Art generator
# http://patorjk.com/software/taag/#p=testall&f=Spliff&t=BOF%20Toolbox%0Av0.9
