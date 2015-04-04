# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template.loader import get_template
import re
from helpers.page_class import Page
from helpers.navigation import Navigation
from toolbox.models import Tool, Advice
from django.db.models import Q
from django.db import OperationalError
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import Http404
import settings

def indexpage(request,slugs):
    # placeholder for page data
    page = Page()
    # nav provides Navbar, Sitemap, selected Filters, processing of slugs etc.
    nav = Navigation(slugs)
    # A dict of models for the index pages, all for index.jade or one for page.jade
    table_objects = { "advices" : Advice, "tools" : Tool }
    # Get selected filters to pass to models..
    filters = nav.filters
    # Get reverse slugs from nav.
    sluglistrev = nav.sluglistrev
    # Determine specific request for layout and or item in models
    item_slug = filters['item_slug']
    item_arg = filters['item_arg']

    # item_slug can determine a layout and selection of article types from db
    # If item_slug is "overview" the main index should be displayed
    if item_slug and item_slug == "overview":
        template = "index.jade"
    # A specific model is selected and/or a specific item is selected
    elif item_slug:
        template = "page.jade"
        # Reduce the dict of models to 1 model
        table_objects = { item_slug : table_objects[item_slug] }
    # Only other options are static docs and root (/),
    # those are handled in app.py so we shouldn't end up here..
    else:
        raise Http404
        
    
    for key, table in table_objects.iteritems():
        
        if item_slug and item_arg:
            table_objects[key] = table_objects[key].objects.filter(slug=item_arg)
            page.index = False
        else:
            table_objects[key] = table_objects[key].objects.order_by('-date').order_by('-feature_score').defer("intro_md","content_md")
            for strslug in filters:
                if strslug not in ("item_slug","item_arg"):
                    for strarg in filters[strslug]:
                        if re.match("^[a-zA-Z0-9\-\_]*$",strslug):
                            kwargs = { "%s__id" % strslug : nav[strslug][strarg]['id'] } 
                            table_objects[key] = table_objects[key].filter(**kwargs)

        table_objects[key] = table_objects[key].exclude(published=False)

    strtitle    = ""
    # if item_slug and item_arg:
    if item_slug and item_slug != "overview":
        page.data['item'] = table_objects[key].prefetch_related()
        strtitle += "%s | " % sluglistrev[item_slug]['slug'].capitalize()
        if item_arg and table_objects[key].exists():
            strtitle = "%s - " % table_objects[key][0].title + strtitle
    else:
        for key, table in table_objects.iteritems():
            page.data[key] = table_objects[key].prefetch_related()
        if item_slug == "overview":
            strtitle += "%s | " % sluglistrev[item_slug]['slug'].capitalize()
    
    page.title                  = strtitle + settings.title 
    page.data['nav']            = nav
    page.data['navlinks']       = nav.categorieslinks
    page.data['request']        = request
    page.data['filters']        = nav.filter_dropdowns
    page.data['debug_str']      = ""
    page.data['errorpage']      = False
    page.data['itemslug']       = sluglistrev[item_slug]['slug']
    #page.data['debug']          = ''
    page.show_filters           = True
       
    return render_to_response(template, {"page":page})
    