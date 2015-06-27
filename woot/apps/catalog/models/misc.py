from django.db import models

from abstract import BaseModel
from core import Location, Product, User


class ToIndexStore(models.Model):
    name = models.CharField(max_length = 200)
    description = models.CharField(max_length = 100, blank = True, )
    url = models.URLField(max_length = 200)
    location = models.ForeignKey(Location)
    added_time = models.DateTimeField('added time')
    
    class Meta:
        app_label = 'catalog'
    
    def __unicode__(self):
        return self.url
    

class EmailCollect(models.Model):
    email = models.EmailField(max_length = 30)

    class Meta:
        app_label = 'catalog'
    
    def __unicode__(self):
        return self.email


class ListItem(BaseModel):
    note = models.CharField(max_length = 500)
    product = models.ForeignKey(Product)
    createdby = models.ForeignKey(User)

    class Meta:
        app_label = 'catalog'
    
    def __unicode__(self):
        return self.product.name


class List(BaseModel):
    name = models.CharField(max_length = 100)
    is_private = models.BooleanField() # 1 if private, 0 if public
    
    owner = models.ForeignKey(User, related_name = "owner")
    
    access = models.ManyToManyField(User, related_name = "access") # this is relevant for private lists
    items = models.ManyToManyField(ListItem)

    class Meta:
        app_label = 'catalog'
    
    def __unicode__(self):
        return self.name, "-", self.owner 


class ListGroup(BaseModel):
    name = models.CharField(max_length = 100)
    
    lists = models.ManyToManyField(List)

    class Meta:
        app_label = 'catalog'
    
    

class SearchLog(models.Model):
    term = models.CharField(max_length = 100)
    time = models.DateTimeField('searched date')
    
    user = models.ForeignKey(User, blank = True, null = True)

    class Meta:
        app_label = 'catalog'
    
    def __unicode__(self):
        return self.term


class LogIdenticalProduct(models.Model):
    user = models.ForeignKey(User)
    product1 = models.ForeignKey(Product, related_name = "product1")
    product2 = models.ForeignKey(Product, related_name = "product2")
    added_time = models.DateTimeField('logged date')
    
    class Meta:
        app_label = 'catalog'
    
    def __unicode__(self):
        return self.user

class CfiStoreItem(BaseModel):
    item = models.OneToOneField(Product)
    likers = models.ManyToManyField(User, through = "LikeCfiStoreItem", related_name = "cfi_store_item_likes")

    class Meta:
        app_label = 'catalog'

    def __unicode__(self):
        return self.item.name