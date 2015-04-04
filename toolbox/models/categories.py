# -*- coding: utf-8 -*-
from django.db import models
from generic import GenericFields  

class Category(GenericFields):
    
    name   = models.CharField(
                                verbose_name   = 'Categorie',
                                max_length=60
                            )
                            
    icon   = models.CharField(
                                verbose_name   = 'Font icon',
                                blank          = True,
                                max_length     = 32
                            )
                            
    show_in_sitemap = models.BooleanField(    
                                verbose_name   = 'In sitemap?',
                                default        = True
                            )
    
    class Meta:
        """
            Change display of model in Django admin
        """
        app_label = "toolbox"
        verbose_name = "Categorie"
        verbose_name_plural = "Categorieën"
    
    def __unicode__(self):
        """
            String representation of the model
        """
        return self.name