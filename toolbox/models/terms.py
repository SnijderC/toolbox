# -*- coding: utf-8 -*-
from django.db import models


class Terms(models.Model):

    term        = models.CharField (
                                verbose_name   = 'Technische term',
                                max_length=120
                            )
                            
    description = models.TextField (   
                                         verbose_name    = 'Omschrijving van de term',
                                         blank           = False
                            )

    
    class Meta:
        """
            Change display of model in Django admin
        """
        app_label = "toolbox"
        verbose_name = "Verklarende woordenlijst"
        verbose_name_plural = "Verklarende woordenlijst"
        
    def __unicode__(self):
        """
            String representation of the model
        """
        return self.term
    
    def save(self, *args, **kw):
        super(Terms, self).save(*args, **kw)
        for model in ('Advice', 'Tool'):
            model = models.get_model('toolbox', model)
            for item in model.objects.all():
                item.date = item.date                
                item.save(skip_date_update=True)