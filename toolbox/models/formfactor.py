# -*- coding: utf-8 -*-
from django.db import models
from generic import GenericFields 

class Formfactor(GenericFields):

    name        = models.CharField(
                                   verbose_name        = 'Formfactor',
                                   max_length          = 60
                                 )
                                   
    icon        = models.CharField(
                                   verbose_name        = 'Font icon',
                                   blank               = True,
                                   max_length          = 32
                                 )

    platforms   = models.ManyToManyField( 
                                   'Platform',
                                   verbose_name    = 'Platformen',
                                   blank           = True,
                                   null            = True,
                                 )

    show_in_sitemap = models.BooleanField(    
                                   verbose_name = 'In sitemap?',
                                   default      = True
                                         )
    
    class Meta:
        """
            Change display of model in Django admin
        """ 
        app_label = "toolbox"
        verbose_name = "Formfactor"
        verbose_name_plural = "Formfactors"

    def __unicode__(self):
        """
            String representation of the model
        """
        return "%s" % self.name