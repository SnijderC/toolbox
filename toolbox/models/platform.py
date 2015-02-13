# -*- coding: utf-8 -*-
from django.db import models
from generic import GenericFields  

class Platform(GenericFields):
    
    name       = models.CharField(
                                   verbose_name        = 'Platform',
                                   max_length          = 60
                                 )
                                   
    vendor     = models.CharField(
                                   verbose_name        = 'Producent',
                                   max_length          = 60
                                 )
                                   
    icon       = models.CharField(
                                   verbose_name        = 'Font icon',
                                   blank               = True,
                                   max_length          = 32
                                 )
    
    class Meta:
        """
            Change display of model in Django admin
        """
        app_label = "toolbox"
        verbose_name = "Platform"
        verbose_name_plural = "Platformen"

    def __unicode__(self):
        """
            String representation of the model
        """
        return "%s (%s)" % (self.name, self.vendor)