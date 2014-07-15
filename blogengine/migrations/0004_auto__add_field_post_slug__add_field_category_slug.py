# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Post.slug'
        db.add_column(u'blogengine_post', 'slug',
                      self.gf('django.db.models.fields.SlugField')(max_length=40, unique=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.slug'
        db.add_column(u'blogengine_category', 'slug',
                      self.gf('django.db.models.fields.SlugField')(max_length=40, unique=True, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Post.slug'
        db.delete_column(u'blogengine_post', 'slug')

        # Deleting field 'Category.slug'
        db.delete_column(u'blogengine_category', 'slug')


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
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['blogengine']