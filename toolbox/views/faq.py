# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from helpers.page_class import Page
from helpers.navigation import Navigation
from toolbox.models import FAQCategories
from django.db import OperationalError
from django.http import Http404
import re
import settings

def faq(request):
    
    print "dafaq!"
    # placeholder for page data
    page = Page()
    page.index = False
    # nav provides Navbar, Sitemap, selected Filters, processing of slugs etc.
    nav = Navigation('')
    # Get reverse slugs from nav.
    sluglistrev = nav.sluglistrev
    
    page.meta['section'] = "FAQ"
    
    # Set the template to the playlist template
    template = "faq.jade"
    try:
        faq_obj = FAQCategories.objects.all()
    except FAQCategories.DoesNotExist:
        raise Http404

    page.title = "FAQ | %s" % settings.title
    page.data['nav']            = nav
    page.data['navlinks']       = nav.categorieslinks
    page.data['debug']          = ''
    page.data['item']           = faq_obj
       
    return render_to_response(template, {"page":page})