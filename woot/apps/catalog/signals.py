import logging

from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.core.mail import EmailMessage

from allauth.account.signals import user_signed_up, user_logged_in,\
    email_confirmed
from models.core import UserProfile

from apps.core.models import SendMail, MailType

logger = logging.getLogger(__name__)


@receiver(user_signed_up, dispatch_uid='signup')
def create_profile(sender, request, user, sociallogin=None, **kwargs):
    profile = UserProfile(user=user, added_time=user.date_joined)
    profile.save()


@receiver(email_confirmed, dispatch_uid='welcome_mail')
def send_welcome_mail(sender, email_address, **kwargs):
    user = email_address.user
    emailId = user.first_name + " " + user.last_name + "<" +\
        email_address.email + ">"
    msg = EmailMessage(subject="Welcome to Makeystreet",
                       from_email="Alex J V<alex@makeystreet.com>",
                       to=[emailId],
                       cc=['Numaan Ashraf<numaan@makeystreet.com>'],
                       bcc=['Alex JV<alex@makeystreet.com>'])
    msg.template_name = "SignUp"
    msg.use_template_subject = True
    msg.use_template_from = True
    msg.global_merge_vars = {
        'USERNAME': user.first_name,
    }
    msg.preserve_recipients = True
    msg.send()


@receiver(user_logged_in, dispatch_uid='login')
def user_login(request, user, **kwargs):
    logger.info("%s logged in", (user.username))


@receiver(user_logged_out, dispatch_uid='logout')
def user_logout(request, user, **kwargs):
    logger.info('%s logged out', request.user.username)
