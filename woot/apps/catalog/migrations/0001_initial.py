# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Makey'
        db.create_table(u'catalog_makey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_facebook.FacebookCustomUser'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('added_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'catalog', ['Makey'])

        # Adding model 'Tutorial'
        db.create_table(u'catalog_tutorial', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_facebook.FacebookCustomUser'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('added_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'catalog', ['Tutorial'])

        # Adding model 'Product'
        db.create_table(u'catalog_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sku', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('added_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'catalog', ['Product'])

        # Adding M2M table for field makeys on 'Product'
        m2m_table_name = db.shorten_name(u'catalog_product_makeys')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm[u'catalog.product'], null=False)),
            ('makey', models.ForeignKey(orm[u'catalog.makey'], null=False))
        ))
        db.create_unique(m2m_table_name, ['product_id', 'makey_id'])

        # Adding M2M table for field tutorials on 'Product'
        m2m_table_name = db.shorten_name(u'catalog_product_tutorials')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm[u'catalog.product'], null=False)),
            ('tutorial', models.ForeignKey(orm[u'catalog.tutorial'], null=False))
        ))
        db.create_unique(m2m_table_name, ['product_id', 'tutorial_id'])

        # Adding model 'ProductImage'
        db.create_table(u'catalog_productimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('added_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_facebook.FacebookCustomUser'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Product'])),
        ))
        db.send_create_signal(u'catalog', ['ProductImage'])

        # Adding model 'Shop'
        db.create_table(u'catalog_shop', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('added_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'catalog', ['Shop'])

        # Adding model 'ProductShopUrl'
        db.create_table(u'catalog_productshopurl', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Product'])),
            ('shop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Shop'])),
            ('added_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'catalog', ['ProductShopUrl'])

        # Adding model 'ProductDescription'
        db.create_table(u'catalog_productdescription', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=10000)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Product'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_facebook.FacebookCustomUser'], blank=True)),
            ('shop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Shop'], blank=True)),
            ('added_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('user_or_shop', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'catalog', ['ProductDescription'])

        # Adding model 'LikeProduct'
        db.create_table(u'catalog_likeproduct', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_facebook.FacebookCustomUser'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Product'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'catalog', ['LikeProduct'])

        # Adding model 'LikeProductImage'
        db.create_table(u'catalog_likeproductimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_facebook.FacebookCustomUser'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Product'])),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.ProductImage'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'catalog', ['LikeProductImage'])

        # Adding model 'LikeMakey'
        db.create_table(u'catalog_likemakey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_facebook.FacebookCustomUser'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Product'])),
            ('makey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Makey'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'catalog', ['LikeMakey'])

        # Adding model 'LikeTutorial'
        db.create_table(u'catalog_liketutorial', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_facebook.FacebookCustomUser'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Product'])),
            ('tutorial', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Tutorial'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'catalog', ['LikeTutorial'])

        # Adding model 'LikeShop'
        db.create_table(u'catalog_likeshop', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_facebook.FacebookCustomUser'])),
            ('shop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Shop'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'catalog', ['LikeShop'])

        # Adding model 'LikeProductDescription'
        db.create_table(u'catalog_likeproductdescription', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_facebook.FacebookCustomUser'])),
            ('product_description', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.ProductDescription'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'catalog', ['LikeProductDescription'])

        # Adding model 'EmailCollect'
        db.create_table(u'catalog_emailcollect', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=30)),
        ))
        db.send_create_signal(u'catalog', ['EmailCollect'])


    def backwards(self, orm):
        # Deleting model 'Makey'
        db.delete_table(u'catalog_makey')

        # Deleting model 'Tutorial'
        db.delete_table(u'catalog_tutorial')

        # Deleting model 'Product'
        db.delete_table(u'catalog_product')

        # Removing M2M table for field makeys on 'Product'
        db.delete_table(db.shorten_name(u'catalog_product_makeys'))

        # Removing M2M table for field tutorials on 'Product'
        db.delete_table(db.shorten_name(u'catalog_product_tutorials'))

        # Deleting model 'ProductImage'
        db.delete_table(u'catalog_productimage')

        # Deleting model 'Shop'
        db.delete_table(u'catalog_shop')

        # Deleting model 'ProductShopUrl'
        db.delete_table(u'catalog_productshopurl')

        # Deleting model 'ProductDescription'
        db.delete_table(u'catalog_productdescription')

        # Deleting model 'LikeProduct'
        db.delete_table(u'catalog_likeproduct')

        # Deleting model 'LikeProductImage'
        db.delete_table(u'catalog_likeproductimage')

        # Deleting model 'LikeMakey'
        db.delete_table(u'catalog_likemakey')

        # Deleting model 'LikeTutorial'
        db.delete_table(u'catalog_liketutorial')

        # Deleting model 'LikeShop'
        db.delete_table(u'catalog_likeshop')

        # Deleting model 'LikeProductDescription'
        db.delete_table(u'catalog_likeproductdescription')

        # Deleting model 'EmailCollect'
        db.delete_table(u'catalog_emailcollect')


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
        u'catalog.emailcollect': {
            'Meta': {'object_name': 'EmailCollect'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'catalog.likemakey': {
            'Meta': {'object_name': 'LikeMakey'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'makey': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Makey']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Product']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        u'catalog.likeproduct': {
            'Meta': {'object_name': 'LikeProduct'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Product']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        u'catalog.likeproductdescription': {
            'Meta': {'object_name': 'LikeProductDescription'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product_description': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.ProductDescription']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        u'catalog.likeproductimage': {
            'Meta': {'object_name': 'LikeProductImage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.ProductImage']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Product']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        u'catalog.likeshop': {
            'Meta': {'object_name': 'LikeShop'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Shop']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        u'catalog.liketutorial': {
            'Meta': {'object_name': 'LikeTutorial'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Product']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'tutorial': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Tutorial']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        u'catalog.makey': {
            'Meta': {'object_name': 'Makey'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        u'catalog.product': {
            'Meta': {'object_name': 'Product'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'makeys': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['catalog.Makey']", 'symmetrical': 'False', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'sku': ('django.db.models.fields.IntegerField', [], {}),
            'tutorials': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['catalog.Tutorial']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'catalog.productdescription': {
            'Meta': {'object_name': 'ProductDescription'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '10000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Product']"}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Shop']", 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']", 'blank': 'True'}),
            'user_or_shop': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'catalog.productimage': {
            'Meta': {'object_name': 'ProductImage'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Product']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        u'catalog.productshopurl': {
            'Meta': {'object_name': 'ProductShopUrl'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Product']"}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Shop']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'catalog.shop': {
            'Meta': {'object_name': 'Shop'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'catalog.tutorial': {
            'Meta': {'object_name': 'Tutorial'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'django_facebook.facebookcustomuser': {
            'Meta': {'object_name': 'FacebookCustomUser'},
            'about_me': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'access_token': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'blog_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'facebook_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'facebook_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'facebook_open_graph': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_profile_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'new_token_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'raw_data': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'website_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['catalog']