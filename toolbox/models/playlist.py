# -*- coding: utf-8 -*-
from django.db import models
from generic import GenericFields
from django.utils.safestring import mark_safe
from terms import Terms
import datetime
import settings
import re

class PlaylistOrder(models.Model):
    playlist        = models.ForeignKey('Playlist')
    advice          = models.ForeignKey('Advice')
    number          = models.IntegerField(
                                            verbose_name    = 'Volgorde',
                                        )
    class Meta:
        """
            Change display of model in Django admin
        """ 
        app_label = "toolbox"
        verbose_name = "Playlist inhoud"
        verbose_name_plural = "Inhoud playlists"
        
    def __unicode__(self):
        """
            String representation of the model
        """
        return self.playlist.title


class Playlist(GenericFields):

                                          
    title       = models.CharField   (
                                         verbose_name    = 'Titel',
                                         max_length      = 60
                                     )
    
    i_want_to   = models.CharField   (
                                         verbose_name    = 'Doel',
                                         max_length      = 120,
                                         help_text       = 'Ik wil mijn data beschermen'
                                     ) 
                                     
    intro_md    = models.TextField   (   
                                         verbose_name    = 'Intro',
                                         blank           = True
                                     )
                                     
    intro_html  = models.TextField  (   
                                         verbose_name    = 'Intro',
                                         blank           = True,
                                         editable        = False
                                     )
                                              
    date        = models.DateTimeField (  
                                        verbose_name    = 'Laatste update'
                                     ) 
                                                                                                                                                  
    published   = models.BooleanField ( verbose_name   = "Publiseer" )

    playlist    = models.ManyToManyField ( 
                                       'Advice',
                                       verbose_name    = 'Playlist',
                                       blank           = True,
                                       through         = 'PlaylistOrder',
                                     )

    str_intro_md = ""
        
    def clean(self):
        """
            Process inline images for markdown, check if they exist or raise Exception.
        """
        try:
            self.str_intro_md = self.intro_md + self.process_inline_images(self.intro_md)
        except:
            raise

    def save(self, *args, **kw):
        """            
            Convert markdown to html to speed up the pageloading.
        """
        
        if not kw.pop('skip_date_update', False):
            self.date = datetime.datetime.now()
        
        self.intro_html = self.cache_md([self.str_intro_md])[0]
        
        super(GenericFields, self).save(*args, **kw)

    def intro(self):
        """
            Aside from what is written below this is an alias to .intro_html

            Markdown automatically generates links.
            Markdown automatically generates <abbr> tags for wordlists (add-on).
            
            In the toolbox we now use popovers for <abbr> tags. 
            It looks pretty bad when these show up wrapped inside links..
            
            Preventing it from happening seems pretty hard so to hack around this issue I remove the 
            <abbr...><abbr> with regex magic.
            The pattern: (<a(?![a-z]).*?>.*?)<abbr.*>(.*)</abbr>(.*?</a>)
            
            It consists of multiple groups:
             1. (<a(?![a-z]).*?>.*?)
             x  <abbr.*>
             2. (.*)
             x  </abbr>
             3. (.*?</a>)
             
            1. Grabs the start of the anchor and it's contents up to the start of the <abbr> tag.
            x  <abbr.*> should be discarded
            2. Captures anything inside the <abbr> tag (that should not be lost).
            x  </abbr> is the end of the <abbr> tag and should be discarded
            3. Is the last bit of text before the anchor is closed, including the anchor's closing tag.
            
            Replacement string is simply all capturing groups combined.
            
            This should be cached because it may be CPU intensive but for testing if anyhing odd occurs
            this is left as an on-the-fly action.
             
        """
        return mark_safe(re.sub(r"(<a(?![a-z]).*?>.*?)<abbr.*>(.*)</abbr>(.*?</a>)", "\\1\\2\\3", self.intro_html, flags=re.MULTILINE))

    def intro_no_url(self):
        """ For intro texts there should be a anchor-less version as these are wrapped in anchors entirely
            This can be optimised for speed by caching the outcome in another model field.
            Pattern: </?(a|A)(?![a-zA-Z]).*?>
            Matching anything like "<a hre...", "<a>", "</a>" but nothing in between.
            Specifically not matching <abbr>, <address>, <applet> etc. ie. character after "a" in <a> is not a-z.
        """
        return mark_safe(re.sub(r'</?(a|A)(?![a-zA-Z]).*?>', '', self.intro_html, flags=re.MULTILINE))
    
    def dateformatted(self):
        """
            Format the date and time nicely
        """    
        return self.date.strftime('%d-%m-%Y om %H:%M')
    
    class Meta:
        """
            Change display of model in Django admin
        """ 
        app_label = "toolbox"
    
    def __unicode__(self):
        """
            String representation of the model
        """
        return self.title
