# -*- coding: utf-8 -*-
from django.db import models
from generic import GenericFields
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from filer.fields.image import FilerImageField
from filer.models.imagemodels import Image as FilerImage
from django.core.exceptions import ValidationError
from terms import Terms
import datetime
import settings
import re

class CommonFields(GenericFields):

                                          
    title       = models.CharField   (
                                         verbose_name    = 'Titel',
                                         max_length      = 60
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
                                              
    content_md  = models.TextField   (   
                                         verbose_name    = 'Beschrijving',
                                         blank           = True
                                     )
                                     
    content_html= models.TextField  (   
                                         verbose_name    = 'Beschrijving',
                                         blank           = True,
                                         editable        = False
                                     )

    date        = models.DateTimeField (  
                                        verbose_name    = 'Laatste update'
                                     ) 
                                           
    user        = models.ForeignKey  (
                                        User,
                                        verbose_name    = 'Vrijwilliger'
                                     )
    
    credit      = models.CharField   (
                                        verbose_name    = 'Overschrijf credits',
                                        help_text       = 'Dit veld mag leeg blijven, indien je de credits onderaan het artikel wilt aanpassen vul je hier de naam/namen in.',
                                        blank           = True,
                                        default         = '',
                                        max_length      = 150
                                     )
                                                                           
    platforms   = models.ManyToManyField (  
                                        'Platform',
                                        verbose_name    = 'Platform (OS)',
                                        blank           = True
                                     )
                                     
    formfactors = models.ManyToManyField (  
                                        'Formfactor',
                                        verbose_name    = 'Formfactor',
                                        blank           = True
                                     )
                                     
    categories  = models.ManyToManyField ( 
                                       'Category',
                                       verbose_name     = 'Categorie/Tag',
                                       blank            = True
                                     )   
                                             

    image       = FilerImageField (
                                       related_name    = "%(class)s_image",
                                       on_delete       = models.SET_NULL,
                                       verbose_name    = 'Logo/Icoon',
                                       blank           = True,
                                       null            = True,
                                  )
                                  
    feature_score = models.PositiveSmallIntegerField (
                                         verbose_name    = 'Feature score',
                                         help_text       = "Bepaalt volgorde op de index pagina's. " +
                                                           "Gebruik zoveel mogelijk honderdtallen, " +
                                                           "indien noodzakelijk kan er dan een getal " +
                                                           "tussen de hondertallen gekozen worden om " +
                                                           "het item ergens tussenin te krijgen.",
                                         default         = 0
                                                      )
    topic         = models.CharField   (
                                         verbose_name    = 'Onderwerp (punt-komma gescheiden)',
                                         help_text       = 'Zet hierin woorden die je zelf uitlegt in het artikel, de woord verklaringsfunctie wordt voor deze woorden niet toegepast.',
                                         max_length      = 150,
                                         blank           = True,
                                     )

                              
    published = models.BooleanField ( verbose_name   = "Publiseer" )

    str_intro_md = ""
    str_content_md = ""
        
    def clean(self):
        """
            Process inline images for markdown, check if they exist or raise Exception.
        """
        try:
            self.str_content_md = self.content_md + self.process_inline_images(self.content_md)
            self.str_intro_md   = self.intro_md + self.process_inline_images(self.intro_md)
        except:
            raise

    def save(self, *args, **kw):
        """            
            Convert markdown to html to speed up the pageloading.
        """
        
        if not kw.pop('skip_date_update', False):
            self.date = datetime.datetime.now()
        
        self.content_html = self.cache_md(self.str_content_md)
        self.intro_html   = self.cache_md(self.str_intro_md)
        
        super(CommonFields, self).save(*args, **kw)

    def content(self):
        """
            Aside from what is written below this is an alias to .content_html

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
        return mark_safe(re.sub(r"(<a(?![a-z]).*?>.*?)<abbr.*>(.*)</abbr>(.*?</a>)", "\\1\\2\\3", self.content_html, flags=re.MULTILINE))

    def intro(self):
        """
            Simplify access to the actual intro data..
            For more info see self.content() comments.
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
    
    def contributor(self):
        """
            Get the full name of the Django user..
        """
        o_user = User.objects.get(pk=self.user)
        return "%s %s" % o_user.first_name, o_user.last_name

    def has_image(self):
        """
            Return true if there's an image related, false if not.
        """
        return self.image and "empty" not in self.image.name 
    
    def is_featured(self):
        """
            Determine whether the item is featured.
            
            Featured items have a feature_score > 0.
        """
        return (self.feature_score > 0)
    
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
        abstract = True
    
    def __unicode__(self):
        """
            String representation of the model
        """
        return self.title
    