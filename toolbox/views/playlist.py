# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template.loader import get_template
from helpers.page_class import Page
from helpers.navigation import Navigation
from toolbox.models import Advice, Playlist
from django.db import OperationalError
from django.http import Http404
import re
import settings

def playlist(request,playlist):
    # placeholder for page data
    page = Page()
    # nav provides Navbar, Sitemap, selected Filters, processing of slugs etc.
    nav = Navigation('')
    # Get reverse slugs from nav.
    sluglistrev = nav.sluglistrev

    # Set the template to the playlist template
    template = "playlist.jade"
    
    try:
        playlist_obj = Playlist.objects.defer("intro_md").exclude(published=False).get(slug=playlist)
    except Playlist.DoesNotExist:
        raise Http404

    page.title = "%s | %s" % (playlist_obj.title,settings.title)
    page.data['nav']            = nav
    page.data['navlinks']       = nav.categorieslinks
    page.data['debug']          = ''#playlist_obj.playlistorder_set.__dict__
    page.data['item']           = playlist_obj  
       
    return render_to_response(template, {"page":page})
    
def playlist_item(request,slugs):
    pass