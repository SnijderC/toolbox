# -*- coding: utf-8 -*-
#import settings.models as models
import json
import re
import settings
from django.db import models
from django.http import HttpResponse
from toolbox.models import Tool, Advice, Category, Platform, Playlist
from django.db import connection
def query(request, query):
    """
        Return search results in JSON for queries.
    """
    resp = {}
    
    
    base_query = '''
SELECT 
    `id`,
    %(icon_field)s
    `%(table)s`.`slug`,
    `%(table)s`.`%(title)s` as name,
    (IF(`%(table)s`.`%(title)s` LIKE %%s,2,1) * MATCH (%(matches)s) AGAINST ("%%s" IN BOOLEAN MODE)) AS `relevance`
FROM 
    `%(table)s`
WHERE 
    %(check_published)s 
    MATCH (%(matches)s) AGAINST ("%%s" IN BOOLEAN MODE)
ORDER BY `relevance` DESC
LIMIT 5;
'''    
    try:
    
        # This array determines the models and fields to be searched for the search function.
        
        models = [ 
                    {
                        'name'          : 'tools',
                        'model'         : Tool,
                        'fields'        : ['title', 'intro_md', 'content_md'],
                        'title'         : 'title',
                        'checkpublished': True,
                        'hasIcon'       : False,
                        'href'          : "/tools/%s/",
                        'icon'          : 'tb-tools'
                    }, 
                    {
                        'name'          : 'adviezen',
                        'model'         : Advice,
                        'fields'        : ['title', 'intro_md', 'content_md'],
                        'title'         : 'title',
                        'checkpublished': True,
                        'hasIcon'       : False,
                        'href'          : "/adviezen/%s/",
                        'icon'          : 'tb-info'
                    },                                
                    {       
                        'name'          : 'categorie',        
                        'model'         : Category,
                        'fields'        : ['name'],
                        'title'         : 'name',
                        'checkpublished': False,
                        'hasIcon'       : True,
                        'href'          : "/overzicht/categorie/%s/",
                        'icon'          : 'tb-label'
                    },
                    {                 
                        'name'          : 'platforms',
                        'model'         : Platform,
                        'fields'        : ['name'],
                        'title'         : 'name',
                        'checkpublished': False,
                        'hasIcon'       : True,
                        'href'          : "/overzicht/platform/%s/",
                        'icon'          : 'tb-platforms'
                    },
                    {                 
                        'name'          : 'playlist',
                        'model'         : Playlist,
                        'fields'        : ['title', 'intro_md'],
                        'title'         : 'title',
                        'checkpublished': False,
                        'hasIcon'       : True,
                        'href'          : "/playlist/%s/",
                        'icon'          : 'tb-rocket'
                    }
             ]
        for model in models:
            # make a dict with modelname keys..
            resp[model['name']]   = []
        
        query = "".join(re.findall('[a-zA-Z0-9 ]', query))
        like = "%%%s%%" % query
        query += "*"

        # for each model..
        for model in models:
            # Search the models specified above.. 
            tablename = model['model']._meta.db_table
            model['table']           = tablename
            model['icon_field']      = ''
            model['check_published'] = ''
            model['matches']         = ''
            model['like']            = like 
            
            # Does this model have an icon field?
            if model['hasIcon']:
                model['icon_field'] = '`%s`.`icon`,\n' % tablename
             
            # Categories have no published state
            if model['checkpublished']:
                model['check_published'] = '`%s`.`published` = TRUE AND\n' % tablename
            
            for field in model['fields']:
                model['matches'] += '`%s`.`%s`, ' % (tablename, field)
            
            model['matches'] = model['matches'].rstrip(", ")
                
            strquery = base_query % model
            
            # Exclude unpublished items
            
            group = {
                'icon'       : model['icon'],
                'title'      : model['name'].capitalize(),
                'suggestions': [],
            }
            resp[model['name']] = group
            suggestions         = group['suggestions']
            
            for res in model['model'].objects.raw(strquery,[like, query, query]):
                   
                if model['hasIcon']:
                    icon = res.icon
                else:
                    icon = "tb-"+model['name']
                
                # append seachresults
                suggestions.append({
                                    'title'     : res.name,
                                    'href'      : model['href'] % res.slug,
                                    'icon'      : icon,
                                })
            #print connection.queries[-1]['sql']
            
    # If some Exception occurs, give an error message..
    except Exception, e:
        #raise e
        errstr = ''
        if settings.DEBUG:
            errstr = str(e)
        group = {
                'icon'       : 'tb-error',
                'title'      : 'Error',
                'suggestions': [],
            }
        resp['messages']    = group
        suggestions         = group['suggestions']
        suggestions.append({
                                'title'     : 'Onbekende fout opgetreden..',
                                'href'      : '#',
                                'icon'      : 'tb-warning',
                                'error'     : errstr
                            })
    """
    if settings.DEBUG:
        suggestions.append({
                                'title'     : query[:-1],
                                'href'      : '#',
                                'icon'      : 'tb-search',
                                'group'     : 'Query'
                            })
    """
    # Dump the searchresults dict to the client in JSON format    
    return HttpResponse(json.dumps(resp), content_type="application/json")
