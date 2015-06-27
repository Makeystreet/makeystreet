# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SendMail'
        db.create_table(u'core_sendmail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('to', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('cc', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('from_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('to_name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('sent_time', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('mail_type', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('core', ['SendMail'])


    def backwards(self, orm):
        # Deleting model 'SendMail'
        db.delete_table(u'core_sendmail')


    models = {
        'core.sendmail': {
            'Meta': {'object_name': 'SendMail'},
            'cc': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'from_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail_type': ('django.db.models.fields.IntegerField', [], {}),
            'sent_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'to': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'to_name': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['core']