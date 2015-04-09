# -*- coding: utf-8 -*-
from django.db import models
import re

class GenericFields(models.Model):


    slug        = models.CharField   (     
                                         verbose_name    = 'Slug',
                                         max_length      = 60,
                                         help_text       = "slug"
                                     )

    def save(self, *args, **kw):
        #make slug..
        self.slug = re.sub("[^a-zA-Z0-9\-]","-",self.slug).strip("-").lower()
        
        super(GenericFields, self).save(*args, **kw)
   
    class Meta:
        """
            Change display of model in Django admin
        """ 
        app_label = "toolbox"
        abstract = True