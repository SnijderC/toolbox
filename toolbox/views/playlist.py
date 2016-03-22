# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from helpers.page_class import Page
from helpers.navigation import Navigation
from helpers.metatags import set_metatags
from toolbox.models import Advice, Playlist, PlaylistOrder
from django.http import Http404
import settings


def playlist(request, playlist):
    # placeholder for page data
    page = Page()
    page.index = False
    # nav provides Navbar, Sitemap, selected Filters, processing of slugs etc.
    nav = Navigation('')

    # Get reverse slugs from nav.
    sluglistrev = nav.sluglistrev

    # Set the template to the playlist template
    template = "playlist.jade"

    try:
        playlist_obj = Playlist.objects.exclude(
            published=False).get(slug=playlist)
        # TODO: Nice pep8 alignment
        playlist_order_obj = PlaylistOrder.objects.exclude(
            playlist__published=False
        ).filter(playlist__slug=playlist).order_by('number')
    except Playlist.DoesNotExist:
        raise Http404

    page.meta = set_metatags(page.meta, playlist_obj)
    page.title = "%s | %s" % (playlist_obj.title, settings.title)
    page.data['nav'] = nav
    page.data['navlinks'] = nav.categorieslinks
    page.data['debug_str'] = ''  # playlist_obj.playlistorder_set.__dict__
    page.data['item'] = playlist_obj
    page.data['playlist'] = playlist_order_obj
    page.data['playlist_href'] = "/playlist/%s/" % playlist
    page.playlist = True

    return render_to_response(template, {"page": page})


def playlist_item(request, playlist, item):
    # placeholder for page data
    page = Page()
    # nav provides Navbar, Sitemap, selected Filters, processing of slugs etc.
    nav = Navigation('')
    # Get reverse slugs from nav.
    sluglistrev = nav.sluglistrev

    # Set the template to the playlist template
    template = "page.jade"

    try:
        advice = Advice.objects.exclude(published=False).exclude(playlist__published=False).filter(
            playlist__slug=playlist, playlistorder__number=item).defer('intro_md').defer('content_md')[0]
        playlist_obj = PlaylistOrder.objects.exclude(playlist__published=False).filter(
            playlist__slug=playlist).order_by('number')
    except Playlist.DoesNotExist:
        raise Http404
    except IndexError:
        raise Http404

    page.meta = set_metatags(page.meta, advice)

    num = 0
    for i, item in enumerate(playlist_obj):
        if item.advice.id == advice.id:
            num = i

    if num-1 > -1:
        page.data[
            "previous"] = "/playlist/%s/%s/" % (playlist, playlist_obj[num-1].number)
    if num+1 <= playlist_obj.__len__()-1:
        page.data[
            "next"] = "/playlist/%s/%s/" % (playlist, playlist_obj[num+1].number)

    page.data['playlist'] = "/playlist/%s/" % playlist

    page.title = "%s | %s" % (advice.title, settings.title)
    page.data['nav'] = nav
    page.data['navlinks'] = nav.categorieslinks
    page.data['item'] = (advice,)
    page.data['playlist_href'] = "/playlist/%s/" % playlist
    page.index = False
    page.playlist = True
    page.data['itemnr'] = num+1
    page.data['nav_title'] = "Stappenplan"

    return render_to_response(template, {"page": page})
