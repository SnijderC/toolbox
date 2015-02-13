# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from common import CommonFields
  
class Advice(CommonFields):
    
    time = models.IntegerField (
                                verbose_name   = 'Takes (min.)',
                                blank          = True,
                                null           = True,
                            )
    
    related = models.ManyToManyField( 
                                       'self',  # m2m on myself, if you are my friend I'm yours..
                                       blank           = True,
                                       verbose_name    = 'Gerelateerd'
                                       ) 
                                   
    def i_am(self):
        """ 
            Return the name of the model.
        """
        return "advice"

    def url_slug(self):
        """
            Return the item type slug of the model.
        """
        return "adviezen"
    
    def time_formatted(self):
        """
            Calculate an amount of time in hours and minutes from minutes.
        """
        if self.time > 59:
            m = self.time % 60
            h = self.time / 60
            if m > 0:
                return "%d uur %d min." % (h , m)
            else:
                return "%d uur" % h
        else:
            return "%d min. " % self.time
    
    class Meta:
        """
            Change display of model in Django admin
        """
        app_label = "toolbox"
        verbose_name = "Advies"
        verbose_name_plural = "Adviezen"
    
    def __unicode__(self):
        """
            String representation of the model
        """
        return self.title
    