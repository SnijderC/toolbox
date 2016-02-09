# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import filer.fields.image
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0002_auto_20150606_2003'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Advice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(help_text=b'slug', max_length=60, verbose_name=b'Slug')),
                ('title', models.CharField(max_length=60, verbose_name=b'Titel')),
                ('intro_md', models.TextField(verbose_name=b'Intro', blank=True)),
                ('intro_html', models.TextField(verbose_name=b'Intro', editable=False, blank=True)),
                ('content_md', models.TextField(verbose_name=b'Beschrijving', blank=True)),
                ('content_html', models.TextField(verbose_name=b'Beschrijving', editable=False, blank=True)),
                ('date', models.DateTimeField(verbose_name=b'Laatste update')),
                ('creationdate', models.DateTimeField(auto_now_add=True, verbose_name=b'Toegevoegd')),
                ('credit', models.CharField(default=b'', help_text=b'Dit veld mag leeg blijven, indien je de credits onderaan het artikel wilt aanpassen vul je hier de naam/namen in.', max_length=150, verbose_name=b'Overschrijf credits', blank=True)),
                ('feature_score', models.PositiveSmallIntegerField(default=0, help_text=b"Bepaalt volgorde op de index pagina's. Gebruik zoveel mogelijk honderdtallen, indien noodzakelijk kan er dan een getal tussen de hondertallen gekozen worden om het item ergens tussenin te krijgen.", verbose_name=b'Feature score')),
                ('topic', models.CharField(help_text=b'Zet hierin woorden die je zelf uitlegt in het artikel, de woord verklaringsfunctie wordt voor deze woorden niet toegepast.', max_length=150, verbose_name=b'Onderwerp (punt-komma gescheiden)', blank=True)),
                ('published', models.BooleanField(verbose_name=b'Publiseer')),
                ('time', models.IntegerField(null=True, verbose_name=b'Takes (min.)', blank=True)),
            ],
            options={
                'verbose_name': 'Advies',
                'verbose_name_plural': 'Adviezen',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(help_text=b'slug', max_length=60, verbose_name=b'Slug')),
                ('name', models.CharField(max_length=60, verbose_name=b'Categorie')),
                ('icon', models.CharField(max_length=32, verbose_name=b'Font icon', blank=True)),
                ('show_in_sitemap', models.BooleanField(default=True, verbose_name=b'In sitemap?')),
            ],
            options={
                'verbose_name': 'Categorie',
                'verbose_name_plural': 'Categorie\xebn',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.CharField(max_length=200, verbose_name=b'Vraag')),
                ('answer_md', models.TextField(verbose_name=b'Antwoord')),
                ('answer_html', models.TextField(verbose_name=b'Antwoord', editable=False, blank=True)),
            ],
            options={
                'verbose_name': 'FAQ (veel gestelde vragen)',
                'verbose_name_plural': 'FAQs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FAQCategories',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(help_text=b'slug', max_length=60, verbose_name=b'Slug')),
                ('category', models.CharField(max_length=200, verbose_name=b'Categorie')),
            ],
            options={
                'verbose_name': 'FAQ Categorie',
                'verbose_name_plural': 'FAQ Categorie\xebn',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Formfactor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(help_text=b'slug', max_length=60, verbose_name=b'Slug')),
                ('name', models.CharField(max_length=60, verbose_name=b'Formfactor')),
                ('icon', models.CharField(max_length=32, verbose_name=b'Font icon', blank=True)),
                ('show_in_sitemap', models.BooleanField(default=True, verbose_name=b'In sitemap?')),
            ],
            options={
                'verbose_name': 'Formfactor',
                'verbose_name_plural': 'Formfactors',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(help_text=b'slug', max_length=60, verbose_name=b'Slug')),
                ('name', models.CharField(max_length=60, verbose_name=b'Naam')),
                ('license_md', models.TextField(verbose_name=b'Beschrijving', blank=True)),
                ('license_html', models.TextField(verbose_name=b'Beschrijving', editable=False, blank=True)),
                ('icon', models.CharField(max_length=32, verbose_name=b'Font icon', blank=True)),
                ('open_source', models.BooleanField(default=False, verbose_name=b'Open Source?')),
            ],
            options={
                'verbose_name': 'Licentie',
                'verbose_name_plural': 'Licenties',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Manual',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(help_text=b'slug', max_length=60, verbose_name=b'Slug')),
                ('title', models.CharField(max_length=60, verbose_name=b'Titel')),
                ('intro_md', models.TextField(verbose_name=b'Intro', blank=True)),
                ('intro_html', models.TextField(verbose_name=b'Intro', editable=False, blank=True)),
                ('content_md', models.TextField(verbose_name=b'Beschrijving', blank=True)),
                ('content_html', models.TextField(verbose_name=b'Beschrijving', editable=False, blank=True)),
                ('date', models.DateTimeField(verbose_name=b'Laatste update')),
                ('creationdate', models.DateTimeField(auto_now_add=True, verbose_name=b'Toegevoegd')),
                ('credit', models.CharField(default=b'', help_text=b'Dit veld mag leeg blijven, indien je de credits onderaan het artikel wilt aanpassen vul je hier de naam/namen in.', max_length=150, verbose_name=b'Overschrijf credits', blank=True)),
                ('feature_score', models.PositiveSmallIntegerField(default=0, help_text=b"Bepaalt volgorde op de index pagina's. Gebruik zoveel mogelijk honderdtallen, indien noodzakelijk kan er dan een getal tussen de hondertallen gekozen worden om het item ergens tussenin te krijgen.", verbose_name=b'Feature score')),
                ('topic', models.CharField(help_text=b'Zet hierin woorden die je zelf uitlegt in het artikel, de woord verklaringsfunctie wordt voor deze woorden niet toegepast.', max_length=150, verbose_name=b'Onderwerp (punt-komma gescheiden)', blank=True)),
                ('published', models.BooleanField(verbose_name=b'Publiseer')),
                ('categories', models.ManyToManyField(to='toolbox.Category', verbose_name=b'Categorie/Tag', blank=True)),
                ('formfactors', models.ManyToManyField(to='toolbox.Formfactor', verbose_name=b'Formfactor', blank=True)),
                ('image', filer.fields.image.FilerImageField(related_name='manual_image', on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'Logo/Icoon', blank=True, to='filer.Image', null=True)),
            ],
            options={
                'verbose_name': 'Handleiding',
                'verbose_name_plural': 'Handleidingen',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ParentCategories',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name=b'Hoofd Categorie')),
                ('icon', models.CharField(max_length=32, verbose_name=b'Font icon', blank=True)),
                ('show_in_sitemap', models.BooleanField(default=True, verbose_name=b'In sitemap?')),
                ('categories', models.ManyToManyField(to='toolbox.Category', verbose_name=b'Subcategorie', blank=True)),
            ],
            options={
                'verbose_name': 'Hoofd Categorie',
                'verbose_name_plural': 'Hoofd Categorie\xebn',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(help_text=b'slug', max_length=60, verbose_name=b'Slug')),
                ('name', models.CharField(max_length=60, verbose_name=b'Platform')),
                ('vendor', models.CharField(max_length=60, verbose_name=b'Producent')),
                ('icon', models.CharField(max_length=32, verbose_name=b'Font icon', blank=True)),
            ],
            options={
                'verbose_name': 'Platform',
                'verbose_name_plural': 'Platformen',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(help_text=b'slug', max_length=60, verbose_name=b'Slug')),
                ('title', models.CharField(max_length=60, verbose_name=b'Titel')),
                ('i_want_to', models.CharField(help_text=b'Ik wil mijn data beschermen', max_length=120, verbose_name=b'Doel')),
                ('intro_md', models.TextField(verbose_name=b'Intro', blank=True)),
                ('intro_html', models.TextField(verbose_name=b'Intro', editable=False, blank=True)),
                ('date', models.DateTimeField(verbose_name=b'Laatste update')),
                ('published', models.BooleanField(verbose_name=b'Publiseer')),
                ('icon', models.CharField(max_length=32, verbose_name=b'Font icon', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlaylistOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(verbose_name=b'Volgorde')),
                ('advice', models.ForeignKey(to='toolbox.Advice')),
                ('playlist', models.ForeignKey(to='toolbox.Playlist')),
            ],
            options={
                'verbose_name': 'Playlist inhoud',
                'verbose_name_plural': 'Inhoud playlists',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(help_text=b'slug', max_length=60, verbose_name=b'Slug')),
                ('title', models.CharField(max_length=60, verbose_name=b'Titel')),
                ('intro', models.TextField(verbose_name=b'Intro', blank=True)),
                ('icon', models.CharField(max_length=32, verbose_name=b'Font icon', blank=True)),
                ('is_good', models.BooleanField(help_text=b'Bepaalt of het item in de "Voordelen" lijst te selecteren is.', verbose_name=b'Goede eigenschap?')),
                ('is_bad', models.BooleanField(help_text=b'Bepaalt of het item in de "Nadelen" lijst te selecteren is.', verbose_name=b'Slechte eigenschap?')),
            ],
            options={
                'verbose_name': 'Eigenschap',
                'verbose_name_plural': 'Eigenschappen',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Terms',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('term', models.CharField(max_length=120, verbose_name=b'Technische term')),
                ('description', models.TextField(verbose_name=b'Omschrijving van de term')),
                ('description_html', models.TextField(verbose_name=b'Omschrijving van de term', editable=False, blank=True)),
            ],
            options={
                'verbose_name': 'Verklarende woordenlijst',
                'verbose_name_plural': 'Verklarende woordenlijst',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(help_text=b'slug', max_length=60, verbose_name=b'Slug')),
                ('title', models.CharField(max_length=60, verbose_name=b'Titel')),
                ('intro_md', models.TextField(verbose_name=b'Intro', blank=True)),
                ('intro_html', models.TextField(verbose_name=b'Intro', editable=False, blank=True)),
                ('content_md', models.TextField(verbose_name=b'Beschrijving', blank=True)),
                ('content_html', models.TextField(verbose_name=b'Beschrijving', editable=False, blank=True)),
                ('date', models.DateTimeField(verbose_name=b'Laatste update')),
                ('creationdate', models.DateTimeField(auto_now_add=True, verbose_name=b'Toegevoegd')),
                ('credit', models.CharField(default=b'', help_text=b'Dit veld mag leeg blijven, indien je de credits onderaan het artikel wilt aanpassen vul je hier de naam/namen in.', max_length=150, verbose_name=b'Overschrijf credits', blank=True)),
                ('feature_score', models.PositiveSmallIntegerField(default=0, help_text=b"Bepaalt volgorde op de index pagina's. Gebruik zoveel mogelijk honderdtallen, indien noodzakelijk kan er dan een getal tussen de hondertallen gekozen worden om het item ergens tussenin te krijgen.", verbose_name=b'Feature score')),
                ('topic', models.CharField(help_text=b'Zet hierin woorden die je zelf uitlegt in het artikel, de woord verklaringsfunctie wordt voor deze woorden niet toegepast.', max_length=150, verbose_name=b'Onderwerp (punt-komma gescheiden)', blank=True)),
                ('published', models.BooleanField(verbose_name=b'Publiseer')),
                ('cost', models.CharField(max_length=40, verbose_name=b'Prijs', blank=True)),
                ('url', models.CharField(max_length=2000, verbose_name=b'Website', blank=True)),
                ('author', models.CharField(max_length=40, verbose_name=b'Auteur', blank=True)),
                ('author_url', models.CharField(max_length=2000, verbose_name=b'Website auteur', blank=True)),
                ('risk', models.CharField(blank=True, max_length=1, verbose_name=b'Privacy inbreuk risico', choices=[(b'L', b'Laag'), (b'V', b'Wees voorzichtig'), (b'H', b'Hoog')])),
            ],
            options={
                'verbose_name': 'Tools',
                'verbose_name_plural': 'Tools',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('tool_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='toolbox.Tool')),
            ],
            options={
                'verbose_name': 'Diensten',
                'verbose_name_plural': 'Diensten',
            },
            bases=('toolbox.tool',),
        ),
        migrations.CreateModel(
            name='App',
            fields=[
                ('tool_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='toolbox.Tool')),
                ('playstore', models.CharField(help_text=b'Vul het id in, niet een link dus: com.google.android.apps.maps', max_length=150, verbose_name=b'Playstore id', blank=True)),
                ('appstore', models.CharField(help_text=b'Vul het id in, niet een link dus: googlemaps', max_length=150, verbose_name=b'Appstore', blank=True)),
                ('marketplace', models.CharField(help_text=b'Vul het id in, niet een link dus: c14e93aa-27d7-df11-a844-00237de2db9e', max_length=150, verbose_name=b'Marketplace', blank=True)),
            ],
            options={
                'verbose_name': 'Tools',
                'verbose_name_plural': 'Tools',
            },
            bases=('toolbox.tool',),
        ),
        migrations.AddField(
            model_name='tool',
            name='alternative',
            field=models.ManyToManyField(related_name='alternative_rel_+', verbose_name=b'Alternatief', to='toolbox.Tool', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tool',
            name='categories',
            field=models.ManyToManyField(to='toolbox.Category', verbose_name=b'Categorie/Tag', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tool',
            name='cons',
            field=models.ManyToManyField(related_name='tool_cons', verbose_name=b'Nadeel', to='toolbox.Property', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tool',
            name='formfactors',
            field=models.ManyToManyField(to='toolbox.Formfactor', verbose_name=b'Formfactor', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tool',
            name='image',
            field=filer.fields.image.FilerImageField(related_name='tool_image', on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'Logo/Icoon', blank=True, to='filer.Image', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tool',
            name='license',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='toolbox.License', null=True, verbose_name=b'Licentie'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tool',
            name='platforms',
            field=models.ManyToManyField(to='toolbox.Platform', verbose_name=b'Platform (OS)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tool',
            name='pros',
            field=models.ManyToManyField(related_name='tool_pros', verbose_name=b'Voordeel', to='toolbox.Property', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tool',
            name='user',
            field=models.ForeignKey(verbose_name=b'Vrijwilliger', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='playlist',
            name='playlist',
            field=models.ManyToManyField(to='toolbox.Advice', verbose_name=b'Playlist', through='toolbox.PlaylistOrder', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='manual',
            name='platforms',
            field=models.ManyToManyField(to='toolbox.Platform', verbose_name=b'Platform (OS)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='manual',
            name='user',
            field=models.ForeignKey(verbose_name=b'Vrijwilliger', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='formfactor',
            name='platforms',
            field=models.ManyToManyField(to='toolbox.Platform', null=True, verbose_name=b'Platformen', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='faq',
            name='categories',
            field=models.ManyToManyField(to='toolbox.FAQCategories', verbose_name='Categorie\xebn', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advice',
            name='categories',
            field=models.ManyToManyField(to='toolbox.Category', verbose_name=b'Categorie/Tag', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advice',
            name='formfactors',
            field=models.ManyToManyField(to='toolbox.Formfactor', verbose_name=b'Formfactor', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advice',
            name='image',
            field=filer.fields.image.FilerImageField(related_name='advice_image', on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'Logo/Icoon', blank=True, to='filer.Image', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advice',
            name='platforms',
            field=models.ManyToManyField(to='toolbox.Platform', verbose_name=b'Platform (OS)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advice',
            name='related',
            field=models.ManyToManyField(related_name='related_rel_+', verbose_name=b'Gerelateerd', to='toolbox.Advice', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advice',
            name='user',
            field=models.ForeignKey(verbose_name=b'Vrijwilliger', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
