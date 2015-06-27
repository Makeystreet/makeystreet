# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'AbstractTop'
        db.delete_table(u'catalog_abstracttop')

        # Deleting model 'AbstractLike'
        db.delete_table(u'catalog_abstractlike')

        # Deleting field 'Like.abstractlike_ptr'
        db.delete_column(u'catalog_like', u'abstractlike_ptr_id')

        # Adding field 'Like.id'
        db.execute('ALTER TABLE "catalog_like" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
        # db.add_column(u'catalog_like', u'id',
        #               self.gf('django.db.models.fields.AutoField')(primary_key=True),
        #               keep_default=False)

        # Adding field 'Like.added_time'
        db.add_column(u'catalog_like', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'Like.is_enabled'
        db.add_column(u'catalog_like', 'is_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Like.score'
        db.add_column(u'catalog_like', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Like.user'
        db.add_column(u'catalog_like', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=76, to=orm['django_facebook.FacebookCustomUser']),
                      keep_default=False)

        # Deleting field 'LikeShop.abstractlike_ptr'
        db.delete_column(u'catalog_likeshop', u'abstractlike_ptr_id')

        # Adding field 'LikeShop.id'
        db.execute('ALTER TABLE "catalog_likeshop" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
        # db.add_column(u'catalog_likeshop', u'id',
        #               self.gf('django.db.models.fields.AutoField')(primary_key=True),
        #               keep_default=False)

        # Adding field 'LikeShop.added_time'
        db.add_column(u'catalog_likeshop', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'LikeShop.is_enabled'
        db.add_column(u'catalog_likeshop', 'is_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'LikeShop.score'
        db.add_column(u'catalog_likeshop', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'LikeShop.user'
        db.add_column(u'catalog_likeshop', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=76, to=orm['django_facebook.FacebookCustomUser']),
                      keep_default=False)

        # Deleting field 'LikeProductTutorial.abstractlike_ptr'
        db.delete_column(u'catalog_likeproducttutorial', u'abstractlike_ptr_id')

        # Adding field 'LikeProductTutorial.id'
        db.execute('ALTER TABLE "catalog_likeproducttutorial" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
        # db.add_column(u'catalog_likeproducttutorial', u'id',
        #               self.gf('django.db.models.fields.AutoField')(primary_key=True),
        #               keep_default=False)

        # Adding field 'LikeProductTutorial.added_time'
        db.add_column(u'catalog_likeproducttutorial', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'LikeProductTutorial.is_enabled'
        db.add_column(u'catalog_likeproducttutorial', 'is_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'LikeProductTutorial.score'
        db.add_column(u'catalog_likeproducttutorial', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'LikeProductTutorial.user'
        db.add_column(u'catalog_likeproducttutorial', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=76, to=orm['django_facebook.FacebookCustomUser']),
                      keep_default=False)

        # Deleting field 'TopMakeys.abstracttop_ptr'
        db.delete_column(u'catalog_topmakeys', u'abstracttop_ptr_id')

        # Adding field 'TopMakeys.id'
        db.execute('ALTER TABLE "catalog_topmakeys" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
        # db.add_column(u'catalog_topmakeys', u'id',
        #               self.gf('django.db.models.fields.AutoField')(primary_key=True),
        #               keep_default=False)

        # Deleting field 'LikeProductImage.abstractlike_ptr'
        db.delete_column(u'catalog_likeproductimage', u'abstractlike_ptr_id')

        # Adding field 'LikeProductImage.id'
        db.execute('ALTER TABLE "catalog_likeproductimage" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
        # db.add_column(u'catalog_likeproductimage', u'id',
        #               self.gf('django.db.models.fields.AutoField')(default=76, primary_key=True),
        #               keep_default=False)

        # Adding field 'LikeProductImage.added_time'
        db.add_column(u'catalog_likeproductimage', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'LikeProductImage.is_enabled'
        db.add_column(u'catalog_likeproductimage', 'is_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'LikeProductImage.score'
        db.add_column(u'catalog_likeproductimage', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'LikeProductImage.user'
        db.add_column(u'catalog_likeproductimage', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=76, to=orm['django_facebook.FacebookCustomUser']),
                      keep_default=False)

        # Deleting field 'LikeProductDescription.abstractlike_ptr'
        db.delete_column(u'catalog_likeproductdescription', u'abstractlike_ptr_id')

        # Adding field 'LikeProductDescription.id'
        db.execute('ALTER TABLE "catalog_likeproductdescription" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
        # db.add_column(u'catalog_likeproductdescription', u'id',
        #               self.gf('django.db.models.fields.AutoField')(primary_key=True),
        #               keep_default=False)

        # Adding field 'LikeProductDescription.added_time'
        db.add_column(u'catalog_likeproductdescription', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'LikeProductDescription.is_enabled'
        db.add_column(u'catalog_likeproductdescription', 'is_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'LikeProductDescription.score'
        db.add_column(u'catalog_likeproductdescription', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'LikeProductDescription.user'
        db.add_column(u'catalog_likeproductdescription', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=76, to=orm['django_facebook.FacebookCustomUser']),
                      keep_default=False)

        # Deleting field 'LikeProduct.abstractlike_ptr'
        db.delete_column(u'catalog_likeproduct', u'abstractlike_ptr_id')

        # Adding field 'LikeProduct.id'
        db.execute('ALTER TABLE "catalog_likeproduct" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
        # db.add_column(u'catalog_likeproduct', u'id',
        #               self.gf('django.db.models.fields.AutoField')(primary_key=True),
        #               keep_default=False)

        # Adding field 'LikeProduct.added_time'
        db.add_column(u'catalog_likeproduct', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'LikeProduct.is_enabled'
        db.add_column(u'catalog_likeproduct', 'is_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'LikeProduct.score'
        db.add_column(u'catalog_likeproduct', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'LikeProduct.user'
        db.add_column(u'catalog_likeproduct', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=76, to=orm['django_facebook.FacebookCustomUser']),
                      keep_default=False)

        # Deleting field 'TopProducts.abstracttop_ptr'
        db.delete_column(u'catalog_topproducts', u'abstracttop_ptr_id')

        # Adding field 'TopProducts.id'
        db.execute('ALTER TABLE "catalog_topproducts" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
        # db.add_column(u'catalog_topproducts', u'id',
        #               self.gf('django.db.models.fields.AutoField')(primary_key=True),
        #               keep_default=False)

        # Deleting field 'LikeMakey.abstractlike_ptr'
        db.delete_column(u'catalog_likemakey', u'abstractlike_ptr_id')

        # Adding field 'LikeMakey.id'
        db.execute('ALTER TABLE "catalog_likemakey" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
        # db.add_column(u'catalog_likemakey', u'id',
        #               self.gf('django.db.models.fields.AutoField')(primary_key=True),
        #               keep_default=False)

        # Adding field 'LikeMakey.added_time'
        db.add_column(u'catalog_likemakey', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'LikeMakey.is_enabled'
        db.add_column(u'catalog_likemakey', 'is_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'LikeMakey.score'
        db.add_column(u'catalog_likemakey', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'LikeMakey.user'
        db.add_column(u'catalog_likemakey', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=76, to=orm['django_facebook.FacebookCustomUser']),
                      keep_default=False)

        # Deleting field 'TopUsers.abstracttop_ptr'
        db.delete_column(u'catalog_topusers', u'abstracttop_ptr_id')

        # Adding field 'TopUsers.id'
        db.execute('ALTER TABLE "catalog_topusers" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
        # db.add_column(u'catalog_topusers', u'id',
        #               self.gf('django.db.models.fields.AutoField')(primary_key=True),
        #               keep_default=False)

        # Deleting field 'LikeCfiStoreItem.abstractlike_ptr'
        db.delete_column(u'catalog_likecfistoreitem', u'abstractlike_ptr_id')

        # Adding field 'LikeCfiStoreItem.id'
        db.execute('ALTER TABLE "catalog_likecfistoreitem" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
        # db.add_column(u'catalog_likecfistoreitem', u'id',
        #               self.gf('django.db.models.fields.AutoField')(primary_key=True),
        #               keep_default=False)

        # Adding field 'LikeCfiStoreItem.added_time'
        db.add_column(u'catalog_likecfistoreitem', 'added_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 3, 0, 0)),
                      keep_default=False)

        # Adding field 'LikeCfiStoreItem.is_enabled'
        db.add_column(u'catalog_likecfistoreitem', 'is_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'LikeCfiStoreItem.score'
        db.add_column(u'catalog_likecfistoreitem', 'score',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'LikeCfiStoreItem.user'
        db.add_column(u'catalog_likecfistoreitem', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=76, to=orm['django_facebook.FacebookCustomUser']),
                      keep_default=False)

        # Deleting field 'TopShops.abstracttop_ptr'
        db.delete_column(u'catalog_topshops', u'abstracttop_ptr_id')

        # Adding field 'TopShops.id'
        db.execute('ALTER TABLE "catalog_topshops" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
        # db.add_column(u'catalog_topshops', u'id',
        #               self.gf('django.db.models.fields.AutoField')(primary_key=True),
        #               keep_default=False)

        # Deleting field 'TopTutorials.abstracttop_ptr'
        db.delete_column(u'catalog_toptutorials', u'abstracttop_ptr_id')

        # Adding field 'TopTutorials.id'
        db.execute('ALTER TABLE "catalog_toptutorials" ADD COLUMN "id" SERIAL NOT NULL PRIMARY KEY')
        # db.add_column(u'catalog_toptutorials', u'id',
        #               self.gf('django.db.models.fields.AutoField')(primary_key=True),
        #               keep_default=False)


    def backwards(self, orm):
        # Adding model 'AbstractTop'
        db.create_table(u'catalog_abstracttop', (
            ('is_enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('recorded_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('added_time', self.gf('django.db.models.fields.DateTimeField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('catalog', ['AbstractTop'])

        # Adding model 'AbstractLike'
        db.create_table(u'catalog_abstractlike', (
            ('is_enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_facebook.FacebookCustomUser'])),
            ('liked_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('added_time', self.gf('django.db.models.fields.DateTimeField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('catalog', ['AbstractLike'])


        # User chose to not deal with backwards NULL issues for 'Like.abstractlike_ptr'
        raise RuntimeError("Cannot reverse this migration. 'Like.abstractlike_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Like.abstractlike_ptr'
        db.add_column(u'catalog_like', u'abstractlike_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.AbstractLike'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'Like.id'
        db.delete_column(u'catalog_like', u'id')

        # Deleting field 'Like.added_time'
        db.delete_column(u'catalog_like', 'added_time')

        # Deleting field 'Like.is_enabled'
        db.delete_column(u'catalog_like', 'is_enabled')

        # Deleting field 'Like.score'
        db.delete_column(u'catalog_like', 'score')

        # Deleting field 'Like.user'
        db.delete_column(u'catalog_like', 'user_id')


        # User chose to not deal with backwards NULL issues for 'LikeShop.abstractlike_ptr'
        raise RuntimeError("Cannot reverse this migration. 'LikeShop.abstractlike_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'LikeShop.abstractlike_ptr'
        db.add_column(u'catalog_likeshop', u'abstractlike_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.AbstractLike'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'LikeShop.id'
        db.delete_column(u'catalog_likeshop', u'id')

        # Deleting field 'LikeShop.added_time'
        db.delete_column(u'catalog_likeshop', 'added_time')

        # Deleting field 'LikeShop.is_enabled'
        db.delete_column(u'catalog_likeshop', 'is_enabled')

        # Deleting field 'LikeShop.score'
        db.delete_column(u'catalog_likeshop', 'score')

        # Deleting field 'LikeShop.user'
        db.delete_column(u'catalog_likeshop', 'user_id')


        # User chose to not deal with backwards NULL issues for 'LikeProductTutorial.abstractlike_ptr'
        raise RuntimeError("Cannot reverse this migration. 'LikeProductTutorial.abstractlike_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'LikeProductTutorial.abstractlike_ptr'
        db.add_column(u'catalog_likeproducttutorial', u'abstractlike_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.AbstractLike'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'LikeProductTutorial.id'
        db.delete_column(u'catalog_likeproducttutorial', u'id')

        # Deleting field 'LikeProductTutorial.added_time'
        db.delete_column(u'catalog_likeproducttutorial', 'added_time')

        # Deleting field 'LikeProductTutorial.is_enabled'
        db.delete_column(u'catalog_likeproducttutorial', 'is_enabled')

        # Deleting field 'LikeProductTutorial.score'
        db.delete_column(u'catalog_likeproducttutorial', 'score')

        # Deleting field 'LikeProductTutorial.user'
        db.delete_column(u'catalog_likeproducttutorial', 'user_id')


        # User chose to not deal with backwards NULL issues for 'TopMakeys.abstracttop_ptr'
        raise RuntimeError("Cannot reverse this migration. 'TopMakeys.abstracttop_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'TopMakeys.abstracttop_ptr'
        db.add_column(u'catalog_topmakeys', u'abstracttop_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.AbstractTop'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'TopMakeys.id'
        db.delete_column(u'catalog_topmakeys', u'id')

        # Adding field 'LikeProductImage.abstractlike_ptr'
        db.add_column(u'catalog_likeproductimage', u'abstractlike_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.AbstractLike'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'LikeProductImage.id'
        db.delete_column(u'catalog_likeproductimage', u'id')

        # Deleting field 'LikeProductImage.added_time'
        db.delete_column(u'catalog_likeproductimage', 'added_time')

        # Deleting field 'LikeProductImage.is_enabled'
        db.delete_column(u'catalog_likeproductimage', 'is_enabled')

        # Deleting field 'LikeProductImage.score'
        db.delete_column(u'catalog_likeproductimage', 'score')

        # Deleting field 'LikeProductImage.user'
        db.delete_column(u'catalog_likeproductimage', 'user_id')


        # User chose to not deal with backwards NULL issues for 'LikeProductDescription.abstractlike_ptr'
        raise RuntimeError("Cannot reverse this migration. 'LikeProductDescription.abstractlike_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'LikeProductDescription.abstractlike_ptr'
        db.add_column(u'catalog_likeproductdescription', u'abstractlike_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.AbstractLike'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'LikeProductDescription.id'
        db.delete_column(u'catalog_likeproductdescription', u'id')

        # Deleting field 'LikeProductDescription.added_time'
        db.delete_column(u'catalog_likeproductdescription', 'added_time')

        # Deleting field 'LikeProductDescription.is_enabled'
        db.delete_column(u'catalog_likeproductdescription', 'is_enabled')

        # Deleting field 'LikeProductDescription.score'
        db.delete_column(u'catalog_likeproductdescription', 'score')

        # Deleting field 'LikeProductDescription.user'
        db.delete_column(u'catalog_likeproductdescription', 'user_id')


        # User chose to not deal with backwards NULL issues for 'LikeProduct.abstractlike_ptr'
        raise RuntimeError("Cannot reverse this migration. 'LikeProduct.abstractlike_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'LikeProduct.abstractlike_ptr'
        db.add_column(u'catalog_likeproduct', u'abstractlike_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.AbstractLike'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'LikeProduct.id'
        db.delete_column(u'catalog_likeproduct', u'id')

        # Deleting field 'LikeProduct.added_time'
        db.delete_column(u'catalog_likeproduct', 'added_time')

        # Deleting field 'LikeProduct.is_enabled'
        db.delete_column(u'catalog_likeproduct', 'is_enabled')

        # Deleting field 'LikeProduct.score'
        db.delete_column(u'catalog_likeproduct', 'score')

        # Deleting field 'LikeProduct.user'
        db.delete_column(u'catalog_likeproduct', 'user_id')


        # User chose to not deal with backwards NULL issues for 'TopProducts.abstracttop_ptr'
        raise RuntimeError("Cannot reverse this migration. 'TopProducts.abstracttop_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'TopProducts.abstracttop_ptr'
        db.add_column(u'catalog_topproducts', u'abstracttop_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.AbstractTop'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'TopProducts.id'
        db.delete_column(u'catalog_topproducts', u'id')

        # Adding field 'LikeMakey.abstractlike_ptr'
        db.add_column(u'catalog_likemakey', u'abstractlike_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.AbstractLike'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'LikeMakey.id'
        db.delete_column(u'catalog_likemakey', u'id')

        # Deleting field 'LikeMakey.added_time'
        db.delete_column(u'catalog_likemakey', 'added_time')

        # Deleting field 'LikeMakey.is_enabled'
        db.delete_column(u'catalog_likemakey', 'is_enabled')

        # Deleting field 'LikeMakey.score'
        db.delete_column(u'catalog_likemakey', 'score')

        # Deleting field 'LikeMakey.user'
        db.delete_column(u'catalog_likemakey', 'user_id')


        # User chose to not deal with backwards NULL issues for 'TopUsers.abstracttop_ptr'
        raise RuntimeError("Cannot reverse this migration. 'TopUsers.abstracttop_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'TopUsers.abstracttop_ptr'
        db.add_column(u'catalog_topusers', u'abstracttop_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.AbstractTop'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'TopUsers.id'
        db.delete_column(u'catalog_topusers', u'id')

        # Adding field 'LikeCfiStoreItem.abstractlike_ptr'
        db.add_column(u'catalog_likecfistoreitem', u'abstractlike_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.AbstractLike'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'LikeCfiStoreItem.id'
        db.delete_column(u'catalog_likecfistoreitem', u'id')

        # Deleting field 'LikeCfiStoreItem.added_time'
        db.delete_column(u'catalog_likecfistoreitem', 'added_time')

        # Deleting field 'LikeCfiStoreItem.is_enabled'
        db.delete_column(u'catalog_likecfistoreitem', 'is_enabled')

        # Deleting field 'LikeCfiStoreItem.score'
        db.delete_column(u'catalog_likecfistoreitem', 'score')

        # Deleting field 'LikeCfiStoreItem.user'
        db.delete_column(u'catalog_likecfistoreitem', 'user_id')


        # User chose to not deal with backwards NULL issues for 'TopShops.abstracttop_ptr'
        raise RuntimeError("Cannot reverse this migration. 'TopShops.abstracttop_ptr' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'TopShops.abstracttop_ptr'
        db.add_column(u'catalog_topshops', u'abstracttop_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.AbstractTop'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'TopShops.id'
        db.delete_column(u'catalog_topshops', u'id')

        # Adding field 'TopTutorials.abstracttop_ptr'
        db.add_column(u'catalog_toptutorials', u'abstracttop_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalog.AbstractTop'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'TopTutorials.id'
        db.delete_column(u'catalog_toptutorials', u'id')


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
            'Meta': {'object_name': 'Like'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        'catalog.likecfistoreitem': {
            'Meta': {'object_name': 'LikeCfiStoreItem'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            'cfi_store_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.CfiStoreItem']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        'catalog.likemakey': {
            'Meta': {'object_name': 'LikeMakey'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'makey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Makey']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        'catalog.likeproduct': {
            'Meta': {'object_name': 'LikeProduct'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Product']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        'catalog.likeproductdescription': {
            'Meta': {'object_name': 'LikeProductDescription'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'product_description': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.ProductDescription']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        'catalog.likeproductimage': {
            'Meta': {'object_name': 'LikeProductImage'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.ProductImage']"}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Product']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        'catalog.likeproducttutorial': {
            'Meta': {'object_name': 'LikeProductTutorial'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Product']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tutorial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Tutorial']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        'catalog.likeshop': {
            'Meta': {'object_name': 'LikeShop'},
            'added_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Shop']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
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
            'Meta': {'object_name': 'TopMakeys'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'makey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Makey']"})
        },
        'catalog.topproducts': {
            'Meta': {'object_name': 'TopProducts'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Product']"})
        },
        'catalog.topshops': {
            'Meta': {'object_name': 'TopShops'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Shop']"})
        },
        'catalog.toptutorials': {
            'Meta': {'object_name': 'TopTutorials'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tutorial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Tutorial']"})
        },
        'catalog.topusers': {
            'Meta': {'object_name': 'TopUsers'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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