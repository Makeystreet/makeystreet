from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse

from abstract import AbstractLike
from core import Product, ProductImage, Makey, Tutorial, Shop,\
    ProductDescription, Note, Image, Video, Comment, Listing,\
    ArticleTag, Article
# from interactions import UserInteraction, Interaction
from misc import CfiStoreItem

from woot.apps.core.models import MailType, SendMail

from django.core.exceptions import ValidationError


class Like(AbstractLike):
    class Meta:
        app_label = 'catalog'

    def __unicode__(self):
        return self.user.name


class LikeProductImage(AbstractLike):
    product = models.ForeignKey(Product)
    image = models.ForeignKey(ProductImage)

    class Meta:
        app_label = 'catalog'
        unique_together = (("user", "image"),)

    def __unicode__(self):
        return unicode(self.product)


class LikeMakey(AbstractLike):
    makey = models.ForeignKey(Makey, related_name="makeylikes")

    class Meta:
        app_label = 'catalog'
        unique_together = (("user", "makey"),)

    def __unicode__(self):
        return unicode(self.user) + " likes " + unicode(self.makey)

    def save(self, *args, **kwargs):
        if self.fb_like_id != '-1':
            super(LikeMakey, self).save(*args, **kwargs)
            return
        super(LikeMakey, self).full_clean(*args, **kwargs)
        super(LikeMakey, self).save(*args, **kwargs)

        # interaction = UserInteraction(user=self.user,
        #                               event=Interaction.like_makey,
        #                               event_id=self.id,
        #                               added_time=timezone.now())
        # interaction.save()

        # global_merge_vars = {
        #     'MAKEY_URL' : ''.join(['http://www.makeystreet.com',
        #                              reverse('catalog:makey',
        #                                      kwargs={'makey_id': self.makey.id}
        #                                      )]),
        #     'MAKEY_NAME' : self.makey.name
        # }

        # for collab in self.makey.collaborators.all():
        #     send_mail = SendMail(to=collab.email,
        #                          to_name=collab.first_name,
        #                          mail_type=MailType.like_makey,
        #                          actor_id=self.user.id,
        #                          target_id=self.makey.id,
        #                          subject="[Makeystreet] " + self.user.first_name +\
        #                                 " likes your Makey '" + self.makey.name + "'!"
        #                          )
        #     send_mail.save(global_merge_vars=global_merge_vars)

    def validate_unique(self, *args, **kwargs):
        same_like = self.__class__.objects.filter(user=self.user,
                                                  makey=self.makey,)
        if same_like.exists():
            same_like[0].delete()
            raise ValidationError(unicode(self.user) + " already likes " +
                                  unicode(self.makey))
        super(LikeMakey, self).validate_unique(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # interaction = UserInteraction.objects.get(user=self.user,
        #                                           event=Interaction.like_makey,
        #                                           event_id=self.id)
        # interaction.delete()
        super(LikeMakey, self).delete(*args, **kwargs)


class LikeProductTutorial(AbstractLike):
    product = models.ForeignKey(Product)
    tutorial = models.ForeignKey(Tutorial)

    class Meta:
        app_label = 'catalog'
        unique_together = (("user", "tutorial", "product"),)

    def __unicode__(self):
        return unicode(self.tutorial)


class LikeProductDescription(AbstractLike):
    product_description = models.ForeignKey(ProductDescription)

    class Meta:
        app_label = 'catalog'
        unique_together = (("user", "product_description"),)

    def __unicode__(self):
        return self.product_description.product.name


class LikeCfiStoreItem(AbstractLike):
    cfi_store_item = models.ForeignKey(CfiStoreItem)

    class Meta:
        app_label = 'catalog'
        unique_together = (("user", "cfi_store_item"),)

    def __unicode__(self):
        return unicode(self.user) + " likes " + unicode(self.cfi_store_item)

    def save(self, *args, **kwargs):
        # Calls full_clean() which calls validate_unique()
        super(LikeCfiStoreItem, self).full_clean(*args, **kwargs)

        # Add like to original product also
        same_like = LikeProduct.objects.filter(user=self.user,
                                               product=self.cfi_store_item.item)
        if not same_like.exists():
            like_product = LikeProduct(user=self.user,
                                       product=self.cfi_store_item.item,
                                       added_time=self.added_time)
            like_product.save()

        super(LikeCfiStoreItem, self).save(*args, **kwargs)

        # Increasing CFI Store Item Score
        self.cfi_store_item.score += 1
        self.cfi_store_item.save()

        # interaction = UserInteraction(user=self.user,
        #                               event=Interaction.like_cfi_store_item,
        #                               event_id=self.id,
        #                               added_time=timezone.now())
        # interaction.save()

    def validate_unique(self, *args, **kwargs):
        same_like = self.__class__.objects.filter(user=self.user,
                                                  cfi_store_item=
                                                  self.cfi_store_item,)
        if same_like.exists():
            same_like[0].delete()

            same_like = LikeProduct.objects.filter(user=self.user,
                                                   product=
                                                   self.cfi_store_item.item,)
            same_like[0].delete()

            raise ValidationError(unicode(self.user) + " already likes " +
                                  unicode(self.cfi_store_item))
        super(LikeCfiStoreItem, self).validate_unique(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # interaction = UserInteraction.objects.get(user=self.user,
        #                                           event=Interaction.
        #                                           like_cfi_store_item,
        #                                           event_id=self.id)
        # interaction.delete()

        self.cfi_store_item.score -= 1
        self.cfi_store_item.save()

        super(LikeCfiStoreItem, self).delete(*args, **kwargs)


class LikeProduct(AbstractLike):
    product = models.ForeignKey(Product)

    class Meta:
        app_label = 'catalog'
        unique_together = (("user", "product"),)

    def __unicode__(self):
        return unicode(self.user) + " likes " + unicode(self.product)

    def save(self, *args, **kwargs):
        super(LikeProduct, self).full_clean(*args, **kwargs)
        super(LikeProduct, self).save(*args, **kwargs)

        # interaction = UserInteraction(user=self.user,
        #                               event=Interaction.like_product,
        #                               event_id=self.id,
        #                               added_time=timezone.now())
        # interaction.save()

    def validate_unique(self, *args, **kwargs):
        same_like = self.__class__.objects.filter(user=self.user,
                                                  product=self.product,)
        if same_like.exists():
            same_like[0].delete()
            raise ValidationError(unicode(self.user) + " already likes " +
                                  unicode(self.product))
        super(LikeProduct, self).validate_unique(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # interaction = UserInteraction.objects.get(user=self.user,
        #                                           event=
        #                                           Interaction.like_product,
        #                                           event_id=self.id)
        # interaction.delete()
        super(LikeProduct, self).delete(*args, **kwargs)


class LikeArticle(AbstractLike):
    article = models.ForeignKey(Article)

    class Meta:
        app_label = 'catalog'
        unique_together = (("user", "article"),)

    def __unicode__(self):
        return unicode(self.user) + " likes " + unicode(self.article)

    def save(self, *args, **kwargs):
        super(LikeArticle, self).full_clean(*args, **kwargs)
        super(LikeArticle, self).save(*args, **kwargs)

    def validate_unique(self, *args, **kwargs):
        same_like = self.__class__.objects.filter(user=self.user,
                                                  article=self.article,)
        if same_like.exists():
            same_like[0].delete()
            raise ValidationError(unicode(self.user) + " already likes " +
                                  unicode(self.article))
        super(LikeArticle, self).validate_unique(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(LikeArticle, self).delete(*args, **kwargs)


class LikeShop(AbstractLike):
    shop = models.ForeignKey(Shop)

    class Meta:
        app_label = 'catalog'
        unique_together = (("user", "shop"),)

    def __unicode__(self):
        return unicode(self.user) + " likes " + unicode(self.shop)

    def save(self, *args, **kwargs):
        super(LikeShop, self).full_clean(*args, **kwargs)
        super(LikeShop, self).save(*args, **kwargs)

        # interaction = UserInteraction(user=self.user,
        #                               event=Interaction.like_shop,
        #                               event_id=self.id,
        #                               added_time=timezone.now())
        # interaction.save()

    def validate_unique(self, *args, **kwargs):
        same_like = self.__class__.objects.filter(user=self.user,
                                                  shop=self.shop,)
        if same_like.exists():
            same_like[0].delete()
            raise ValidationError(unicode(self.user) + " already likes " +
                                  unicode(self.shop))
        super(LikeShop, self).validate_unique(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # interaction = UserInteraction.objects.get(user=self.user,
        #                                           event=Interaction.like_shop,
        #                                           event_id=self.id)
        # interaction.delete()
        super(LikeShop, self).delete(*args, **kwargs)


class LikeNote(AbstractLike):
    note = models.ForeignKey(Note)

    class Meta:
        app_label = 'catalog'
        unique_together = (("user", "note"),)

    def __unicode__(self):
        return unicode(self.user) + " likes " + unicode(self.note)

    def save(self, *args, **kwargs):
        super(LikeNote, self).full_clean(*args, **kwargs)
        super(LikeNote, self).save(*args, **kwargs)

        self.note.likes_count += 1
        self.note.save()

        # interaction = UserInteraction(user=self.user,
        #                               event=Interaction.like_note,
        #                               event_id=self.id,
        #                               added_time=timezone.now())
        # interaction.save()

        # send_mail = SendMail(to=self.note.user.email,
        #                      to_name=self.note.user.first_name,
        #                      mail_type=MailType.like_makey_note,
        #                      actor_id=self.user.id,
        #                      target_id=self.note.id,
        #                      )
        # send_mail.save()

    def validate_unique(self, *args, **kwargs):
        same_like = self.__class__.objects.filter(user=self.user,
                                                  note=self.note,)
        if same_like.exists():
            same_like[0].delete()
            raise ValidationError(unicode(self.user) + " already likes " +
                                  unicode(self.note))
        super(LikeNote, self).validate_unique(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # interaction = UserInteraction.objects.get(user=self.user,
        #                                           event=Interaction.like_note,
        #                                           event_id=self.id)
        # interaction.delete()

        self.note.likes_count -= 1
        self.note.save()

        super(LikeNote, self).delete(*args, **kwargs)


class LikeImage(AbstractLike):
    image = models.ForeignKey(Image)

    class Meta:
        app_label = 'catalog'
        unique_together = (("user", "image"),)

    def __unicode__(self):
        return unicode(self.user) + " likes " + unicode(self.image)

    def save(self, *args, **kwargs):
        super(LikeImage, self).full_clean(*args, **kwargs)
        super(LikeImage, self).save(*args, **kwargs)

        self.image.likes_count += 1
        self.image.save()

        # interaction = UserInteraction(user=self.user,
        #                               event=Interaction.like_image,
        #                               event_id=self.id,
        #                               added_time=timezone.now())
        # interaction.save()

        # for collab in self.image.makeyimages.first().collaborators.all():
        #     send_mail = SendMail(to=collab.email,
        #                          to_name=collab.first_name,
        #                          mail_type=MailType.like_makey_image,
        #                          actor_id=self.user.id,
        #                          target_id=self.image.id,
        #                          )
        #     send_mail.save()

    def validate_unique(self, *args, **kwargs):
        same_like = self.__class__.objects.filter(user=self.user,
                                                  image=self.image,)
        if same_like.exists():
            same_like[0].delete()
            raise ValidationError(unicode(self.user) + " already likes " +
                                  unicode(self.image))
        super(LikeImage, self).validate_unique(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # interaction = UserInteraction.objects.get(user=self.user,
        #                                           event=Interaction.like_image,
        #                                           event_id=self.id)
        # interaction.delete()

        self.image.likes_count -= 1
        self.image.save()

        super(LikeImage, self).delete(*args, **kwargs)


class LikeVideo(AbstractLike):
    video = models.ForeignKey(Video)

    class Meta:
        app_label = 'catalog'
        unique_together = (("user", "video"),)

    def __unicode__(self):
        return unicode(self.user) + " likes " + unicode(self.video)

    def save(self, *args, **kwargs):
        super(LikeVideo, self).full_clean(*args, **kwargs)
        super(LikeVideo, self).save(*args, **kwargs)

        self.video.likes_count += 1
        # self.video.save()

        # interaction = UserInteraction(user=self.user,
        #                               event=Interaction.like_video,
        #                               event_id=self.id,
        #                               added_time=timezone.now())
        # interaction.save()

        # for collab in self.video.makeyvideos.first().collaborators.all():
        #     send_mail = SendMail(to=collab.email,
        #                          to_name=collab.first_name,
        #                          mail_type=MailType.like_makey_video,
        #                          actor_id=self.user.id,
        #                          target_id=self.video.id,
        #                          )
        #     send_mail.save()

    def validate_unique(self, *args, **kwargs):
        same_like = self.__class__.objects.filter(user=self.user,
                                                  video=self.video,)
        if same_like.exists():
            same_like[0].delete()
            raise ValidationError(unicode(self.user) + " already likes " +
                                  unicode(self.video))
        super(LikeVideo, self).validate_unique(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # interaction = UserInteraction.objects.get(user=self.user,
        #                                           event=Interaction.like_video,
        #                                           event_id=self.id)
        # interaction.delete()

        self.video.likes_count -= 1
        self.video.save()

        super(LikeVideo, self).delete(*args, **kwargs)


class LikeComment(AbstractLike):
    comment = models.ForeignKey(Comment)

    class Meta:
        app_label = 'catalog'
        unique_together = (("user", "comment"),)

    def __unicode__(self):
        return unicode(self.user) + " likes " + unicode(self.comment)

    def save(self, *args, **kwargs):
        super(LikeComment, self).full_clean(*args, **kwargs)
        super(LikeComment, self).save(*args, **kwargs)

        self.comment.likes_count += 1
        self.comment.save()

        # interaction = UserInteraction(user=self.user,
        #                               event=Interaction.like_comment,
        #                               event_id=self.id,
        #                               added_time=timezone.now())
        # interaction.save()

    def validate_unique(self, *args, **kwargs):
        same_like = self.__class__.objects.filter(user=self.user,
                                                  comment=self.comment,)
        if same_like.exists():
            same_like[0].delete()
            raise ValidationError(unicode(self.user) + " already likes " +
                                  unicode(self.comment))
        super(LikeComment, self).validate_unique(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # interaction = UserInteraction.objects.get(user=self.user,
        #                                           event=
        #                                           Interaction.like_comment,
        #                                           event_id=self.id)
        # interaction.delete()

        self.comment.likes_count -= 1
        self.comment.save()

        super(LikeComment, self).delete(*args, **kwargs)


class LikeListing(AbstractLike):
    listing = models.ForeignKey(Listing)

    class Meta:
        app_label = 'catalog'
        unique_together = (("user", "listing"),)

    def __unicode__(self):
        return unicode(self.user) + " likes " + unicode(self.listing)

    def save(self, *args, **kwargs):
        super(LikeListing, self).full_clean(*args, **kwargs)
        super(LikeListing, self).save(*args, **kwargs)

        self.listing.likes_count += 1
        self.listing.save()

        # interaction = UserInteraction(user=self.user,
        #                               event=Interaction.like_listing,
        #                               event_id=self.id,
        #                               added_time=timezone.now())
        # interaction.save()

    def validate_unique(self, *args, **kwargs):
        same_like = self.__class__.objects.filter(user=self.user,
                                                  listing=self.listing,)
        if same_like.exists():
            same_like[0].delete()
            raise ValidationError(unicode(self.user) + " already likes " +
                                  unicode(self.listing))
        super(LikeListing, self).validate_unique(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # interaction = UserInteraction.objects.get(user=self.user,
        #                                           event=
        #                                           Interaction.like_listing,
        #                                           event_id=self.id)
        # interaction.delete()

        self.listing.likes_count -= 1
        self.listing.save()

        super(LikeListing, self).delete(*args, **kwargs)


class LikeChannel(AbstractLike):
    channel = models.ForeignKey(ArticleTag)

    class Meta:
        app_label = 'catalog'
        unique_together = (("user", "channel"),)

    def __unicode__(self):
        return unicode(self.user) + " likes " + unicode(self.channel)

    def save(self, *args, **kwargs):
        super(LikeChannel, self).full_clean(*args, **kwargs)
        super(LikeChannel, self).save(*args, **kwargs)

        self.channel.likes_count += 1
        self.channel.save()

        # interaction = UserInteraction(user=self.user,
        #                               event=Interaction.like_channel,
        #                               event_id=self.id,
        #                               added_time=timezone.now())
        # interaction.save()

    def validate_unique(self, *args, **kwargs):
        same_like = self.__class__.objects.filter(user=self.user,
                                                  channel=self.channel,)
        if same_like.exists():
            same_like[0].delete()
            raise ValidationError(unicode(self.user) + " already likes " +
                                  unicode(self.channel))
        super(LikeChannel, self).validate_unique(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # interaction = UserInteraction.objects.get(user=self.user,
        #                                           event=
        #                                           Interaction.like_channel,
        #                                           event_id=self.id)
        # interaction.delete()

        self.channel.likes_count -= 1
        self.channel.save()

        super(LikeChannel, self).delete(*args, **kwargs)
