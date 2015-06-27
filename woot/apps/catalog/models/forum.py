from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from tinymce.models import HTMLField

class Question(models.Model):
    '''
    Question has title and description
    '''
    name = models.CharField(max_length=255)
    description = HTMLField()
    views = models.IntegerField(blank=True, default=0)
    closed = models.BooleanField(blank=True, default=False)

    creator = models.ForeignKey(User, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    accepted_answer = models.ForeignKey('Answer', null=True, blank=True,
                                        default=None, related_name='answer_of')
    accepted_time = models.DateTimeField(null=True, blank=True, default=None)

    makey = models.ForeignKey('Makey')

    class Meta:
        app_label = 'catalog'

    def num_answers(self):
        return self.answer_set.count()

    def latest_answer(self):
        return self.answer_set.order_by("created")[0]

    def get_accepted_answer(self):
        return self.accepted_answer

    def has_accepted_answer(self):
        return True if self.accepted_answer else False

    def increase_views(self):
        self.views += 1
        self.save()

    def save_from_form(self, form, creator, makey):
        self.name = form.cleaned_data['name']
        self.description = form.cleaned_data['description']
        self.creator = creator
        self.makey = makey
        self.save()

    def __unicode__(self):
        return unicode(self.creator) + ' - ' + self.name


class AnswerManager(models.Manager):
    def search_content_in_makey(self, makey, query):
        if not query:
            return super(AnswerManager, self).none()
        return super(AnswerManager, self).\
            filter(question__in=makey.question_set.all()).\
            filter(models.Q(title__icontains=query) |
                   models.Q(description__icontains=query))


class Answer(models.Model):
    '''
    Answer has possible answers
    '''
    title = models.CharField(max_length=255, null=True, blank=True)
    description = HTMLField()
    question = models.ForeignKey(Question)

    creator = models.ForeignKey(User, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = AnswerManager()

    class Meta:
        app_label = 'catalog'
        ordering = ['-created']

    def save_from_form(self, form, creator, question):
        self.title = form.cleaned_data['title']
        self.description = form.cleaned_data['description']
        self.question = question
        self.creator = creator
        self.save()

    def __unicode__(self):
        tail = '...' if len(self.description) > 50 else ''
        return self.description[:50] + tail

