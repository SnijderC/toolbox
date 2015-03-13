# -*- coding: utf-8 -*-
from django.db import models
import markdown

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
        wordlist = "\n"
        for term_obj in Terms.objects.all():
            terms = term_obj.term.split(";")
            topics = self.term.split(";")
            for term in terms:
                if term not in topics:
                    wordlist += "*[%s]: %s\n" % (term, term_obj.description)
        
        md = markdown.Markdown(extensions=['extra','nl2br','smarty'],output_format='html5')
        self.description_html = md.convert(self.description+wordlist).encode("utf-8")
        
        super(Terms, self).save(*args, **kw)
        
        for model in ('Advice', 'Tool', 'FAQ'):
            model = models.get_model('toolbox', model)
            for item in model.objects.all():
                item.date = item.date                
                item.clean()
                item.save(skip_date_update=True)