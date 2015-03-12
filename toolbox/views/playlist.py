# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template.loader import get_template
from helpers.page_class import Page
from helpers.navigation import Navigation
from toolbox.models import Advice, Playlist, PlaylistOrder
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
        playlist_obj = Playlist.objects.exclude(published=False).get(slug=playlist)
    except Playlist.DoesNotExist:
        raise Http404

    page.title = "%s | %s" % (playlist_obj.title,settings.title)
    page.data['nav']            = nav
    page.data['navlinks']       = nav.categorieslinks
    page.data['debug']          = ''#playlist_obj.playlistorder_set.__dict__
    page.data['item']           = playlist_obj  
       
    return render_to_response(template, {"page":page})
    
def playlist_item(request,playlist,item):
    # placeholder for page data
    page = Page()
    # nav provides Navbar, Sitemap, selected Filters, processing of slugs etc.
    nav = Navigation('')
    # Get reverse slugs from nav.
    sluglistrev = nav.sluglistrev

    # Set the template to the playlist template
    template = "page.jade"
    
    try:
        advice       = Advice.objects.exclude(published=False).exclude(playlist__published=False).filter(playlist__slug=playlist,playlistorder__number=item).defer('intro_md').defer('content_md')[0]
        playlist_obj = PlaylistOrder.objects.exclude(playlist__published=False).filter(playlist__slug=playlist).order_by('number')
    except Playlist.DoesNotExist:
        raise Http404 
    except IndexError:
        raise Http404
    
    num = 0    
    for i, item in enumerate(playlist_obj):
        if item.advice.id == advice.id:
            num = i

    if num-1 > -1:
        page.data["previous"] = "/playlist/%s/%s/" % (playlist,playlist_obj[num-1].number)
    if num+1 <= playlist_obj.__len__()-1:
        page.data["next"] = "/playlist/%s/%s/" % (playlist,playlist_obj[num+1].number)
    
    page.data['playlist'] = "/playlist/%s/" % playlist   
        
    page.title = "%s | %s" % (advice.title,settings.title)
    page.data['nav']            = nav
    page.data['navlinks']       = nav.categorieslinks
    page.data['item']           = (advice,)
    page.index                  = False
    page.playlist               = True
       
    return render_to_response(template, {"page":page})
    