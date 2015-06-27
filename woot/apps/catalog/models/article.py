from django.contrib.auth.models import User
from django.db import models

from abstract import BaseModel
from core import ArticleTag
from woot.apps.core.models import SendMail, MailType


class ArticleEmail(BaseModel):
    email = models.EmailField(max_length=100)
    tag = models.ForeignKey(ArticleTag, related_name='email_subscriptions', null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    temp_id = models.CharField(max_length=50)

    class Meta:
        app_label = 'catalog'

    def __unicode__(self):
        if self.tag:
            return self.email + ' subscribed for ' + self.tag.name
        if self.user:
            return self.email + ' subscribed for ' + self.user.first_name + ' ' + self.user.last_name

    def save(self, *args, **kwargs):
        super(ArticleEmail, self).save(*args, **kwargs)

        # Generally, actor_id is set to user_id.
        # Since, we don't expect the user to be already registered in this
        # method, setting actor_id to self.id
        if self.tag:
            username = self.email[:self.email.find('@')]
            # send_mail = SendMail(to=self.email,
            #                      to_name=username,
            #                      mail_type=MailType.signup_article,
            #                      actor_id=self.id,
            #                      target_id=self.tag.id,
            #                      )
            # send_mail.save()
        if self.user:
            username = self.email[:self.email.find('@')]
            # send_mail = SendMail(to=self.email,
            #                      to_name=username,
            #                      mail_type=MailType.signup_article_user,
            #                      actor_id=self.id,
            #                      target_id=self.user.id,
            #                      )
            # send_mail.save()
