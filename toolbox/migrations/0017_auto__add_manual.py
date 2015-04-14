# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Manual'
        db.create_table(u'toolbox_manual', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('intro_md', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('intro_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('content_md', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('content_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('credit', self.gf('django.db.models.fields.CharField')(default='', max_length=150, blank=True)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='manual_image', null=True, on_delete=models.SET_NULL, to=orm['filer.Image'])),
            ('feature_score', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('topic', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal('toolbox', ['Manual'])

        # Adding M2M table for field platforms on 'Manual'
        m2m_table_name = db.shorten_name(u'toolbox_manual_platforms')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('manual', models.ForeignKey(orm['toolbox.manual'], null=False)),
            ('platform', models.ForeignKey(orm['toolbox.platform'], null=False))
        ))
        db.create_unique(m2m_table_name, ['manual_id', 'platform_id'])

        # Adding M2M table for field formfactors on 'Manual'
        m2m_table_name = db.shorten_name(u'toolbox_manual_formfactors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('manual', models.ForeignKey(orm['toolbox.manual'], null=False)),
            ('formfactor', models.ForeignKey(orm['toolbox.formfactor'], null=False))
        ))
        db.create_unique(m2m_table_name, ['manual_id', 'formfactor_id'])

        # Adding M2M table for field categories on 'Manual'
        m2m_table_name = db.shorten_name(u'toolbox_manual_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('manual', models.ForeignKey(orm['toolbox.manual'], null=False)),
            ('category', models.ForeignKey(orm['toolbox.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['manual_id', 'category_id'])


    def backwards(self, orm):
        # Deleting model 'Manual'
        db.delete_table(u'toolbox_manual')

        # Removing M2M table for field platforms on 'Manual'
        db.delete_table(db.shorten_name(u'toolbox_manual_platforms'))

        # Removing M2M table for field formfactors on 'Manual'
        db.delete_table(db.shorten_name(u'toolbox_manual_formfactors'))

        # Removing M2M table for field categories on 'Manual'
        db.delete_table(db.shorten_name(u'toolbox_manual_categories'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'filer.file': {
            'Meta': {'object_name': 'File'},
            '_file_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'all_files'", 'null': 'True', 'to': "orm['filer.Folder']"}),
            'has_all_mandatory_data': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'original_filename': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'owned_files'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_filer.file_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'sha1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40', 'blank': 'True'}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'filer.folder': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('parent', 'name'),)", 'object_name': 'Folder'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'filer_owned_folders'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['filer.Folder']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'filer.image': {
            'Meta': {'object_name': 'Image', '_ormbases': ['filer.File']},
            '_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            '_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'default_alt_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'default_caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'file_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['filer.File']", 'unique': 'True', 'primary_key': 'True'}),
            'must_always_publish_author_credit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'must_always_publish_copyright': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subject_location': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        'toolbox.advice': {
            'Meta': {'object_name': 'Advice'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['toolbox.Category']", 'symmetrical': 'False', 'blank': 'True'}),
            'content_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_md': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'credit': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'feature_score': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'formfactors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['toolbox.Formfactor']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'advice_image'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['filer.Image']"}),
            'intro_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'intro_md': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'platforms': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['toolbox.Platform']", 'symmetrical': 'False', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {}),
            'related': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_rel_+'", 'blank': 'True', 'to': "orm['toolbox.Advice']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'time': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'toolbox.app': {
            'Meta': {'object_name': 'App', '_ormbases': ['toolbox.Tool']},
            'appstore': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'marketplace': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'playstore': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            u'tool_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['toolbox.Tool']", 'unique': 'True', 'primary_key': 'True'})
        },
        'toolbox.category': {
            'Meta': {'object_name': 'Category'},
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'show_in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'toolbox.faq': {
            'Meta': {'object_name': 'FAQ'},
            'answer_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'answer_md': ('django.db.models.fields.TextField', [], {}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['toolbox.FAQCategories']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'toolbox.faqcategories': {
            'Meta': {'object_name': 'FAQCategories'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'toolbox.formfactor': {
            'Meta': {'object_name': 'Formfactor'},
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'platforms': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['toolbox.Platform']", 'null': 'True', 'blank': 'True'}),
            'show_in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'toolbox.license': {
            'Meta': {'object_name': 'License'},
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'license_md': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'open_source': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'toolbox.manual': {
            'Meta': {'object_name': 'Manual'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['toolbox.Category']", 'symmetrical': 'False', 'blank': 'True'}),
            'content_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_md': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'credit': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'feature_score': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'formfactors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['toolbox.Formfactor']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'manual_image'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['filer.Image']"}),
            'intro_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'intro_md': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'platforms': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['toolbox.Platform']", 'symmetrical': 'False', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'toolbox.parentcategories': {
            'Meta': {'object_name': 'ParentCategories'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['toolbox.Category']", 'symmetrical': 'False', 'blank': 'True'}),
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'show_in_sitemap': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'toolbox.platform': {
            'Meta': {'object_name': 'Platform'},
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'vendor': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'toolbox.playlist': {
            'Meta': {'object_name': 'Playlist'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'i_want_to': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'intro_md': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'playlist': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['toolbox.Advice']", 'symmetrical': 'False', 'through': "orm['toolbox.PlaylistOrder']", 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'toolbox.playlistorder': {
            'Meta': {'object_name': 'PlaylistOrder'},
            'advice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['toolbox.Advice']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'playlist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['toolbox.Playlist']"})
        },
        'toolbox.property': {
            'Meta': {'object_name': 'Property'},
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'is_bad': ('django.db.models.fields.BooleanField', [], {}),
            'is_good': ('django.db.models.fields.BooleanField', [], {}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'toolbox.service': {
            'Meta': {'object_name': 'Service', '_ormbases': ['toolbox.Tool']},
            u'tool_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['toolbox.Tool']", 'unique': 'True', 'primary_key': 'True'})
        },
        'toolbox.terms': {
            'Meta': {'object_name': 'Terms'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'description_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        'toolbox.tool': {
            'Meta': {'object_name': 'Tool'},
            'alternative': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'alternative_rel_+'", 'blank': 'True', 'to': "orm['toolbox.Tool']"}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'author_url': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['toolbox.Category']", 'symmetrical': 'False', 'blank': 'True'}),
            'cons': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'tool_cons'", 'blank': 'True', 'to': "orm['toolbox.Property']"}),
            'content_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_md': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'cost': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'credit': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '150', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'feature_score': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'formfactors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['toolbox.Formfactor']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tool_image'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['filer.Image']"}),
            'intro_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'intro_md': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['toolbox.License']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'platforms': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['toolbox.Platform']", 'symmetrical': 'False', 'blank': 'True'}),
            'pros': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'tool_pros'", 'blank': 'True', 'to': "orm['toolbox.Property']"}),
            'published': ('django.db.models.fields.BooleanField', [], {}),
            'risk': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['toolbox']