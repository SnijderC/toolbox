# -*- coding: utf-8 -*-
#import settings.models as models
import json
import re
import settings
from django.db import models
from django.http import HttpResponse
from toolbox.models import Tool, Advice, Service, Category, Platform

def query(request, query):
    """
        Return search results in JSON for queries.
    """
    resp = {}
    
    try:
    
        # This array determines the models and fields to be searched for the search function.
        # "slug" : { 'model' : modelname, 'fields' : [ 'fieldname1', 'fieldname2' ] } 
        
        models = { 
                    'tools'     : {
                                    'model'         : Tool,
                                    'field'         : 'title',
                                    'checkpublished': True,
                                    'hasIcon'       : False,
                                    'href'          : "/tools/%s/"
                                  }, 
                    'adviezen'  : {                 
                                    'model'         : Advice,
                                    'field'         : 'title',
                                    'checkpublished': True,
                                    'hasIcon'       : False,
                                    'href'          : "/adviezen/%s/"
                                  },                
                    'diensten'  : {                 
                                    'model'         : Service,
                                    'field'         : 'title',
                                    'checkpublished': True,
                                    'hasIcon'       : False,
                                    'href'          : "/diensten/%s/"
                                  },                
                    'categorie' : {                 
                                    'model'         : Category,
                                    'field'         : 'name',
                                    'checkpublished': False,
                                    'hasIcon'       : True,
                                    'href'          : "/overzicht/categorie/%s/"
                                  },
                    'platforms' : {                 
                                    'model'         : Platform,
                                    'field'         : 'name',
                                    'checkpublished': False,
                                    'hasIcon'       : True,
                                    'href'          : "/overzicht/platform/%s/"
                                  }
             }
        for name, model in models.iteritems():
            # make a dict with modelname keys..
            resp[name]   = []
        resp['messages'] = []
            
        query = query.replace("*","") + "*"
    
        # for each model..
        for name, model in models.iteritems():
            # Search the models specified above.. 
            
            # Exclude unpublished items
            searchres = model['model'].objects
            
            if model['checkpublished']:
                searchres = searchres.exclude(published=False)

            # Set model's field to search..
            kwargs = { "%s__search" % model['field'] : query}

            # Set output fields..
            args   = [model['field'], 'slug']
            
            # Does this model have an icon field?
            if model['hasIcon']:
                args.append('icon')
            
            # Apply the previous 2 variables..
            searchres = searchres.filter(**kwargs).only(*args)
            
            for res in searchres.values():
                
                if model['hasIcon']:
                    icon = res['icon']
                else:
                    icon = "tb-"+name
                
                # append seachresults
                resp[name].append({
                                    'title'     : res[model['field']],
                                    'href'      : model['href'] % res['slug'],
                                    'icon'      : icon,
                                    'group'     : name.capitalize()
                                })
    # If some Exception occurs, give an error message..
    except:
        resp['messages'].append({
                                    'title'     : 'Onbekende fout opgetreden..',
                                    'href'      : '#',
                                    'icon'      : 'tb-warning',
                                    'group'     : 'Messages'
                                })
    """
    if settings.DEBUG:
        resp['messages'].append({
                                    'title'     : query[:-1],
                                    'href'      : '#',
                                    'icon'      : 'tb-search',
                                    'group'     : 'Query'
                                })
    """
    # Dump the searchresults dict to the client in JSON format    
    return HttpResponse(json.dumps(resp), content_type="application/json")
