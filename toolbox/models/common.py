# -*- coding: utf-8 -*-
from django.db import models
from generic import GenericFields
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from filer.fields.image import FilerImageField
from filer.models.imagemodels import Image as FilerImage
from django.core.exceptions import ValidationError
import markdown
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
                                        verbose_name    = 'Gepubliceerd',
                                        auto_now        = True
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
                              
    published = models.BooleanField ( verbose_name   = "Publiseer" )

    str_intro_md = ""
    str_content_md = ""
    
    def process_inline_images(self,str_md):
        """
            Place filer images in markdown code
            
            FOR EVERY: ![Alt text][id] OR ![id]
            ADD      : [id]: url/to/image  "Optional title attribute"
            
            
            
            Pattern: /(?<!\\)\!(?:\[.*\])?\[([a-zA-Z0-9\-\+\_\.\ \]{4,200})\]/
            Finds what is between in the [id] block only, alt text is ignored.
            Alt text can contain anything except likebreaks.
            ID's can contain [ a-Z 0-9 - + _ . ] and space, min 4, max 200 tekens.    
            
        """

        # Items to be added..
        pat = re.compile(r'(?<!\\)\!(?:\[.*\])?\[([a-zA-Z0-9\-\+\_\.\ ]{4,200})\]')
        arr_images = re.findall(pat,str_md)
        str_img = ""
        errors = ""
        for image in arr_images:
            fi = FilerImage.objects.filter(name=image)
            if len(fi) > 0:
                str_img += "\n[%s]: %s  \"%s\"\n" % (image, fi.first().url, fi.first().default_caption) 
            else:
                errors += "No file found for %s.\n" % image
        if len(errors) > 0:
            raise ValidationError(errors.strip("\n"))
        else:
            return str_img 
        
    def clean(self):
        """
            Process inline images for markdown, check if thet exist or raise Exception.
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
        md = markdown.Markdown(extensions=['extra','nl2br','smarty', 'toc'],output_format='html5')
        self.intro_html = md.convert(self.str_intro_md).encode("utf-8")
        self.content_html = md.convert(self.str_content_md).encode("utf-8")
        
        super(CommonFields, self).save(*args, **kw)

    def content(self):
        """
            Simplify access to the actual content data..
        """
        return mark_safe(self.content_html)

    def intro(self):
        """
            Simplify access to the actual intro data..
        """
        return mark_safe(self.intro_html)    
    
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
    