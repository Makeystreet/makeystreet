# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'SendMail.actor_id'
        db.add_column(u'core_sendmail', 'actor_id',
                      self.gf('django.db.models.fields.IntegerField')(default=76),
                      keep_default=False)

        # Adding field 'SendMail.target_id'
        db.add_column(u'core_sendmail', 'target_id',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'SendMail.actor_id'
        db.delete_column(u'core_sendmail', 'actor_id')

        # Deleting field 'SendMail.target_id'
        db.delete_column(u'core_sendmail', 'target_id')


    models = {
        'core.sendmail': {
            'Meta': {'object_name': 'SendMail'},
            'actor_id': ('django.db.models.fields.IntegerField', [], {}),
            'cc': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'from_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail_type': ('django.db.models.fields.IntegerField', [], {}),
            'sent_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'target_id': ('django.db.models.fields.IntegerField', [], {}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'to': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'to_name': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['core']