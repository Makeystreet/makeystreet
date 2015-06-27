from django.db import models
# from django_facebook.models import FacebookCustomUser as User
from django.contrib.auth.models import User


class BaseModel(models.Model):
    added_time = models.DateTimeField('added time', auto_now_add=True)
    is_enabled = models.BooleanField(default=True)
    score = models.IntegerField(default=0)

    class Meta:
        abstract = True
        app_label = 'catalog'


class AbstractLike(BaseModel):
    user = models.ForeignKey(User)
    fb_like_id = models.CharField(default='-1', max_length=100, null=True,
                                  blank=True)

    class Meta:
        abstract = True
        app_label = 'catalog'


class AbstractVote(BaseModel):
    user = models.ForeignKey(User)
    vote = models.BooleanField(default=True)

    class Meta:
        abstract = True
        app_label = 'catalog'
