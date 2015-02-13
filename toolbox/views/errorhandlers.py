# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from helpers.page_class import Page

def handler404(request):
    return commonhandler(request, 404)

def handler500(request):
    return commonhandler(request, 500)

def handler400(request):
    return commonhandler(request, 400)

def handler403(request):
    return commonhandler(request, 403)

def handler502(request):
    return commonhandler(request, 502)

def commonhandler(request, code):
    page = Page()
    page.data['errorpage'] = True
    page.data['error'] = ""
    response = render_to_response('errorpage.jade', {"page":page} ,context_instance=RequestContext(request))
    response.status_code = code
    return response
