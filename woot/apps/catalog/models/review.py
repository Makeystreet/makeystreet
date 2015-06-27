from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from .abstract import BaseModel
from .core import Product, Shop, Space
# from .interactions import Interaction, UserInteraction


class AbstractReview(BaseModel):
    title = models.CharField(max_length=100)
    review = models.CharField(max_length=100000)
    user = models.ForeignKey(User)
    rating = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)

    class Meta:
        abstract = True
        app_label = 'catalog'

    def unicode(self):
        return self.title

    # def save_user_interaction(self, *args, **kwargs):
        # interaction = UserInteraction(user=self.user,
        #                               event=self.interaction_type,
        #                               event_id=self.id,
        #                               added_time=timezone.now())
        # interaction.save()

    # def delete_user_interaction(self, *args, **kwargs):
        # interaction = UserInteraction.objects.get(user=self.user,
        #                                           event=self.interaction_type,
        #                                           event_id=self.id)
        # interaction.delete()


class ShopReview(AbstractReview):
    shop = models.ForeignKey(Shop, related_name='shop_reviews')
    # interaction_type = Interaction.review_shop

    class Meta:
        app_label = 'catalog'

    def save(self, *args, **kwargs):
        super(ShopReview, self).save(*args, **kwargs)
        # super(ShopReview, self).save_user_interaction()

    def delete(self, *args, **kwargs):
        # super(ShopReview, self).delete_user_interaction()
        super(ShopReview, self).delete(*args, **kwargs)


class ProductReview(AbstractReview):
    product = models.ForeignKey(Product, related_name='product_reviews')
    # interaction_type = Interaction.review_product

    class Meta:
        app_label = 'catalog'

    def save(self, *args, **kwargs):
        super(ProductReview, self).save(*args, **kwargs)
        # super(ProductReview, self).save_user_interaction(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # super(ProductReview, self).delete_user_interaction(*args, **kwargs)
        super(ProductReview, self).delete(*args, **kwargs)


class SpaceReview(AbstractReview):
    space = models.ForeignKey(Space, related_name='space_reviews')
    # interaction_type = Interaction.review_space

    class Meta:
        app_label = 'catalog'

    def save(self, *args, **kwargs):
        super(SpaceReview, self).save(*args, **kwargs)
        # super(SpaceReview, self).save_user_interaction(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # super(SpaceReview, self).delete_user_interaction(*args, **kwargs)
        super(SpaceReview, self).delete(*args, **kwargs)
