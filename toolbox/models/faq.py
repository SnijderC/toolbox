# -*- coding: utf-8 -*-
from django.db import models
from terms import Terms
from toolbox.functions import fix_anchor_abbr
from helpers.tb_markdown import ToolboxMD


class FAQ(models.Model):

    question = models.CharField(
        verbose_name='Vraag',
        max_length=200
    )

    answer_md = models.TextField(
        verbose_name='Antwoord',
        blank=False
    )

    answer_html = models.TextField(
        verbose_name='Antwoord',
        editable=False,
        blank=True
    )

    categories = models.ManyToManyField(
        'FAQCategories',
        verbose_name=u'Categorieën',
        blank=True,
    )

    md = ToolboxMD(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.nl2br',
        'markdown.extensions.smarty'
    ])

    def __unicode__(self):
        """
            String representation of the model
        """
        return self.question

    def save(self, *args, **kw):

        self.answer_html = self.md.convert(self.answer_md)
        kw.pop("skip_date_update", False)
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

    slug = models.CharField(
        verbose_name='Slug',
        max_length=60,
        help_text="slug"
    )

    category = models.CharField(
        verbose_name='Categorie',
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
