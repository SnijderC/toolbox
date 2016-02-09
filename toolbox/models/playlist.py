# -*- coding: utf-8 -*-
from django.db import models
from generic import GenericFields
from django.utils.safestring import mark_safe
from helpers.tb_markdown import ToolboxMD
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
                                                                                                                                                  
    published   = models.BooleanField   (
                                            verbose_name    = "Publiseer",
                                            default         = False,
                                        )

    playlist    = models.ManyToManyField ( 
                                       'Advice',
                                       verbose_name    = 'Playlist',
                                       blank           = True,
                                       through         = 'PlaylistOrder',
                                     )
    icon        = models.CharField(
                                   verbose_name        = 'Font icon',
                                   blank               = True,
                                   max_length          = 32
                                 )
 

    str_intro_md = ""
    
    md = ToolboxMD()
        
    def clean(self):
        """
            Process inline images for markdown, check if they exist or raise Exception.
        """
        try:
            self.str_intro_md = self.intro_md + self.md.process_inline_images(self.intro_md)
        except:
            raise

    def save(self, *args, **kw):
        """            
            Convert markdown to html to speed up the pageloading.
        """
        
        if not kw.pop('skip_date_update', False):
            self.date = datetime.datetime.now()
        
        self.intro_html = self.md.convert(self.str_intro_md)
        
        super(GenericFields, self).save(*args, **kw)

    def intro(self):
        """
            This is an alias to .intro_html.             
        """
        return mark_safe(self.intro_html)

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
    
    def i_am(self):
        return "playlist"
    
    def url_slug(self):
        """
            Return the item type slug of the model.
        """
        return "playlist"
    
    def has_image(self):
        """
            Return true if there's an image related, false if not.
        """
        return False 
    
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
