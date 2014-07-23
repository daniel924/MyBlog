# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'blogengine_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=40, unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'blogengine', ['Category'])

        # Adding model 'Tag'
        db.create_table(u'blogengine_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=40, unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'blogengine', ['Tag'])

        # Adding model 'Post'
        db.create_table(u'blogengine_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blogengine.Category'], null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=40, unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'blogengine', ['Post'])

        # Adding M2M table for field tags on 'Post'
        m2m_table_name = db.shorten_name(u'blogengine_post_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm[u'blogengine.post'], null=False)),
            ('tag', models.ForeignKey(orm[u'blogengine.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['post_id', 'tag_id'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'blogengine_category')

        # Deleting model 'Tag'
        db.delete_table(u'blogengine_tag')

        # Deleting model 'Post'
        db.delete_table(u'blogengine_post')

        # Removing M2M table for field tags on 'Post'
        db.delete_table(db.shorten_name(u'blogengine_post_tags'))


    models = {
        u'blogengine.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '40', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'blogengine.post': {
            'Meta': {'ordering': "['-pub_date']", 'object_name': 'Post'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blogengine.Category']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '40', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['blogengine.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'blogengine.tag': {
            'Meta': {'object_name': 'Tag'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '40', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['blogengine']