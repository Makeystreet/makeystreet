# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'LikeTutorial'
        # commenting this to take care of merge issues
        # db.delete_table(u'catalog_liketutorial')

        # Adding model 'AbstractLike'
        db.create_table(u'catalog_abstractlike', (
            (u'basemodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.BaseModel'], unique=True, primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_facebook.FacebookCustomUser'])),
            ('liked_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('catalog', ['AbstractLike'])

        # Adding model 'LikeProductTutorial'
        db.create_table(u'catalog_likeproducttutorial', (
            (u'abstractlike_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.AbstractLike'], unique=True, primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Product'])),
            ('tutorial', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Tutorial'])),
        ))
        db.send_create_signal('catalog', ['LikeProductTutorial'])

        # Adding model 'AbstractTop'
        db.create_table(u'catalog_abstracttop', (
            (u'basemodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.BaseModel'], unique=True, primary_key=True)),
            ('recorded_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('catalog', ['AbstractTop'])

        # Adding model 'BaseModel'
        db.create_table(u'catalog_basemodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('added_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('catalog', ['BaseModel'])

        # Deleting field 'ProductImage.added_time'
        db.delete_column(u'catalog_productimage', 'added_time')

        # Deleting field 'Location.id'
        db.delete_column(u'catalog_location', u'id')

        # Adding field 'Location.basemodel_ptr'
        db.add_column(u'catalog_location', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=1, to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'LogIdenticalProduct.time'
        db.delete_column(u'catalog_logidenticalproduct', 'time')

        # Deleting field 'LogIdenticalProduct.id'
        db.delete_column(u'catalog_logidenticalproduct', u'id')

        # Adding field 'LogIdenticalProduct.basemodel_ptr'
        db.add_column(u'catalog_logidenticalproduct', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=2, to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'Product.disabled'
        db.delete_column(u'catalog_product', 'disabled')

        # Deleting field 'Product.added_time'
        db.delete_column(u'catalog_product', 'added_time')

        # Deleting field 'Product.score'
        db.delete_column(u'catalog_product', 'score')

        # Deleting field 'Product.id'
        db.delete_column(u'catalog_product', u'id')

        # Adding field 'Product.basemodel_ptr'
        db.add_column(u'catalog_product', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=2, to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'LikeShop.user'
        db.delete_column(u'catalog_likeshop', 'user_id')

        # Deleting field 'LikeShop.id'
        db.delete_column(u'catalog_likeshop', u'id')

        # Deleting field 'LikeShop.time'
        db.delete_column(u'catalog_likeshop', 'time')

        # Adding field 'LikeShop.abstractlike_ptr'
        db.add_column(u'catalog_likeshop', u'abstractlike_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=2, to=orm['catalog.AbstractLike'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'Image.added_time'
        db.delete_column(u'catalog_image', 'added_time')

        # Deleting field 'Image.id'
        db.delete_column(u'catalog_image', u'id')

        # Adding field 'Image.basemodel_ptr'
        db.add_column(u'catalog_image', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=2, to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'Tutorial.disabled'
        db.delete_column(u'catalog_tutorial', 'disabled')

        # Deleting field 'Tutorial.added_time'
        db.delete_column(u'catalog_tutorial', 'added_time')

        # Deleting field 'Tutorial.score'
        db.delete_column(u'catalog_tutorial', 'score')

        # Deleting field 'Tutorial.id'
        db.delete_column(u'catalog_tutorial', u'id')

        # Adding field 'Tutorial.basemodel_ptr'
        db.add_column(u'catalog_tutorial', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=2, to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'ListItem.id'
        db.delete_column(u'catalog_listitem', u'id')

        # Adding field 'ListItem.basemodel_ptr'
        db.add_column(u'catalog_listitem', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=2, to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'ProductShopUrl.added_time'
        db.delete_column(u'catalog_productshopurl', 'added_time')

        # Deleting field 'ProductShopUrl.id'
        db.delete_column(u'catalog_productshopurl', u'id')

        # Adding field 'ProductShopUrl.basemodel_ptr'
        db.add_column(u'catalog_productshopurl', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=2, to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'ProductDescription.added_time'
        db.delete_column(u'catalog_productdescription', 'added_time')

        # Deleting field 'Comment.added_time'
        db.delete_column(u'catalog_comment', 'added_time')

        # Deleting field 'Comment.id'
        db.delete_column(u'catalog_comment', u'id')

        # Adding field 'Comment.basemodel_ptr'
        db.add_column(u'catalog_comment', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=2, to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'List.id'
        db.delete_column(u'catalog_list', u'id')

        # Adding field 'List.basemodel_ptr'
        db.add_column(u'catalog_list', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=2, to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'ListGroup.id'
        db.delete_column(u'catalog_listgroup', u'id')

        # Adding field 'ListGroup.basemodel_ptr'
        db.add_column(u'catalog_listgroup', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=2, to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'Documentation.added_time'
        db.delete_column(u'catalog_documentation', 'added_time')

        # Deleting field 'Documentation.id'
        db.delete_column(u'catalog_documentation', u'id')

        # Adding field 'Documentation.basemodel_ptr'
        db.add_column(u'catalog_documentation', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=2, to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'TopMakeys.score'
        db.delete_column(u'catalog_topmakeys', 'score')

        # Deleting field 'TopMakeys.id'
        db.delete_column(u'catalog_topmakeys', u'id')

        # Deleting field 'TopMakeys.time'
        db.delete_column(u'catalog_topmakeys', 'time')

        # Adding field 'TopMakeys.abstracttop_ptr'
        db.add_column(u'catalog_topmakeys', u'abstracttop_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=2, to=orm['catalog.AbstractTop'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'Note.added_time'
        db.delete_column(u'catalog_note', 'added_time')

        # Deleting field 'Note.id'
        db.delete_column(u'catalog_note', u'id')

        # Adding field 'Note.basemodel_ptr'
        db.add_column(u'catalog_note', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=2, to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'Makey.disabled'
        db.delete_column(u'catalog_makey', 'disabled')

        # Deleting field 'Makey.score'
        db.delete_column(u'catalog_makey', 'score')

        # Deleting field 'Makey.id'
        db.delete_column(u'catalog_makey', u'id')

        # Deleting field 'Makey.added_time'
        db.delete_column(u'catalog_makey', 'added_time')

        # Adding field 'Makey.basemodel_ptr'
        db.add_column(u'catalog_makey', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=2, to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'LikeProductImage.user'
        db.delete_column(u'catalog_likeproductimage', 'user_id')

        # Deleting field 'LikeProductImage.time'
        db.delete_column(u'catalog_likeproductimage', 'time')

        # Deleting field 'LikeProductImage.id'
        db.delete_column(u'catalog_likeproductimage', u'id')

        # Adding field 'LikeProductImage.abstractlike_ptr'
        db.add_column(u'catalog_likeproductimage', u'abstractlike_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=2, to=orm['catalog.AbstractLike'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'SearchLog.id'
        db.delete_column(u'catalog_searchlog', u'id')

        # Adding field 'SearchLog.basemodel_ptr'
        db.add_column(u'catalog_searchlog', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=2, to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'LikeProductDescription.time'
        db.delete_column(u'catalog_likeproductdescription', 'time')

        # Deleting field 'LikeProductDescription.user'
        db.delete_column(u'catalog_likeproductdescription', 'user_id')

        # Deleting field 'LikeProductDescription.id'
        db.delete_column(u'catalog_likeproductdescription', u'id')

        # Adding field 'LikeProductDescription.abstractlike_ptr'
        db.add_column(u'catalog_likeproductdescription', u'abstractlike_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=2, to=orm['catalog.AbstractLike'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'LikeProduct.user'
        db.delete_column(u'catalog_likeproduct', 'user_id')

        # Deleting field 'LikeProduct.id'
        db.delete_column(u'catalog_likeproduct', u'id')

        # Deleting field 'LikeProduct.time'
        db.delete_column(u'catalog_likeproduct', 'time')

        # Adding field 'LikeProduct.abstractlike_ptr'
        db.add_column(u'catalog_likeproduct', u'abstractlike_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=2, to=orm['catalog.AbstractLike'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'Shop.disabled'
        db.delete_column(u'catalog_shop', 'disabled')

        # Deleting field 'Shop.added_time'
        db.delete_column(u'catalog_shop', 'added_time')

        # Deleting field 'Shop.score'
        db.delete_column(u'catalog_shop', 'score')

        # Deleting field 'Shop.id'
        db.delete_column(u'catalog_shop', u'id')

        # Adding field 'Shop.basemodel_ptr'
        db.add_column(u'catalog_shop', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=2, to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'TopProducts.score'
        db.delete_column(u'catalog_topproducts', 'score')

        # Deleting field 'TopProducts.id'
        db.delete_column(u'catalog_topproducts', u'id')

        # Deleting field 'TopProducts.time'
        db.delete_column(u'catalog_topproducts', 'time')

        # Adding field 'TopProducts.abstracttop_ptr'
        db.add_column(u'catalog_topproducts', u'abstracttop_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=2, to=orm['catalog.AbstractTop'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'LikeMakey.user'
        db.delete_column(u'catalog_likemakey', 'user_id')

        # Deleting field 'LikeMakey.id'
        db.delete_column(u'catalog_likemakey', u'id')

        # Deleting field 'LikeMakey.time'
        db.delete_column(u'catalog_likemakey', 'time')

        # Adding field 'LikeMakey.abstractlike_ptr'
        db.add_column(u'catalog_likemakey', u'abstractlike_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=2, to=orm['catalog.AbstractLike'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'ToIndexStore.added_time'
        db.delete_column(u'catalog_toindexstore', 'added_time')

        # Deleting field 'ToIndexStore.id'
        db.delete_column(u'catalog_toindexstore', u'id')

        # Adding field 'ToIndexStore.basemodel_ptr'
        db.add_column(u'catalog_toindexstore', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=2, to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'EmailCollect.id'
        db.delete_column(u'catalog_emailcollect', u'id')

        # Adding field 'EmailCollect.basemodel_ptr'
        db.add_column(u'catalog_emailcollect', u'basemodel_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=2, to=orm['catalog.BaseModel'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'TopUsers.score'
        db.delete_column(u'catalog_topusers', 'score')

        # Deleting field 'TopUsers.id'
        db.delete_column(u'catalog_topusers', u'id')

        # Deleting field 'TopUsers.time'
        db.delete_column(u'catalog_topusers', 'time')

        # Adding field 'TopUsers.abstracttop_ptr'
        db.add_column(u'catalog_topusers', u'abstracttop_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=2, to=orm['catalog.AbstractTop'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'TopShops.score'
        db.delete_column(u'catalog_topshops', 'score')

        # Deleting field 'TopShops.id'
        db.delete_column(u'catalog_topshops', u'id')

        # Deleting field 'TopShops.time'
        db.delete_column(u'catalog_topshops', 'time')

        # Adding field 'TopShops.abstracttop_ptr'
        db.add_column(u'catalog_topshops', u'abstracttop_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=2, to=orm['catalog.AbstractTop'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'TopTutorials.score'
        db.delete_column(u'catalog_toptutorials', 'score')

        # Deleting field 'TopTutorials.id'
        db.delete_column(u'catalog_toptutorials', u'id')

        # Deleting field 'TopTutorials.time'
        db.delete_column(u'catalog_toptutorials', 'time')

        # Adding field 'TopTutorials.abstracttop_ptr'
        db.add_column(u'catalog_toptutorials', u'abstracttop_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=2, to=orm['catalog.AbstractTop'], unique=True, primary_key=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'LikeTutorial'
        db.create_table(u'catalog_liketutorial', (
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Product'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_facebook.FacebookCustomUser'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tutorial', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Tutorial'])),
        ))
        db.send_create_signal(u'catalog', ['LikeTutorial'])

        # Deleting model 'AbstractLike'
        db.delete_table(u'catalog_abstractlike')

        # Deleting model 'LikeProductTutorial'
        db.delete_table(u'catalog_likeproducttutorial')

        # Deleting model 'AbstractTop'
        db.delete_table(u'catalog_abstracttop')

        # Deleting model 'BaseModel'
        db.delete_table(u'catalog_basemodel')

        # Adding field 'ProductImage.added_time'
        db.add_column(u'catalog_productimage', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 2, 12, 0, 0)),
                      keep_default=False)

        # Adding field 'Location.id'
        db.add_column(u'catalog_location', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=1, primary_key=True),
                      keep_default=False)

        # Deleting field 'Location.basemodel_ptr'
        db.delete_column(u'catalog_location', u'basemodel_ptr_id')

        # Adding field 'LogIdenticalProduct.time'
        db.add_column(u'catalog_logidenticalproduct', 'time',
                      self.gf('django.db.models.fields.DateTimeField')(default=2),
                      keep_default=False)

        # Adding field 'LogIdenticalProduct.id'
        db.add_column(u'catalog_logidenticalproduct', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=2, primary_key=True),
                      keep_default=False)

        # Deleting field 'LogIdenticalProduct.basemodel_ptr'
        db.delete_column(u'catalog_logidenticalproduct', u'basemodel_ptr_id')

        # Adding field 'Product.disabled'
        db.add_column(u'catalog_product', 'disabled',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Product.added_time'
        db.add_column(u'catalog_product', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=2),
                      keep_default=False)

        # Adding field 'Product.score'
        db.add_column(u'catalog_product', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Product.id'
        db.add_column(u'catalog_product', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=2, primary_key=True),
                      keep_default=False)

        # Deleting field 'Product.basemodel_ptr'
        db.delete_column(u'catalog_product', u'basemodel_ptr_id')

        # Adding field 'LikeShop.user'
        db.add_column(u'catalog_likeshop', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=2, to=orm['django_facebook.FacebookCustomUser']),
                      keep_default=False)

        # Adding field 'LikeShop.id'
        db.add_column(u'catalog_likeshop', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=2, primary_key=True),
                      keep_default=False)

        # Adding field 'LikeShop.time'
        db.add_column(u'catalog_likeshop', 'time',
                      self.gf('django.db.models.fields.DateTimeField')(default=2),
                      keep_default=False)

        # Deleting field 'LikeShop.abstractlike_ptr'
        db.delete_column(u'catalog_likeshop', u'abstractlike_ptr_id')

        # Adding field 'Image.added_time'
        db.add_column(u'catalog_image', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=2),
                      keep_default=False)

        # Adding field 'Image.id'
        db.add_column(u'catalog_image', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=2, primary_key=True),
                      keep_default=False)

        # Deleting field 'Image.basemodel_ptr'
        db.delete_column(u'catalog_image', u'basemodel_ptr_id')

        # Adding field 'Tutorial.disabled'
        db.add_column(u'catalog_tutorial', 'disabled',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Tutorial.added_time'
        db.add_column(u'catalog_tutorial', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=2),
                      keep_default=False)

        # Adding field 'Tutorial.score'
        db.add_column(u'catalog_tutorial', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Tutorial.id'
        db.add_column(u'catalog_tutorial', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=2, primary_key=True),
                      keep_default=False)

        # Deleting field 'Tutorial.basemodel_ptr'
        db.delete_column(u'catalog_tutorial', u'basemodel_ptr_id')

        # Adding field 'ListItem.id'
        db.add_column(u'catalog_listitem', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=2, primary_key=True),
                      keep_default=False)

        # Deleting field 'ListItem.basemodel_ptr'
        db.delete_column(u'catalog_listitem', u'basemodel_ptr_id')

        # Adding field 'ProductShopUrl.added_time'
        db.add_column(u'catalog_productshopurl', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=2),
                      keep_default=False)

        # Adding field 'ProductShopUrl.id'
        db.add_column(u'catalog_productshopurl', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=2, primary_key=True),
                      keep_default=False)

        # Deleting field 'ProductShopUrl.basemodel_ptr'
        db.delete_column(u'catalog_productshopurl', u'basemodel_ptr_id')

        # Adding field 'ProductDescription.added_time'
        db.add_column(u'catalog_productdescription', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=2),
                      keep_default=False)

        # Adding field 'Comment.added_time'
        db.add_column(u'catalog_comment', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=2),
                      keep_default=False)

        # Adding field 'Comment.id'
        db.add_column(u'catalog_comment', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=2, primary_key=True),
                      keep_default=False)

        # Deleting field 'Comment.basemodel_ptr'
        db.delete_column(u'catalog_comment', u'basemodel_ptr_id')

        # Adding field 'List.id'
        db.add_column(u'catalog_list', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=2, primary_key=True),
                      keep_default=False)

        # Deleting field 'List.basemodel_ptr'
        db.delete_column(u'catalog_list', u'basemodel_ptr_id')

        # Adding field 'ListGroup.id'
        db.add_column(u'catalog_listgroup', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=2, primary_key=True),
                      keep_default=False)

        # Deleting field 'ListGroup.basemodel_ptr'
        db.delete_column(u'catalog_listgroup', u'basemodel_ptr_id')

        # Adding field 'Documentation.added_time'
        db.add_column(u'catalog_documentation', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=2),
                      keep_default=False)

        # Adding field 'Documentation.id'
        db.add_column(u'catalog_documentation', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=2, primary_key=True),
                      keep_default=False)

        # Deleting field 'Documentation.basemodel_ptr'
        db.delete_column(u'catalog_documentation', u'basemodel_ptr_id')

        # Adding field 'TopMakeys.score'
        db.add_column(u'catalog_topmakeys', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=2),
                      keep_default=False)

        # Adding field 'TopMakeys.id'
        db.add_column(u'catalog_topmakeys', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=2, primary_key=True),
                      keep_default=False)

        # Adding field 'TopMakeys.time'
        db.add_column(u'catalog_topmakeys', 'time',
                      self.gf('django.db.models.fields.DateTimeField')(default=2),
                      keep_default=False)

        # Deleting field 'TopMakeys.abstracttop_ptr'
        db.delete_column(u'catalog_topmakeys', u'abstracttop_ptr_id')

        # Adding field 'Note.added_time'
        db.add_column(u'catalog_note', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=2),
                      keep_default=False)

        # Adding field 'Note.id'
        db.add_column(u'catalog_note', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=2, primary_key=True),
                      keep_default=False)

        # Deleting field 'Note.basemodel_ptr'
        db.delete_column(u'catalog_note', u'basemodel_ptr_id')

        # Adding field 'Makey.disabled'
        db.add_column(u'catalog_makey', 'disabled',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Makey.score'
        db.add_column(u'catalog_makey', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Makey.id'
        db.add_column(u'catalog_makey', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=2, primary_key=True),
                      keep_default=False)

        # Adding field 'Makey.added_time'
        db.add_column(u'catalog_makey', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=2),
                      keep_default=False)

        # Deleting field 'Makey.basemodel_ptr'
        db.delete_column(u'catalog_makey', u'basemodel_ptr_id')

        # Adding field 'LikeProductImage.user'
        db.add_column(u'catalog_likeproductimage', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=2, to=orm['django_facebook.FacebookCustomUser']),
                      keep_default=False)

        # Adding field 'LikeProductImage.time'
        db.add_column(u'catalog_likeproductimage', 'time',
                      self.gf('django.db.models.fields.DateTimeField')(default=2),
                      keep_default=False)

        # Adding field 'LikeProductImage.id'
        db.add_column(u'catalog_likeproductimage', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=2, primary_key=True),
                      keep_default=False)

        # Deleting field 'LikeProductImage.abstractlike_ptr'
        db.delete_column(u'catalog_likeproductimage', u'abstractlike_ptr_id')

        # Adding field 'SearchLog.id'
        db.add_column(u'catalog_searchlog', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=2, primary_key=True),
                      keep_default=False)

        # Deleting field 'SearchLog.basemodel_ptr'
        db.delete_column(u'catalog_searchlog', u'basemodel_ptr_id')

        # Adding field 'LikeProductDescription.time'
        db.add_column(u'catalog_likeproductdescription', 'time',
                      self.gf('django.db.models.fields.DateTimeField')(default=2),
                      keep_default=False)

        # Adding field 'LikeProductDescription.user'
        db.add_column(u'catalog_likeproductdescription', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=2, to=orm['django_facebook.FacebookCustomUser']),
                      keep_default=False)

        # Adding field 'LikeProductDescription.id'
        db.add_column(u'catalog_likeproductdescription', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=2, primary_key=True),
                      keep_default=False)

        # Deleting field 'LikeProductDescription.abstractlike_ptr'
        db.delete_column(u'catalog_likeproductdescription', u'abstractlike_ptr_id')

        # Adding field 'LikeProduct.user'
        db.add_column(u'catalog_likeproduct', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=2, to=orm['django_facebook.FacebookCustomUser']),
                      keep_default=False)

        # Adding field 'LikeProduct.id'
        db.add_column(u'catalog_likeproduct', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=2, primary_key=True),
                      keep_default=False)

        # Adding field 'LikeProduct.time'
        db.add_column(u'catalog_likeproduct', 'time',
                      self.gf('django.db.models.fields.DateTimeField')(default=2),
                      keep_default=False)

        # Deleting field 'LikeProduct.abstractlike_ptr'
        db.delete_column(u'catalog_likeproduct', u'abstractlike_ptr_id')

        # Adding field 'Shop.disabled'
        db.add_column(u'catalog_shop', 'disabled',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Shop.added_time'
        db.add_column(u'catalog_shop', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=2),
                      keep_default=False)

        # Adding field 'Shop.score'
        db.add_column(u'catalog_shop', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Shop.id'
        db.add_column(u'catalog_shop', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=2, primary_key=True),
                      keep_default=False)

        # Deleting field 'Shop.basemodel_ptr'
        db.delete_column(u'catalog_shop', u'basemodel_ptr_id')

        # Adding field 'TopProducts.score'
        db.add_column(u'catalog_topproducts', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=2),
                      keep_default=False)

        # Adding field 'TopProducts.id'
        db.add_column(u'catalog_topproducts', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=2, primary_key=True),
                      keep_default=False)

        # Adding field 'TopProducts.time'
        db.add_column(u'catalog_topproducts', 'time',
                      self.gf('django.db.models.fields.DateTimeField')(default=2),
                      keep_default=False)

        # Deleting field 'TopProducts.abstracttop_ptr'
        db.delete_column(u'catalog_topproducts', u'abstracttop_ptr_id')

        # Adding field 'LikeMakey.user'
        db.add_column(u'catalog_likemakey', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=2, to=orm['django_facebook.FacebookCustomUser']),
                      keep_default=False)

        # Adding field 'LikeMakey.id'
        db.add_column(u'catalog_likemakey', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=2, primary_key=True),
                      keep_default=False)

        # Adding field 'LikeMakey.time'
        db.add_column(u'catalog_likemakey', 'time',
                      self.gf('django.db.models.fields.DateTimeField')(default=2),
                      keep_default=False)

        # Deleting field 'LikeMakey.abstractlike_ptr'
        db.delete_column(u'catalog_likemakey', u'abstractlike_ptr_id')

        # Adding field 'ToIndexStore.added_time'
        db.add_column(u'catalog_toindexstore', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=2),
                      keep_default=False)

        # Adding field 'ToIndexStore.id'
        db.add_column(u'catalog_toindexstore', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=2, primary_key=True),
                      keep_default=False)

        # Deleting field 'ToIndexStore.basemodel_ptr'
        db.delete_column(u'catalog_toindexstore', u'basemodel_ptr_id')

        # Adding field 'EmailCollect.id'
        db.add_column(u'catalog_emailcollect', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=2, primary_key=True),
                      keep_default=False)

        # Deleting field 'EmailCollect.basemodel_ptr'
        db.delete_column(u'catalog_emailcollect', u'basemodel_ptr_id')

        # Adding field 'TopUsers.score'
        db.add_column(u'catalog_topusers', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=2),
                      keep_default=False)

        # Adding field 'TopUsers.id'
        db.add_column(u'catalog_topusers', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=2, primary_key=True),
                      keep_default=False)

        # Adding field 'TopUsers.time'
        db.add_column(u'catalog_topusers', 'time',
                      self.gf('django.db.models.fields.DateTimeField')(default=2),
                      keep_default=False)

        # Deleting field 'TopUsers.abstracttop_ptr'
        db.delete_column(u'catalog_topusers', u'abstracttop_ptr_id')

        # Adding field 'TopShops.score'
        db.add_column(u'catalog_topshops', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=2),
                      keep_default=False)

        # Adding field 'TopShops.id'
        db.add_column(u'catalog_topshops', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=2, primary_key=True),
                      keep_default=False)

        # Adding field 'TopShops.time'
        db.add_column(u'catalog_topshops', 'time',
                      self.gf('django.db.models.fields.DateTimeField')(default=2),
                      keep_default=False)

        # Deleting field 'TopShops.abstracttop_ptr'
        db.delete_column(u'catalog_topshops', u'abstracttop_ptr_id')

        # Adding field 'TopTutorials.score'
        db.add_column(u'catalog_toptutorials', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=2),
                      keep_default=False)

        # Adding field 'TopTutorials.id'
        db.add_column(u'catalog_toptutorials', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=2, primary_key=True),
                      keep_default=False)

        # Adding field 'TopTutorials.time'
        db.add_column(u'catalog_toptutorials', 'time',
                      self.gf('django.db.models.fields.DateTimeField')(default=2),
                      keep_default=False)

        # Deleting field 'TopTutorials.abstracttop_ptr'
        db.delete_column(u'catalog_toptutorials', u'abstracttop_ptr_id')


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
            'Meta': {'object_name': 'AbstractLike', '_ormbases': ['catalog.BaseModel']},
            u'basemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.BaseModel']", 'unique': 'True', 'primary_key': 'True'}),
            'liked_time': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        'catalog.abstracttop': {
            'Meta': {'object_name': 'AbstractTop', '_ormbases': ['catalog.BaseModel']},
            u'basemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.BaseModel']", 'unique': 'True', 'primary_key': 'True'}),
            'recorded_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'catalog.basemodel': {
            'Meta': {'object_name': 'BaseModel'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'catalog.comment': {
            'Meta': {'object_name': 'Comment', '_ormbases': ['catalog.BaseModel']},
            u'basemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.BaseModel']", 'unique': 'True', 'primary_key': 'True'}),
            'body': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        'catalog.documentation': {
            'Meta': {'object_name': 'Documentation', '_ormbases': ['catalog.BaseModel']},
            u'basemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.BaseModel']", 'unique': 'True', 'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '1000'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']", 'null': 'True', 'blank': 'True'})
        },
        'catalog.emailcollect': {
            'Meta': {'object_name': 'EmailCollect', '_ormbases': ['catalog.BaseModel']},
            u'basemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.BaseModel']", 'unique': 'True', 'primary_key': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '30'})
        },
        'catalog.image': {
            'Meta': {'object_name': 'Image', '_ormbases': ['catalog.BaseModel']},
            u'basemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.BaseModel']", 'unique': 'True', 'primary_key': 'True'}),
            'large_url': ('django.db.models.fields.URLField', [], {'max_length': '1000'}),
            'small_url': ('django.db.models.fields.URLField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'images'", 'null': 'True', 'to': u"orm['django_facebook.FacebookCustomUser']"})
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
            'Meta': {'object_name': 'List', '_ormbases': ['catalog.BaseModel']},
            'access': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'access'", 'symmetrical': 'False', 'to': u"orm['django_facebook.FacebookCustomUser']"}),
            u'basemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.BaseModel']", 'unique': 'True', 'primary_key': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['catalog.ListItem']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner'", 'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        'catalog.listgroup': {
            'Meta': {'object_name': 'ListGroup', '_ormbases': ['catalog.BaseModel']},
            u'basemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.BaseModel']", 'unique': 'True', 'primary_key': 'True'}),
            'lists': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['catalog.List']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'catalog.listitem': {
            'Meta': {'object_name': 'ListItem', '_ormbases': ['catalog.BaseModel']},
            u'basemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.BaseModel']", 'unique': 'True', 'primary_key': 'True'}),
            'createdby': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Product']"})
        },
        'catalog.location': {
            'Meta': {'object_name': 'Location', '_ormbases': ['catalog.BaseModel']},
            u'basemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.BaseModel']", 'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'catalog.logidenticalproduct': {
            'Meta': {'object_name': 'LogIdenticalProduct', '_ormbases': ['catalog.BaseModel']},
            u'basemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.BaseModel']", 'unique': 'True', 'primary_key': 'True'}),
            'product1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'product1'", 'to': "orm['catalog.Product']"}),
            'product2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'product2'", 'to': "orm['catalog.Product']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        'catalog.makey': {
            'Meta': {'object_name': 'Makey', '_ormbases': ['catalog.BaseModel']},
            u'basemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.BaseModel']", 'unique': 'True', 'primary_key': 'True'}),
            'collaborators': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'collaborators'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['django_facebook.FacebookCustomUser']"}),
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'makeycomments'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['catalog.Comment']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'documentations': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'makeydocumentations'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['catalog.Documentation']"}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'makeyimages'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['catalog.Image']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'makeynotes'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['catalog.Note']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']", 'null': 'True', 'blank': 'True'})
        },
        'catalog.note': {
            'Meta': {'object_name': 'Note', '_ormbases': ['catalog.BaseModel']},
            u'basemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.BaseModel']", 'unique': 'True', 'primary_key': 'True'}),
            'body': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        'catalog.product': {
            'Meta': {'object_name': 'Product', '_ormbases': ['catalog.BaseModel']},
            u'basemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.BaseModel']", 'unique': 'True', 'primary_key': 'True'}),
            'identicalto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Product']", 'null': 'True', 'blank': 'True'}),
            'makeys': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'partsused'", 'blank': 'True', 'to': "orm['catalog.Makey']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'sku': ('django.db.models.fields.IntegerField', [], {}),
            'tutorials': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['catalog.Tutorial']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'catalog.productdescription': {
            'Meta': {'object_name': 'ProductDescription'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'productdescriptions'", 'to': "orm['catalog.Product']"}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Shop']", 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']", 'blank': 'True'}),
            'user_or_shop': ('django.db.models.fields.BooleanField', [], {})
        },
        'catalog.productimage': {
            'Meta': {'object_name': 'ProductImage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'productimages'", 'to': "orm['catalog.Product']"}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Shop']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']", 'null': 'True', 'blank': 'True'})
        },
        'catalog.productshopurl': {
            'Meta': {'object_name': 'ProductShopUrl', '_ormbases': ['catalog.BaseModel']},
            u'basemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.BaseModel']", 'unique': 'True', 'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'productshopurls'", 'to': "orm['catalog.Product']"}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Shop']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'catalog.searchlog': {
            'Meta': {'object_name': 'SearchLog', '_ormbases': ['catalog.BaseModel']},
            u'basemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.BaseModel']", 'unique': 'True', 'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']", 'null': 'True', 'blank': 'True'})
        },
        'catalog.shop': {
            'Meta': {'object_name': 'Shop', '_ormbases': ['catalog.BaseModel']},
            u'basemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.BaseModel']", 'unique': 'True', 'primary_key': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'shopimages'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['catalog.Image']"}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'catalog.toindexstore': {
            'Meta': {'object_name': 'ToIndexStore', '_ormbases': ['catalog.BaseModel']},
            u'basemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.BaseModel']", 'unique': 'True', 'primary_key': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
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
            'Meta': {'object_name': 'Tutorial', '_ormbases': ['catalog.BaseModel']},
            u'basemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalog.BaseModel']", 'unique': 'True', 'primary_key': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'tutorialimages'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['catalog.Image']"}),
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