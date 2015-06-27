from django.db import models
from dj.choices import Choices, Choice
from django.contrib.auth.models import User

# from apps.catalog.models.core import Makey, Image, Note, Video, Comment,\
    # ArticleTag

from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.utils import timezone

import os


class MailType(Choices):
    '''
    Choices for mails which are sent to users
    '''

    LIKES = Choices.Group(0)
    like_makey = Choice("Likes a Makey")
    like_makey_image = Choice("Likes a Makey Image")
    like_makey_video = Choice("Likes a Makey Video")
    like_makey_note = Choice("Likes a Makey Note")

    COMMENTS = Choices.Group(100)
    comment_makey = Choice("Comments on a Makey")
    comment_makey_image = Choice("Comments on a Makey Image")
    comment_makey_video = Choice("Comments on a Makey Video")
    comment_makey_note = Choice("Comments on a Makey Note")
    comment_makey_question = Choice("Comments on a Makey Question")
    comment_makey_answer = Choice("Comments on a Makey Answer")

    MISC = Choices.Group(200)
    follow_maker = Choice("Followed a Maker")
    signup_maker = Choice("Maker Signed Up")
    signup_article = Choice("Signed Up For Articles")
    signup_article_user = Choice("Signed Up For Articles From User")

    INSIGHTS = Choices.Group(300)
    create_insight_text = Choice("Insight created")

    QUESTION = Choices.Group(400)
    create_question = Choice("Question created")

    ANSWER = Choices.Group(500)
    create_answer = Choice("Answer created")


class SendMail(models.Model):
    mail_type = models.IntegerField(choices=MailType())
    subject = models.CharField(max_length=250)
    from_email = models.EmailField()

    to_name = models.CharField(max_length=250)
    to = models.EmailField()
    cc = models.EmailField()

    template = models.CharField(max_length=250)
    sent_time = models.DateTimeField(null=True)

    actor_id = models.IntegerField()
    target_id = models.IntegerField()

    class Meta:
        app_label = 'core'

    def save(self, global_merge_vars={}, *args, **kwargs):
        '''
        Following need to be set:
        to - Email Id of person to whom mail should be sent,
        to_name - Name of person to whome mail should be sent,
        mail_type - Type of the mail (see MailType above),
        actor_id - ID of the user who did the action,
        target_id - ID of the object on which the actor did some action
        '''
        self.cc = "Numaan Ashraf<numaan@makeystreet.com>"

        if self.mail_type != MailType.signup_article:
            actor = User.objects.get(id=self.actor_id)

        if self.mail_type != MailType.signup_article_user:
            actor = User.objects.get(id=self.actor_id)

        if self.mail_type == MailType.like_makey:
            self.template = "LikeMakey"
            self.from_email = "Makeystreet " +\
                "Notification<notifications@makeystreet.com>"

        elif self.mail_type == MailType.create_insight_text:
            self.template = "AddInsightText"
            self.from_email = "Makeystreet " +\
                "Notification<notifications@makeystreet.com>"

        elif self.mail_type == MailType.create_question:
            self.template = "AskQuestion"
            self.from_email = "Makeystreet " +\
                "Notification<notifications@makeystreet.com>"

        elif self.mail_type == MailType.create_answer:
            self.template = "AnswerQuestion"
            self.from_email = "Makeystreet " +\
                "Notification<notifications@makeystreet.com>"

        elif self.mail_type == MailType.comment_makey_note:
            self.template = "CommentInsight"
            self.from_email = "Makeystreet " +\
                "Notification<notifications@makeystreet.com>"

        elif self.mail_type == MailType.comment_makey_question:
            self.template = "CommentQuestion"
            self.from_email = "Makeystreet " +\
                "Notification<notifications@makeystreet.com>"

        elif self.mail_type == MailType.comment_makey_answer:
            self.template = "CommentAnswer"
            self.from_email = "Makeystreet " +\
                "Notification<notifications@makeystreet.com>"

        super(SendMail, self).save(*args, **kwargs)
        self.send_mail(global_merge_vars)

    def send_mail(self, global_merge_vars):
        if self.to == "":
            try:
                msg = EmailMessage(subject="[Issue] Email Missing",
                                   from_email="issues@makeystreet.com",
                                   to=["numaan@makeystreet.com"],)
                msg.template_name = "Issue"
                msg.global_merge_vars = {
                    'problem': 'Email ID Missing',
                    'details1': 'SendMail Id: ' + str(self.id),
                    'details2': 'User with missing email: ' + str(self.to_name),
                    'details3': '',
                }
                msg.send()
            except Exception as e:
                print(e)
            return

        try:
            global_merge_vars['USERNAME'] = self.to_name

            # Building actor details
            actor = User.objects.get(id=self.actor_id)
            actor_url = ''.join(['http://www.makeystreet.com',
                                 reverse('catalog:maker',
                                         kwargs={'username': actor.username}
                                         )])
            global_merge_vars['ACTOR_URL'] = actor_url
            global_merge_vars['ACTOR_NAME'] = actor.first_name

            if os.environ.get('DJANGO_SETTINGS_MODULE', '') == 'woot.settings.dev':
                print("From: "+self.from_email)
                print("To: "+self.to)
                print("To Name:"+self.to_name)
                print("CC: "+self.cc)
                print("Subject: "+self.subject)
                print("Mail Type: "+self.mail_type.desc)
                print("Template: "+self.template)
                print(global_merge_vars)
                return

            msg = EmailMessage(subject=self.subject,
                               from_email=self.from_email,
                               to=[self.to_name + "<" + self.to + ">", ],
                               bcc=[self.cc, 'Alex JV<alex@makeystreet.com>'])
            msg.template_name = self.template
            msg.global_merge_vars = global_merge_vars
            msg.send()

            self.sent_time = timezone.now()
            super(SendMail, self).save()
        except Exception as e:
            print(e)
            pass
