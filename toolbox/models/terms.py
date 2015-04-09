# -*- coding: utf-8 -*-
from django.db import models
from helpers.tb_markdown import ToolboxMD

class Terms(models.Model):

    term                = models.CharField (
                                verbose_name   = 'Technische term',
                                max_length=120
                            )
                            
    description         = models.TextField (   
                                         verbose_name    = 'Omschrijving van de term',
                                         blank           = False
                            )
    description_html    = models.TextField (   
                                         verbose_name    = 'Omschrijving van de term',
                                         editable        = False,
                                         blank           = True
                            )

    # caching of wordlist must be switched off because after every save the list is changed.
    md = ToolboxMD(extensions=['extra','nl2br','smarty'],cached_wordlist=False)
    
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
        topics = self.term.split(";")        
        
        self.description_html = self.md.convert(self.description,topics)
        
        super(Terms, self).save(*args, **kw)
        
        for model in ('Advice', 'Tool', 'FAQ'):
            model = models.get_model('toolbox', model)
            for item in model.objects.all():
                if 'date' in item._meta.local_fields:
                    item.date = item.date                
                item.clean()
                item.save(skip_date_update=True)