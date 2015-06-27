# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'BaseModel'
        db.delete_table(u'catalog_basemodel')

        # Deleting field 'ProductImage.basemodel_ptr'
        db.delete_column(u'catalog_productimage', u'basemodel_ptr_id')

        # Adding field 'ProductImage.id'
        db.execute('ALTER TABLE "catalog_productimage" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
#        db.add_column(u'catalog_productimage', u'id',
 #                     self.gf('django.db.models.fields.AutoField')(primary_key=True),
  #                    keep_default=False)

        # Adding field 'ProductImage.added_time'
        db.add_column(u'catalog_productimage', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'ProductImage.is_enabled'
        db.add_column(u'catalog_productimage', 'is_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'ProductImage.score'
        db.add_column(u'catalog_productimage', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'AbstractTop.basemodel_ptr'
        db.delete_column(u'catalog_abstracttop', u'basemodel_ptr_id')

        # Adding field 'AbstractTop.id'
        db.execute('ALTER TABLE "catalog_abstracttop" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
#        db.add_column(u'catalog_abstracttop', u'id',
 #                     self.gf('django.db.models.fields.AutoField')(primary_key=True),
  #                    keep_default=False)

        # Adding field 'AbstractTop.added_time'
        db.add_column(u'catalog_abstracttop', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'AbstractTop.is_enabled'
        db.add_column(u'catalog_abstracttop', 'is_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'AbstractTop.score'
        db.add_column(u'catalog_abstracttop', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'Product.basemodel_ptr'
        db.delete_column(u'catalog_product', u'basemodel_ptr_id')

        # Adding field 'Product.id'
        db.execute('ALTER TABLE "catalog_product" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
#     db.add_column(u'catalog_product', u'id',
 #                     self.gf('django.db.models.fields.AutoField')(primary_key=True),
  #                    keep_default=False)

        # Adding field 'Product.added_time'
        db.add_column(u'catalog_product', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'Product.is_enabled'
        db.add_column(u'catalog_product', 'is_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Product.score'
        db.add_column(u'catalog_product', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'Image.basemodel_ptr'
        db.delete_column(u'catalog_image', u'basemodel_ptr_id')

        # Adding field 'Image.id'
        db.execute('ALTER TABLE "catalog_image" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
#        db.add_column(u'catalog_image', u'id',
 #                     self.gf('django.db.models.fields.AutoField')(primary_key=True),
  #                    keep_default=False)

        # Adding field 'Image.added_time'
        db.add_column(u'catalog_image', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'Image.is_enabled'
        db.add_column(u'catalog_image', 'is_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Image.score'
        db.add_column(u'catalog_image', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'Tutorial.basemodel_ptr'
        db.delete_column(u'catalog_tutorial', u'basemodel_ptr_id')

        # Adding field 'Tutorial.id'
        db.execute('ALTER TABLE "catalog_tutorial" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
#     db.add_column(u'catalog_tutorial', u'id',
 #                     self.gf('django.db.models.fields.AutoField')(primary_key=True),
  #                    keep_default=False)

        # Adding field 'Tutorial.added_time'
        db.add_column(u'catalog_tutorial', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'Tutorial.is_enabled'
        db.add_column(u'catalog_tutorial', 'is_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Tutorial.score'
        db.add_column(u'catalog_tutorial', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'AbstractLike.basemodel_ptr'
        db.delete_column(u'catalog_abstractlike', u'basemodel_ptr_id')

        # Adding field 'AbstractLike.id'
        db.execute('ALTER TABLE "catalog_abstractlike" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
#        db.add_column(u'catalog_abstractlike', u'id',
 #                     self.gf('django.db.models.fields.AutoField')(primary_key=True),
  #                    keep_default=False)

        # Adding field 'AbstractLike.added_time'
        db.add_column(u'catalog_abstractlike', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'AbstractLike.is_enabled'
        db.add_column(u'catalog_abstractlike', 'is_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'AbstractLike.score'
        db.add_column(u'catalog_abstractlike', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'ListItem.basemodel_ptr'
        db.delete_column(u'catalog_listitem', u'basemodel_ptr_id')

        # Adding field 'ListItem.id'
        db.execute('ALTER TABLE "catalog_listitem" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
        # db.add_column(u'catalog_listitem', u'id',
        #               self.gf('django.db.models.fields.AutoField')(primary_key=True),
        #               keep_default=False)

        # Adding field 'ListItem.added_time'
        db.add_column(u'catalog_listitem', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'ListItem.is_enabled'
        db.add_column(u'catalog_listitem', 'is_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'ListItem.score'
        db.add_column(u'catalog_listitem', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'ProductShopUrl.basemodel_ptr'
        db.delete_column(u'catalog_productshopurl', u'basemodel_ptr_id')

        # Adding field 'ProductShopUrl.id'
        db.execute('ALTER TABLE "catalog_productshopurl" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
        # db.add_column(u'catalog_productshopurl', u'id',
        #               self.gf('django.db.models.fields.AutoField')(primary_key=True),
        #               keep_default=False)

        # Adding field 'ProductShopUrl.added_time'
        db.add_column(u'catalog_productshopurl', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'ProductShopUrl.is_enabled'
        db.add_column(u'catalog_productshopurl', 'is_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'ProductShopUrl.score'
        db.add_column(u'catalog_productshopurl', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'ProductDescription.basemodel_ptr'
        db.delete_column(u'catalog_productdescription', u'basemodel_ptr_id')

        # Adding field 'ProductDescription.id'
        db.execute('ALTER TABLE "catalog_productdescription" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
        # db.add_column(u'catalog_productdescription', u'id',
        #               self.gf('django.db.models.fields.AutoField')(primary_key=True),
        #               keep_default=False)

        # Adding field 'ProductDescription.added_time'
        db.add_column(u'catalog_productdescription', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'ProductDescription.is_enabled'
        db.add_column(u'catalog_productdescription', 'is_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'ProductDescription.score'
        db.add_column(u'catalog_productdescription', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'Comment.basemodel_ptr'
        db.delete_column(u'catalog_comment', u'basemodel_ptr_id')

        # Adding field 'Comment.id'
        db.execute('ALTER TABLE "catalog_comment" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
        # db.add_column(u'catalog_comment', u'id',
        #               self.gf('django.db.models.fields.AutoField')(primary_key=True),
        #               keep_default=False)

        # Adding field 'Comment.added_time'
        db.add_column(u'catalog_comment', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'Comment.is_enabled'
        db.add_column(u'catalog_comment', 'is_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Comment.score'
        db.add_column(u'catalog_comment', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'List.basemodel_ptr'
        db.delete_column(u'catalog_list', u'basemodel_ptr_id')

        # Adding field 'List.id'
        db.execute('ALTER TABLE "catalog_list" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
        # db.add_column(u'catalog_list', u'id',
        #               self.gf('django.db.models.fields.AutoField')(primary_key=True),
        #               keep_default=False)

        # Adding field 'List.added_time'
        db.add_column(u'catalog_list', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'List.is_enabled'
        db.add_column(u'catalog_list', 'is_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'List.score'
        db.add_column(u'catalog_list', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'ListGroup.basemodel_ptr'
        db.delete_column(u'catalog_listgroup', u'basemodel_ptr_id')

        # Adding field 'ListGroup.id'
        db.execute('ALTER TABLE "catalog_listgroup" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
        # db.add_column(u'catalog_listgroup', u'id',
        #               self.gf('django.db.models.fields.AutoField')(primary_key=True),
        #               keep_default=False)

        # Adding field 'ListGroup.added_time'
        db.add_column(u'catalog_listgroup', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'ListGroup.is_enabled'
        db.add_column(u'catalog_listgroup', 'is_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'ListGroup.score'
        db.add_column(u'catalog_listgroup', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'Documentation.basemodel_ptr'
        db.delete_column(u'catalog_documentation', u'basemodel_ptr_id')

        # Adding field 'Documentation.id'
        db.execute('ALTER TABLE "catalog_documentation" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
        # db.add_column(u'catalog_documentation', u'id',
        #               self.gf('django.db.models.fields.AutoField')(primary_key=True),
        #               keep_default=False)

        # Adding field 'Documentation.added_time'
        db.add_column(u'catalog_documentation', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'Documentation.is_enabled'
        db.add_column(u'catalog_documentation', 'is_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Documentation.score'
        db.add_column(u'catalog_documentation', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'Note.basemodel_ptr'
        db.delete_column(u'catalog_note', u'basemodel_ptr_id')

        # Adding field 'Note.id'
        db.execute('ALTER TABLE "catalog_note" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
        # db.add_column(u'catalog_note', u'id',
        #               self.gf('django.db.models.fields.AutoField')(primary_key=True),
        #               keep_default=False)

        # Adding field 'Note.added_time'
        db.add_column(u'catalog_note', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'Note.is_enabled'
        db.add_column(u'catalog_note', 'is_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Note.score'
        db.add_column(u'catalog_note', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'Makey.basemodel_ptr'
        db.delete_column(u'catalog_makey', u'basemodel_ptr_id')

        # Adding field 'Makey.id'
        db.execute('ALTER TABLE "catalog_makey" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
        # db.add_column(u'catalog_makey', u'id',
        #               self.gf('django.db.models.fields.AutoField')(primary_key=True),
        #               keep_default=False)

        # Adding field 'Makey.added_time'
        db.add_column(u'catalog_makey', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'Makey.is_enabled'
        db.add_column(u'catalog_makey', 'is_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Makey.score'
        db.add_column(u'catalog_makey', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'Location.basemodel_ptr'
        db.delete_column(u'catalog_location', u'basemodel_ptr_id')

        # Adding field 'Location.id'
        db.execute('ALTER TABLE "catalog_location" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
        # db.add_column(u'catalog_location', u'id',
        #               self.gf('django.db.models.fields.AutoField')(primary_key=True),
        #               keep_default=False)

        # Adding field 'Location.added_time'
        db.add_column(u'catalog_location', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'Location.is_enabled'
        db.add_column(u'catalog_location', 'is_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Location.score'
        db.add_column(u'catalog_location', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'ProductReview.basemodel_ptr'
        db.delete_column(u'catalog_productreview', u'basemodel_ptr_id')

        # Adding field 'ProductReview.id'
        db.execute('ALTER TABLE "catalog_productreview" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
        # db.add_column(u'catalog_productreview', u'id',
        #               self.gf('django.db.models.fields.AutoField')(primary_key=True),
        #               keep_default=False)

        # Adding field 'ProductReview.added_time'
        db.add_column(u'catalog_productreview', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'ProductReview.is_enabled'
        db.add_column(u'catalog_productreview', 'is_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'ProductReview.score'
        db.add_column(u'catalog_productreview', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'Shop.basemodel_ptr'
        db.delete_column(u'catalog_shop', u'basemodel_ptr_id')

        # Adding field 'Shop.id'
        db.execute('ALTER TABLE "catalog_shop" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
        # db.add_column(u'catalog_shop', u'id',
        #               self.gf('django.db.models.fields.AutoField')(primary_key=True),
        #               keep_default=False)

        # Adding field 'Shop.added_time'
        db.add_column(u'catalog_shop', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'Shop.is_enabled'
        db.add_column(u'catalog_shop', 'is_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Shop.score'
        db.add_column(u'catalog_shop', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'CfiStoreItem.basemodel_ptr'
        db.delete_column(u'catalog_cfistoreitem', u'basemodel_ptr_id')

        # Adding field 'CfiStoreItem.id'
        db.execute('ALTER TABLE "catalog_cfistoreitem" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
        # db.add_column(u'catalog_cfistoreitem', u'id',
        #               self.gf('django.db.models.fields.AutoField')(primary_key=True),
        #               keep_default=False)

        # Adding field 'CfiStoreItem.added_time'
        db.add_column(u'catalog_cfistoreitem', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'CfiStoreItem.is_enabled'
        db.add_column(u'catalog_cfistoreitem', 'is_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'CfiStoreItem.score'
        db.add_column(u'catalog_cfistoreitem', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'ShopReview.basemodel_ptr'
        db.delete_column(u'catalog_shopreview', u'basemodel_ptr_id')

        # Adding field 'ShopReview.id'
        db.execute('ALTER TABLE "catalog_shopreview" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
        # db.add_column(u'catalog_shopreview', u'id',
        #               self.gf('django.db.models.fields.AutoField')(primary_key=True),
        #               keep_default=False)

        # Adding field 'ShopReview.added_time'
        db.add_column(u'catalog_shopreview', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'ShopReview.is_enabled'
        db.add_column(u'catalog_shopreview', 'is_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'ShopReview.score'
        db.add_column(u'catalog_shopreview', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'BaseModel'
        db.create_table(u'catalog_basemodel', (
            ('added_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('catalog', ['BaseModel'])


        # User chose to not deal with backwards NULL issues for 'ProductImage.basemodel_ptr'
        raise RuntimeError("Cannot reverse this migration. 'ProductImage.basemodel_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ProductImage.basemodel_ptr'
        db.add_column(u'catalog_productimage', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'ProductImage.id'
        db.delete_column(u'catalog_productimage', u'id')

        # Deleting field 'ProductImage.added_time'
        db.delete_column(u'catalog_productimage', 'added_time')

        # Deleting field 'ProductImage.is_enabled'
        db.delete_column(u'catalog_productimage', 'is_enabled')

        # Deleting field 'ProductImage.score'
        db.delete_column(u'catalog_productimage', 'score')


        # User chose to not deal with backwards NULL issues for 'AbstractTop.basemodel_ptr'
        raise RuntimeError("Cannot reverse this migration. 'AbstractTop.basemodel_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AbstractTop.basemodel_ptr'
        db.add_column(u'catalog_abstracttop', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'AbstractTop.id'
        db.delete_column(u'catalog_abstracttop', u'id')

        # Deleting field 'AbstractTop.added_time'
        db.delete_column(u'catalog_abstracttop', 'added_time')

        # Deleting field 'AbstractTop.is_enabled'
        db.delete_column(u'catalog_abstracttop', 'is_enabled')

        # Deleting field 'AbstractTop.score'
        db.delete_column(u'catalog_abstracttop', 'score')


        # User chose to not deal with backwards NULL issues for 'Product.basemodel_ptr'
        raise RuntimeError("Cannot reverse this migration. 'Product.basemodel_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Product.basemodel_ptr'
        db.add_column(u'catalog_product', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'Product.id'
        db.delete_column(u'catalog_product', u'id')

        # Deleting field 'Product.added_time'
        db.delete_column(u'catalog_product', 'added_time')

        # Deleting field 'Product.is_enabled'
        db.delete_column(u'catalog_product', 'is_enabled')

        # Deleting field 'Product.score'
        db.delete_column(u'catalog_product', 'score')


        # User chose to not deal with backwards NULL issues for 'Image.basemodel_ptr'
        raise RuntimeError("Cannot reverse this migration. 'Image.basemodel_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Image.basemodel_ptr'
        db.add_column(u'catalog_image', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'Image.id'
        db.delete_column(u'catalog_image', u'id')

        # Deleting field 'Image.added_time'
        db.delete_column(u'catalog_image', 'added_time')

        # Deleting field 'Image.is_enabled'
        db.delete_column(u'catalog_image', 'is_enabled')

        # Deleting field 'Image.score'
        db.delete_column(u'catalog_image', 'score')


        # User chose to not deal with backwards NULL issues for 'Tutorial.basemodel_ptr'
        raise RuntimeError("Cannot reverse this migration. 'Tutorial.basemodel_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Tutorial.basemodel_ptr'
        db.add_column(u'catalog_tutorial', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'Tutorial.id'
        db.delete_column(u'catalog_tutorial', u'id')

        # Deleting field 'Tutorial.added_time'
        db.delete_column(u'catalog_tutorial', 'added_time')

        # Deleting field 'Tutorial.is_enabled'
        db.delete_column(u'catalog_tutorial', 'is_enabled')

        # Deleting field 'Tutorial.score'
        db.delete_column(u'catalog_tutorial', 'score')


        # User chose to not deal with backwards NULL issues for 'AbstractLike.basemodel_ptr'
        raise RuntimeError("Cannot reverse this migration. 'AbstractLike.basemodel_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AbstractLike.basemodel_ptr'
        db.add_column(u'catalog_abstractlike', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'AbstractLike.id'
        db.delete_column(u'catalog_abstractlike', u'id')

        # Deleting field 'AbstractLike.added_time'
        db.delete_column(u'catalog_abstractlike', 'added_time')

        # Deleting field 'AbstractLike.is_enabled'
        db.delete_column(u'catalog_abstractlike', 'is_enabled')

        # Deleting field 'AbstractLike.score'
        db.delete_column(u'catalog_abstractlike', 'score')


        # User chose to not deal with backwards NULL issues for 'ListItem.basemodel_ptr'
        raise RuntimeError("Cannot reverse this migration. 'ListItem.basemodel_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ListItem.basemodel_ptr'
        db.add_column(u'catalog_listitem', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'ListItem.id'
        db.delete_column(u'catalog_listitem', u'id')

        # Deleting field 'ListItem.added_time'
        db.delete_column(u'catalog_listitem', 'added_time')

        # Deleting field 'ListItem.is_enabled'
        db.delete_column(u'catalog_listitem', 'is_enabled')

        # Deleting field 'ListItem.score'
        db.delete_column(u'catalog_listitem', 'score')


        # User chose to not deal with backwards NULL issues for 'ProductShopUrl.basemodel_ptr'
        raise RuntimeError("Cannot reverse this migration. 'ProductShopUrl.basemodel_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ProductShopUrl.basemodel_ptr'
        db.add_column(u'catalog_productshopurl', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'ProductShopUrl.id'
        db.delete_column(u'catalog_productshopurl', u'id')

        # Deleting field 'ProductShopUrl.added_time'
        db.delete_column(u'catalog_productshopurl', 'added_time')

        # Deleting field 'ProductShopUrl.is_enabled'
        db.delete_column(u'catalog_productshopurl', 'is_enabled')

        # Deleting field 'ProductShopUrl.score'
        db.delete_column(u'catalog_productshopurl', 'score')


        # User chose to not deal with backwards NULL issues for 'ProductDescription.basemodel_ptr'
        raise RuntimeError("Cannot reverse this migration. 'ProductDescription.basemodel_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ProductDescription.basemodel_ptr'
        db.add_column(u'catalog_productdescription', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'ProductDescription.id'
        db.delete_column(u'catalog_productdescription', u'id')

        # Deleting field 'ProductDescription.added_time'
        db.delete_column(u'catalog_productdescription', 'added_time')

        # Deleting field 'ProductDescription.is_enabled'
        db.delete_column(u'catalog_productdescription', 'is_enabled')

        # Deleting field 'ProductDescription.score'
        db.delete_column(u'catalog_productdescription', 'score')


        # User chose to not deal with backwards NULL issues for 'Comment.basemodel_ptr'
        raise RuntimeError("Cannot reverse this migration. 'Comment.basemodel_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Comment.basemodel_ptr'
        db.add_column(u'catalog_comment', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'Comment.id'
        db.delete_column(u'catalog_comment', u'id')

        # Deleting field 'Comment.added_time'
        db.delete_column(u'catalog_comment', 'added_time')

        # Deleting field 'Comment.is_enabled'
        db.delete_column(u'catalog_comment', 'is_enabled')

        # Deleting field 'Comment.score'
        db.delete_column(u'catalog_comment', 'score')


        # User chose to not deal with backwards NULL issues for 'List.basemodel_ptr'
        raise RuntimeError("Cannot reverse this migration. 'List.basemodel_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'List.basemodel_ptr'
        db.add_column(u'catalog_list', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'List.id'
        db.delete_column(u'catalog_list', u'id')

        # Deleting field 'List.added_time'
        db.delete_column(u'catalog_list', 'added_time')

        # Deleting field 'List.is_enabled'
        db.delete_column(u'catalog_list', 'is_enabled')

        # Deleting field 'List.score'
        db.delete_column(u'catalog_list', 'score')


        # User chose to not deal with backwards NULL issues for 'ListGroup.basemodel_ptr'
        raise RuntimeError("Cannot reverse this migration. 'ListGroup.basemodel_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ListGroup.basemodel_ptr'
        db.add_column(u'catalog_listgroup', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'ListGroup.id'
        db.delete_column(u'catalog_listgroup', u'id')

        # Deleting field 'ListGroup.added_time'
        db.delete_column(u'catalog_listgroup', 'added_time')

        # Deleting field 'ListGroup.is_enabled'
        db.delete_column(u'catalog_listgroup', 'is_enabled')

        # Deleting field 'ListGroup.score'
        db.delete_column(u'catalog_listgroup', 'score')


        # User chose to not deal with backwards NULL issues for 'Documentation.basemodel_ptr'
        raise RuntimeError("Cannot reverse this migration. 'Documentation.basemodel_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Documentation.basemodel_ptr'
        db.add_column(u'catalog_documentation', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'Documentation.id'
        db.delete_column(u'catalog_documentation', u'id')

        # Deleting field 'Documentation.added_time'
        db.delete_column(u'catalog_documentation', 'added_time')

        # Deleting field 'Documentation.is_enabled'
        db.delete_column(u'catalog_documentation', 'is_enabled')

        # Deleting field 'Documentation.score'
        db.delete_column(u'catalog_documentation', 'score')


        # User chose to not deal with backwards NULL issues for 'Note.basemodel_ptr'
        raise RuntimeError("Cannot reverse this migration. 'Note.basemodel_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Note.basemodel_ptr'
        db.add_column(u'catalog_note', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'Note.id'
        db.delete_column(u'catalog_note', u'id')

        # Deleting field 'Note.added_time'
        db.delete_column(u'catalog_note', 'added_time')

        # Deleting field 'Note.is_enabled'
        db.delete_column(u'catalog_note', 'is_enabled')

        # Deleting field 'Note.score'
        db.delete_column(u'catalog_note', 'score')


        # User chose to not deal with backwards NULL issues for 'Makey.basemodel_ptr'
        raise RuntimeError("Cannot reverse this migration. 'Makey.basemodel_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Makey.basemodel_ptr'
        db.add_column(u'catalog_makey', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'Makey.id'
        db.delete_column(u'catalog_makey', u'id')

        # Deleting field 'Makey.added_time'
        db.delete_column(u'catalog_makey', 'added_time')

        # Deleting field 'Makey.is_enabled'
        db.delete_column(u'catalog_makey', 'is_enabled')

        # Deleting field 'Makey.score'
        db.delete_column(u'catalog_makey', 'score')


        # User chose to not deal with backwards NULL issues for 'Location.basemodel_ptr'
        raise RuntimeError("Cannot reverse this migration. 'Location.basemodel_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Location.basemodel_ptr'
        db.add_column(u'catalog_location', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'Location.id'
        db.delete_column(u'catalog_location', u'id')

        # Deleting field 'Location.added_time'
        db.delete_column(u'catalog_location', 'added_time')

        # Deleting field 'Location.is_enabled'
        db.delete_column(u'catalog_location', 'is_enabled')

        # Deleting field 'Location.score'
        db.delete_column(u'catalog_location', 'score')


        # User chose to not deal with backwards NULL issues for 'ProductReview.basemodel_ptr'
        raise RuntimeError("Cannot reverse this migration. 'ProductReview.basemodel_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ProductReview.basemodel_ptr'
        db.add_column(u'catalog_productreview', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'ProductReview.id'
        db.delete_column(u'catalog_productreview', u'id')

        # Deleting field 'ProductReview.added_time'
        db.delete_column(u'catalog_productreview', 'added_time')

        # Deleting field 'ProductReview.is_enabled'
        db.delete_column(u'catalog_productreview', 'is_enabled')

        # Deleting field 'ProductReview.score'
        db.delete_column(u'catalog_productreview', 'score')


        # User chose to not deal with backwards NULL issues for 'Shop.basemodel_ptr'
        raise RuntimeError("Cannot reverse this migration. 'Shop.basemodel_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Shop.basemodel_ptr'
        db.add_column(u'catalog_shop', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'Shop.id'
        db.delete_column(u'catalog_shop', u'id')

        # Deleting field 'Shop.added_time'
        db.delete_column(u'catalog_shop', 'added_time')

        # Deleting field 'Shop.is_enabled'
        db.delete_column(u'catalog_shop', 'is_enabled')

        # Deleting field 'Shop.score'
        db.delete_column(u'catalog_shop', 'score')


        # User chose to not deal with backwards NULL issues for 'CfiStoreItem.basemodel_ptr'
        raise RuntimeError("Cannot reverse this migration. 'CfiStoreItem.basemodel_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'CfiStoreItem.basemodel_ptr'
        db.add_column(u'catalog_cfistoreitem', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'CfiStoreItem.id'
        db.delete_column(u'catalog_cfistoreitem', u'id')

        # Deleting field 'CfiStoreItem.added_time'
        db.delete_column(u'catalog_cfistoreitem', 'added_time')

        # Deleting field 'CfiStoreItem.is_enabled'
        db.delete_column(u'catalog_cfistoreitem', 'is_enabled')

        # Deleting field 'CfiStoreItem.score'
        db.delete_column(u'catalog_cfistoreitem', 'score')


        # User chose to not deal with backwards NULL issues for 'ShopReview.basemodel_ptr'
        raise RuntimeError("Cannot reverse this migration. 'ShopReview.basemodel_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ShopReview.basemodel_ptr'
        db.add_column(u'catalog_shopreview', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'ShopReview.id'
        db.delete_column(u'catalog_shopreview', u'id')

        # Deleting field 'ShopReview.added_time'
        db.delete_column(u'catalog_shopreview', 'added_time')

        # Deleting field 'ShopReview.is_enabled'
        db.delete_column(u'catalog_shopreview', 'is_enabled')

        # Deleting field 'ShopReview.score'
        db.delete_column(u'catalog_shopreview', 'score')


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
        'catalog.abstractlike': {
            'Meta': {'object_name': 'AbstractLike'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'liked_time': ('django.db.models.fields.DateTimeField', [], {}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        'catalog.abstracttop': {
            'Meta': {'object_name': 'AbstractTop'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'recorded_time': ('django.db.models.fields.DateTimeField', [], {}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'catalog.cfistoreitem': {
            'Meta': {'object_name': 'CfiStoreItem'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'item': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.Product']", 'unique': 'True'}),
            'likers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'cfi_store_item_likes'", 'symmetrical': 'False', 'through': "orm['catalog.LikeCfiStoreItem']", 'to': u"orm['django_facebook.FacebookCustomUser']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'catalog.comment': {
            'Meta': {'object_name': 'Comment'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            'body': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        'catalog.documentation': {
            'Meta': {'object_name': 'Documentation'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '1000'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']", 'null': 'True', 'blank': 'True'})
        },
        'catalog.emailcollect': {
            'Meta': {'object_name': 'EmailCollect'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'catalog.image': {
            'Meta': {'object_name': 'Image'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'large_url': ('django.db.models.fields.URLField', [], {'max_length': '1000'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'small_url': ('django.db.models.fields.URLField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'images'", 'null': 'True', 'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        'catalog.like': {
            'Meta': {'object_name': 'Like', '_ormbases': ['catalog.AbstractLike']},
            u'abstractlike_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.AbstractLike']", 'unique': 'True', 'primary_key': 'True'})
        },
        'catalog.likecfistoreitem': {
            'Meta': {'object_name': 'LikeCfiStoreItem', '_ormbases': ['catalog.AbstractLike']},
            u'abstractlike_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.AbstractLike']", 'unique': 'True', 'primary_key': 'True'}),
            'cfi_store_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.CfiStoreItem']"})
        },
        'catalog.likemakey': {
            'Meta': {'object_name': 'LikeMakey', '_ormbases': ['catalog.AbstractLike']},
            u'abstractlike_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.AbstractLike']", 'unique': 'True', 'primary_key': 'True'}),
            'makey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Makey']"})
        },
        'catalog.likeproduct': {
            'Meta': {'object_name': 'LikeProduct', '_ormbases': ['catalog.AbstractLike']},
            u'abstractlike_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.AbstractLike']", 'unique': 'True', 'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Product']"})
        },
        'catalog.likeproductdescription': {
            'Meta': {'object_name': 'LikeProductDescription', '_ormbases': ['catalog.AbstractLike']},
            u'abstractlike_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.AbstractLike']", 'unique': 'True', 'primary_key': 'True'}),
            'product_description': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.ProductDescription']"})
        },
        'catalog.likeproductimage': {
            'Meta': {'object_name': 'LikeProductImage', '_ormbases': ['catalog.AbstractLike']},
            u'abstractlike_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.AbstractLike']", 'unique': 'True', 'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.ProductImage']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Product']"})
        },
        'catalog.likeproducttutorial': {
            'Meta': {'object_name': 'LikeProductTutorial', '_ormbases': ['catalog.AbstractLike']},
            u'abstractlike_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.AbstractLike']", 'unique': 'True', 'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Product']"}),
            'tutorial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Tutorial']"})
        },
        'catalog.likeshop': {
            'Meta': {'object_name': 'LikeShop', '_ormbases': ['catalog.AbstractLike']},
            u'abstractlike_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.AbstractLike']", 'unique': 'True', 'primary_key': 'True'}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Shop']"})
        },
        'catalog.list': {
            'Meta': {'object_name': 'List'},
            'access': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'access'", 'symmetrical': 'False', 'to': u"orm['django_facebook.FacebookCustomUser']"}),
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['catalog.ListItem']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner'", 'to': u"orm['django_facebook.FacebookCustomUser']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'catalog.listgroup': {
            'Meta': {'object_name': 'ListGroup'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'lists': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['catalog.List']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'catalog.listitem': {
            'Meta': {'object_name': 'ListItem'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            'createdby': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Product']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'catalog.location': {
            'Meta': {'object_name': 'Location'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'catalog.logidenticalproduct': {
            'Meta': {'object_name': 'LogIdenticalProduct'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'product1'", 'to': "orm['catalog.Product']"}),
            'product2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'product2'", 'to': "orm['catalog.Product']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        'catalog.makey': {
            'Meta': {'object_name': 'Makey'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            'collaborators': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'collaborators'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['django_facebook.FacebookCustomUser']"}),
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'makeycomments'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['catalog.Comment']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'documentations': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'makeydocumentations'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['catalog.Documentation']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'makeyimages'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['catalog.Image']"}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'makeynotes'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['catalog.Note']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']", 'null': 'True', 'blank': 'True'})
        },
        'catalog.note': {
            'Meta': {'object_name': 'Note'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            'body': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        'catalog.product': {
            'Meta': {'object_name': 'Product'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identicalto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Product']", 'null': 'True', 'blank': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'likers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'product_likes'", 'symmetrical': 'False', 'through': "orm['catalog.LikeProduct']", 'to': u"orm['django_facebook.FacebookCustomUser']"}),
            'makeys': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'partsused'", 'blank': 'True', 'to': "orm['catalog.Makey']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sku': ('django.db.models.fields.IntegerField', [], {}),
            'tutorials': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['catalog.Tutorial']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'catalog.productdescription': {
            'Meta': {'object_name': 'ProductDescription'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'productdescriptions'", 'to': "orm['catalog.Product']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Shop']", 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']", 'blank': 'True'}),
            'user_or_shop': ('django.db.models.fields.BooleanField', [], {})
        },
        'catalog.productimage': {
            'Meta': {'object_name': 'ProductImage'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'productimages'", 'to': "orm['catalog.Product']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Shop']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']", 'null': 'True', 'blank': 'True'})
        },
        'catalog.productreview': {
            'Meta': {'object_name': 'ProductReview'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'product_reviews'", 'to': "orm['catalog.Product']"}),
            'review': ('django.db.models.fields.CharField', [], {'max_length': '100000'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        'catalog.productshopurl': {
            'Meta': {'object_name': 'ProductShopUrl'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'productshopurls'", 'to': "orm['catalog.Product']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Shop']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'catalog.searchlog': {
            'Meta': {'object_name': 'SearchLog'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']", 'null': 'True', 'blank': 'True'})
        },
        'catalog.shop': {
            'Meta': {'object_name': 'Shop'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'shopimages'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['catalog.Image']"}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'likes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'shop_likes'", 'symmetrical': 'False', 'through': "orm['catalog.LikeShop']", 'to': u"orm['django_facebook.FacebookCustomUser']"}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'catalog.shopreview': {
            'Meta': {'object_name': 'ShopReview'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'review': ('django.db.models.fields.CharField', [], {'max_length': '100000'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shop_reviews'", 'to': "orm['catalog.Shop']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        'catalog.toindexstore': {
            'Meta': {'object_name': 'ToIndexStore'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'catalog.topmakeys': {
            'Meta': {'object_name': 'TopMakeys', '_ormbases': ['catalog.AbstractTop']},
            u'abstracttop_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.AbstractTop']", 'unique': 'True', 'primary_key': 'True'}),
            'makey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Makey']"})
        },
        'catalog.topproducts': {
            'Meta': {'object_name': 'TopProducts', '_ormbases': ['catalog.AbstractTop']},
            u'abstracttop_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.AbstractTop']", 'unique': 'True', 'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Product']"})
        },
        'catalog.topshops': {
            'Meta': {'object_name': 'TopShops', '_ormbases': ['catalog.AbstractTop']},
            u'abstracttop_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.AbstractTop']", 'unique': 'True', 'primary_key': 'True'}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Shop']"})
        },
        'catalog.toptutorials': {
            'Meta': {'object_name': 'TopTutorials', '_ormbases': ['catalog.AbstractTop']},
            u'abstracttop_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.AbstractTop']", 'unique': 'True', 'primary_key': 'True'}),
            'tutorial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Tutorial']"})
        },
        'catalog.topusers': {
            'Meta': {'object_name': 'TopUsers', '_ormbases': ['catalog.AbstractTop']},
            u'abstracttop_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.AbstractTop']", 'unique': 'True', 'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        'catalog.tutorial': {
            'Meta': {'object_name': 'Tutorial'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'tutorialimages'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['catalog.Image']"}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']", 'null': 'True', 'blank': 'True'})
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
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
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'website_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['catalog']
