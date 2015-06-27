from django.contrib.auth.models import User
from django.db import models
from .core import Makey, Comment
from .abstract import BaseModel
from taggit.managers import TaggableManager

class Milestone(BaseModel):
    makey = models.ForeignKey(Makey, null=True, related_name='milestones')
    title = models.TextField(null=True, blank=False)
    description = models.TextField(null=True, blank=False)
    completed_time = models.DateTimeField(null=True, blank=True)

    class Meta:
         app_label = 'catalog'

    def __unicode__(self):
        return self.makey.name + ' - ' + self.title


class Issue(BaseModel):
    OPEN = 'open'
    CLOSED = 'closed'
    STATUS_CHOICES = (
        (OPEN, 'Open'),
        (CLOSED, 'Closed'),
    )
    makey = models.ForeignKey(Makey, null=True, related_name='issues')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=OPEN)
    last_comment_time = models.DateTimeField(null=True, blank=True)
    comment_count = models.DateTimeField(null=True, blank=True)
    title = models.TextField(null=True)
    owner = models.ForeignKey(User, related_name='issues_owned')
    subscribers = models.ManyToManyField(User, null=True, blank=True)
    assignee = models.ForeignKey(User, null=True, blank=True, related_name='issues_assigned')
    milestone = models.ManyToManyField(Milestone, null=True, blank=True, related_name='issues')
    comments = models.ManyToManyField(Comment, null=True, blank=True)
    closed_time = models.DateTimeField(null=True, blank=True)
    labels = TaggableManager(blank=True)

    class Meta:
        app_label = 'catalog'

    def __unicode__(self):
        return self.makey.name + ' - ' + self.title
