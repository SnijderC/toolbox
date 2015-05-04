from settings import meta_templates
from settings import tweet_templates
from settings import DEBUG
from easy_thumbnails.files import get_thumbnailer
import re
def set_metatags(metatags, article):

    try:
        if 'title' in article.__dict__:
            metatags['title'] = meta_templates['title'] % article.title
            if article._meta.model_name == "tools":
                metatags['title'] = "Tool: %s" % metatags['title']
        if 'intro_html' in article.__dict__:
            desc = meta_templates['description']
            desc = desc % re.sub("<(.*?)>","",article.intro_html)
            if desc.__len__() > 199:
                desc = u"%s \u2026" % desc[0:198]
            metatags['description'] = desc
        if hasattr(article,'meta_date'):
            metatags['publishedtime'] = article.meta_date
    
        if hasattr(article,'meta_datemodified'):
            metatags['modifiedtime'] = article.meta_datemodified
        
        metatags['section'] = article.url_slug().capitalize()
        
        if hasattr(article,'categories'):
            metatags['articletags'] = []
            for category in article.categories.all():
                metatags['articletags'].append(category)
        
        metatags['permalink'] = meta_templates['permalink'] % "/%s/%s/" % (article.url_slug(),article.slug)
    
        try:
            if article.has_image():
                metatags['imagelink'] = meta_templates['permalink'] % get_thumbnailer(article.image)['social'].url
            else:
                metatags['imagelink'] = None
                
            metatags['type'] = "article"
        except:
            pass # ugly fix for missing images
        
        if hasattr(article,'credit') and article.credit != "":
            metatags['author'] = article.credit
        elif hasattr(article,'user'):    
            metatags['author'] = "%s %s" % (article.user.first_name, article.user.last_name)
    
        if hasattr(article, 'i_am'):
            metatags['tweet_article'] = tweet_templates[article.i_am()] #% article.title
    
    
        return metatags
    
    except Exception, e: 
        print e
        pass
        