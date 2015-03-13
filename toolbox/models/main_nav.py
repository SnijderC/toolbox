# -*- coding: utf-8 -*-
from django.db import models

class MainNav(models.Model):

    name        = models.CharField (
                                verbose_name   = 'Menu onderdeel',
                                max_length=60
                            )
                            
    icon        = models.CharField (
                                verbose_name   = 'Font icon',
                                blank          = True,
                                max_length     = 32
                            )
    
    categories = models.ManyToManyField ( 
                               'ParentCategories',
                               verbose_name    = u'Hoofd categorieën',
                               blank           = True,
                             )

    publish    = models.BooleanField(    
                               verbose_name = 'In navbar?',
                               default      = False
                                     )
    
    class Meta:
        """
            Change display of model in Django admin
        """
        app_label = "toolbox"
        verbose_name = "Menu onderdeel"
        verbose_name_plural = "Menu onderdelen"
        
    def __unicode__(self):
        """
            String representation of the model
        """
        return self.name