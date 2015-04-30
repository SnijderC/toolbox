# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,render
from django.template.loader import get_template
from django.db import OperationalError
from django.http import Http404
from helpers.navigation import Navigation
from helpers.page_class import Page
import markdown
import settings
from toolbox.templates.static_file_titles import titles
    
def doc(request,filename,strformat):
    """
        Render a static jade or Markdown file..
        
        Originally all content was dynamically loaded from the database.
        The format was Markdown. But since layouts, specifically the
        landing page became so complex, Markdown wasn't enough.
        
        Markdown's HTML support is limited and requires hacky formatting.
        
        Loading Jade into the DB would have been (and still is) an option.
        However in the interest of more rapid deployment I chose not to.
        And frankly.. because anyone editing those files would require 
        some web knowledge anyway. 
        
        So sorry for this hacky workaround but to get a nice title in the
        titlebar please add your title to the dict in:
        templates/static_file_title.py
    """
    


    # Initialise Navigation and Page classes..
    nav                 = Navigation("/")
    page_filters        = nav.process_slugs()
    page                = Page()
    page.index          = False
    page.data['nav']    = nav
    try:
        filename = filename.lower()
        
        # Try to find a matching title in the titles dict.
        if filename in titles.keys():
            page.title = titles[filename] % settings.title
        # Or fall back to the settings title..
        else:
            page.title = settings.title
        
        # If the format is markdown, open the file and processes the contents..
        if strformat.lower() in ("md","markdown"):

            f = open('toolbox/templates/%s.md' % filename , 'r')
            str_markdown = f.read()
            
            # Using quite a few plugins..
            page.data['markdown'] = markdown.markdown(
                                                        str_markdown.decode("utf-8"),
                                                        extensions=['extra','nl2br','smarty','toc'],
                                                        output_format='html5'
                                                      ).encode('utf-8')
            
            # return html formatted content of markdown file
            page.data['errorpage'] = False;
            return render_to_response('markdown.jade', {"page":page})

        # If the format is Jade the process is quite simple.. 
        elif strformat.lower() == "jade":
        
            # return html formatted content of jade file
            page.data['errorpage'] = False;
            page.data['filename']  = filename
            return render_to_response(filename+".jade", {"page":page})
            
        # If some other file format was requested that is not supported.. 404
        else:
            raise Http404
    # If any error occurs, most likely file doesn't exist – 404 is returned.
    except:
       raise Http404
