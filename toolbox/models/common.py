# -*- coding: utf-8 -*-
from django.db import models
from generic import GenericFields
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from filer.fields.image import FilerImageField
from helpers.tb_markdown import ToolboxMD
import datetime
import re


class CommonFields(GenericFields):

    title = models.CharField(
        verbose_name='Titel',
        max_length=60
    )

    intro_md = models.TextField(
        verbose_name='Intro',
        blank=True
    )

    intro_html = models.TextField(
        verbose_name='Intro',
        blank=True,
        editable=False
    )

    content_md = models.TextField(
        verbose_name='Beschrijving',
        blank=True
    )

    content_html = models.TextField(
        verbose_name='Beschrijving',
        blank=True,
        editable=False
    )

    date = models.DateTimeField(
        verbose_name='Laatste update'
    )

    creationdate = models.DateTimeField(
        verbose_name='Toegevoegd',
        auto_now_add=True
    )

    user = models.ForeignKey(
        User,
        verbose_name='Vrijwilliger',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    credit = models.CharField(
        verbose_name='Overschrijf credits',
        help_text='Dit veld mag leeg blijven, indien je de credits onderaan het artikel wilt aanpassen vul je hier de naam/namen in.',
        blank=True,
        default='',
        max_length=150
    )

    platforms = models.ManyToManyField(
        'Platform',
        verbose_name='Platform (OS)',
        blank=True
    )

    formfactors = models.ManyToManyField(
        'Formfactor',
        verbose_name='Formfactor',
        blank=True
    )

    categories = models.ManyToManyField(
        'Category',
        verbose_name='Categorie/Tag',
        blank=True
    )

    image = FilerImageField(
        related_name="%(class)s_image",
        verbose_name='Logo/Icoon',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    feature_score = models.PositiveSmallIntegerField(
        verbose_name='Feature score',
        help_text="Bepaalt volgorde op de index pagina's. " +
        "Gebruik zoveel mogelijk honderdtallen, " +
        "indien noodzakelijk kan er dan een getal " +
        "tussen de hondertallen gekozen worden om " +
        "het item ergens tussenin te krijgen.",
        default=0
    )
    topic = models.CharField(
        verbose_name='Onderwerp (punt-komma gescheiden)',
        help_text='Zet hierin woorden die je zelf uitlegt in het artikel, de woord verklaringsfunctie wordt voor deze woorden niet toegepast.',
        max_length=150,
        blank=True,
    )

    published = models.BooleanField(
        verbose_name="Publiseer",
        default=False,
    )

    str_intro_md = ""
    str_content_md = ""
    md = ToolboxMD()

    def clean(self):
        """
            Process inline images for markdown, check if they exist or raise
            Exception.
        """
        try:
            self.str_content_md = self.content_md + \
                self.md.process_inline_images(self.content_md)
            self.str_intro_md = self.intro_md + \
                self.md.process_inline_images(self.intro_md)
        except:
            raise

    def save(self, *args, **kw):
        """
            Convert markdown to html to speed up the pageloading.
        """

        if not kw.pop('skip_date_update', False):
            self.date = datetime.datetime.now()

        topics = self.topic.split(";")

        self.content_html = self.md.convert(self.str_content_md, topics)
        self.intro_html = self.md.convert(self.str_intro_md, topics)

        super(CommonFields, self).save(*args, **kw)

    def content(self):
        """
            This is an alias to .content_html
        """
        return mark_safe(self.content_html)

    def intro(self):
        """
            This is an alias to .intro_html
        """
        return mark_safe(self.intro_html)

    def intro_no_url(self):
        """
            For intro texts there should be a anchor-less version as these are
            wrapped in anchors entirely. This can be optimised for speed by
            caching the outcome in another model field.
            Pattern: </?(a|A)(?![a-zA-Z]).*?>
            Matching anything like "<a hre...", "<a>", "</a>" but nothing in
            between.
            Specifically not matching <abbr>, <address>, <applet> etc.
            ie. character after "a" in <a> is not a-z.
        """
        return mark_safe(re.sub(
                r'</?(a|A)(?![a-zA-Z]).*?>',
                '',
                self.intro_html,
                flags=re.MULTILINE
            ))

    def contributor(self):
        """
            Get the full name of the Django user..
        """
        o_user = User.objects.get(pk=self.user)
        return "%s %s" % o_user.first_name, o_user.last_name

    def has_image(self):
        """
            Return true if there's an image related, false if not.
        """
        return self.image and "empty" not in self.image.name

    def is_featured(self):
        """
            Determine whether the item is featured.

            Featured items have a feature_score > 0.
        """
        return (self.feature_score > 0)

    def dateformatted(self):
        """
            Format the date and time nicely
        """
        return self.creationdate.strftime('%d-%m-%Y om %H:%M')

    def meta_datemodified(self):
        """
            Format the date and time nicely
        """
        return self.date.strftime('%Y-%d-m %H:%M:%S')

    def meta_date(self):
        """
            Format the date and time nicely
        """
        return self.creationdate.strftime('%Y-%d-m %H:%M:%S')

    class Meta:

        """
            Change display of model in Django admin
        """
        app_label = "toolbox"
        abstract = True

    def __unicode__(self):
        """
            String representation of the model
        """
        return self.title
