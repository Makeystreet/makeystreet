from django.db import models

from abstract import BaseModel
from core import Product, User, Makey, Tutorial, Shop


class TopProducts(BaseModel):
    product = models.ForeignKey(Product)

    class Meta:
        app_label = 'catalog'
    
    def __unicode__(self):
        return self.product.name


class TopUsers(BaseModel):
    user = models.ForeignKey(User)

    class Meta:
        app_label = 'catalog'
    
    def __unicode__(self):
        return self.user.username


class TopMakeys(BaseModel):
    makey = models.ForeignKey(Makey)
    
    class Meta:
        app_label = 'catalog'
    
    def __unicode__(self):
        return self.makey.name


class TopTutorials(BaseModel):
    tutorial = models.ForeignKey(Tutorial)
    
    class Meta:
        app_label = 'catalog'
    
    def __unicode__(self):
        return self.tutorial.url
    
    
class TopShops(BaseModel):
    shop = models.ForeignKey(Shop)
    
    class Meta:
        app_label = 'catalog'
    
    def __unicode__(self):
        return self.shop.name
