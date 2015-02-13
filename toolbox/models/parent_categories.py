# -*- coding: utf-8 -*-
from django.db import models

class ParentCategories(models.Model):

    name        = models.CharField (
                                verbose_name   = 'Hoofd Categorie',
                                max_length=60
                            )
                            
    icon        = models.CharField (
                                verbose_name   = 'Font icon',
                                blank          = True,
                                max_length     = 32
                            )
    
    categories  = models.ManyToManyField ( 
                                'Category',
                                verbose_name    = 'Subcategorie',
                                blank           = True,
                            )
    
    show_in_nav = models.BooleanField (    
                                verbose_name = 'In navbar?',
                                default      = True
                                     )
    show_in_sitemap = models.BooleanField (    
                                verbose_name = 'In sitemap?',
                                default      = True
                            )
    
    class Meta:
        """
            Change display of model in Django admin
        """
        app_label = "toolbox"
        verbose_name = "Hoofd Categorie"
        verbose_name_plural = "Hoofd Categorieën"
        
    def __unicode__(self):
        """
            String representation of the model
        """
        return self.name