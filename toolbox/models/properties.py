# -*- coding: utf-8 -*-
from django.db import models
from generic import GenericFields


class Property(GenericFields):

    title = models.CharField(
        verbose_name='Titel',
        max_length=60
    )

    intro = models.TextField(
        verbose_name='Intro',
        blank=True
    )

    icon = models.CharField(
        verbose_name='Font icon',
        blank=True,
        max_length=32
    )

    is_good = models.BooleanField(

        verbose_name='Goede eigenschap?',
        help_text='Bepaalt of het item in de "Voordelen" lijst te selecteren is.',
        default=False,
    )

    is_bad = models.BooleanField(

        verbose_name='Slechte eigenschap?',
        help_text='Bepaalt of het item in de "Nadelen" lijst te selecteren is.',
        default=False,
    )

    class Meta:

        """
            Change display of model in Django admin
        """
        app_label = "toolbox"
        verbose_name = "Eigenschap"
        verbose_name_plural = "Eigenschappen"

    def __unicode__(self):
        """
            String representation of the model
        """
        return self.title
