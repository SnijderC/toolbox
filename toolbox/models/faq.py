# -*- coding: utf-8 -*-
from django.db import models
from terms import Terms
from toolbox.functions import fix_anchor_abbr
import markdown

class FAQ(models.Model):

    question            = models.CharField (
                                verbose_name   = 'Vraag',
                                max_length=200
                            )

    answer_md           = models.TextField (   
                                         verbose_name    = 'Antwoord',
                                         blank           = False
                            )

    answer_html         = models.TextField (   
                                         verbose_name    = 'Antwoord',
                                         editable        = False,
                                         blank           = True
                            ) 
    
    categories          = models.ManyToManyField ( 
                                'FAQCategories',
                                verbose_name    = u'Categorieën',
                                blank           = True,
                            )
    
    def __unicode__(self):
        """
            String representation of the model
        """
        return self.question
    
    def save(self, *args, **kw):        
        wordlist = "\n"
        for term_obj in Terms.objects.all():
            terms = term_obj.term.split(";")
            for term in terms:
                wordlist += "*[%s]: %s\n" % (term, term_obj.description)
        
        md = markdown.Markdown(extensions=['extra','nl2br','smarty'],output_format='html5')
        self.answer_html = fix_anchor_abbr(md.convert(self.answer_md+wordlist).encode("utf-8"))
        
        super(FAQ, self).save(*args, **kw)
    
    def answer(self):
        '''
            Just an alias to answer_html
        '''
        return self.answer_html
    
    class Meta:
        """
            Change display of model in Django admin
        """
        app_label = "toolbox"
        verbose_name = "FAQ (veel gestelde vragen)"
        verbose_name_plural = "FAQs"
        
class FAQCategories(models.Model):
    
    slug                = models.CharField   (     
                                         verbose_name    = 'Slug',
                                         max_length      = 60,
                                         help_text       = "slug"
                                     ) 
                                     
    category            = models.CharField (
                                verbose_name   = 'Categorie',
                                max_length=200
                            )
    def __unicode__(self):
        """
            String representation of the model
        """
        return self.category
        
    class Meta:
        """
            Change display of model in Django admin
        """
        app_label = "toolbox"
        verbose_name = "FAQ Categorie"
        verbose_name_plural = "FAQ Categorieën"
        