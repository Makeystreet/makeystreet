from django.core.urlresolvers import reverse
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.utils import timezone

from models.core import Note, Makey, Comment
from models.forum import Question, Answer
from models.interactions import Interaction, UserInteraction

from apps.core.models import SendMail, MailType

@receiver(m2m_changed, sender=Makey.notes.through, dispatch_uid="insight_added_to_makey_mailer")
def send_mail_on_insight_added_to_makey(sender, instance, action, model, pk_set, **kwargs):

    if action == "post_add":
        makey = instance
        insight_id =  max(pk_set)
        insight = model.objects.get(id=insight_id)
        host_url = "http://www.makeystreet.com"
        makey_url = host_url + makey.get_absolute_url()
        insight_url = makey_url + "insights/" + str(insight_id) + "/"

        #Mailer code
        global_merge_vars = {
            'MAKEY_URL' : makey_url,
            'MAKEY_NAME' : makey.name,
            'INSIGHT_TITLE' : insight.title,
            'INSIGHT_BODY' : insight.body,
            'INSIGHT_URL' : insight_url
        }

        for collab in makey.collaborators.all():
            if collab != insight.user:
                send_mail = SendMail(to=collab.email,
                                     to_name=collab.first_name,
                                     mail_type=MailType.create_insight_text,
                                     actor_id=insight.user.id,
                                     target_id=insight.id,
                                     subject="[Makeystreet] " + insight.user.first_name +\
                                            " created a new Insight in Makey '" + makey.name + "'!"
                                     )
                send_mail.save(global_merge_vars=global_merge_vars)

@receiver(post_save, sender=Question, dispatch_uid="question_created_mailer")
def send_mail_on_question_created(sender, instance, created=False, **kwargs):

    if created:
        question = instance
        makey = question.makey
        host_url = "http://www.makeystreet.com"
        makey_url = host_url + makey.get_absolute_url()
        question_url = host_url + reverse('catalog:makey_new_discussion_slug',
                                   args=[makey.user.username, makey.slug, question.id]
                                  )

        global_merge_vars = {
            'MAKEY_URL' : makey_url,
            'MAKEY_NAME' : makey.name,
            'QUESTION_TITLE' : question.name,
            'QUESTION_BODY' : question.description,
            'QUESTION_URL' : question_url
        }

        for collab in makey.collaborators.all():
            if not collab.id == question.creator.id:
                send_mail = SendMail(to=collab.email,
                                     to_name=collab.first_name,
                                     mail_type=MailType.create_question,
                                     actor_id=question.creator.id,
                                     target_id=question.id,
                                     subject="[Makeystreet] " + question.creator.first_name +\
                                            " asked a question in Makey '" + makey.name + "'!"
                                     )
                send_mail.save(global_merge_vars=global_merge_vars)

@receiver(post_save, sender=Answer, dispatch_uid="answer_created_mailer")
def send_mail_on_answer_created(sender, instance, created=False, **kwargs):

    if created:
        answer = instance
        question = answer.question
        makey = question.makey
        host_url = "http://www.makeystreet.com"
        makey_url = host_url + makey.get_absolute_url()
        question_url = host_url + reverse('catalog:makey_new_discussion_slug',
                                   args=[makey.user.username, makey.slug, answer.question.id]
                                  )

        global_merge_vars = {
            'MAKEY_URL' : makey_url,
            'MAKEY_NAME' : makey.name,
            'QUESTION_TITLE' : question.name,
            'QUESTION_BODY' : question.description,
            'QUESTION_URL' : question_url,
            'ANSWER_TITLE' : answer.title,
            'ANSWER_BODY' : answer.description,
            'ANSWER_URL' : question_url
        }

        #Creating target list
        target_users = set()
        #question creator
        target_users |= set([question.creator])
        #collaborators
        target_users |= set(question.makey.collaborators.all())
        #Watchers
        target_users |= set([x.user for x in question.makey.makeylikes.all()])
        #Remove the insight creator if present
        target_users.discard(answer.creator)

        for user in target_users:
            send_mail = SendMail(to=user.email,
                                 to_name=user.first_name,
                                 mail_type=MailType.create_answer,
                                 actor_id=answer.creator.id,
                                 target_id=answer.id,
                                 subject="[Makeystreet] " + answer.creator.first_name +\
                                        " has answered a question in Makey '" + makey.name + "'!"
                                 )
            send_mail.save(global_merge_vars=global_merge_vars)

@receiver(m2m_changed, sender=Note.comments.through, dispatch_uid="comment_added_to_insight_mailer")
def send_mail_on_comment_added_to_insight(sender, instance, action, model, pk_set, **kwargs):

    if action == "post_add":
        insight = instance
        comment_id =  max(pk_set)
        comment = model.objects.get(id=comment_id)
        makey = insight.makeynotes.all()[0]
        host_url = "http://www.makeystreet.com"
        makey_url = host_url + makey.get_absolute_url()
        insight_url = makey_url + "insights/" + str(insight.id) + "/"

        #Mailer code
        global_merge_vars = {
            'MAKEY_URL' : makey_url,
            'MAKEY_NAME' : makey.name,
            'INSIGHT_TITLE' : insight.title,
            'INSIGHT_BODY' : insight.body,
            'INSIGHT_URL' : insight_url,
            'COMMENT_BODY' : comment.body
        }

        #Creating target list
        target_users = set()
        #Insight owner
        target_users |= set([insight.user])
        #Everybody in the thread
        target_users |= set([x.user for x in insight.comments.all()])
        #Remove the comment creator from the list
        target_users.discard(comment.user)

        for user in target_users:
            send_mail = SendMail(to=user.email,
                                 to_name=user.first_name,
                                 mail_type=MailType.comment_makey_note,
                                 actor_id=comment.user.id,
                                 target_id=comment.id,
                                 subject="[Makeystreet] " + comment.user.first_name +\
                                        " commented on an Insight in Makey '" + makey.name + "'!"
                                 )
            send_mail.save(global_merge_vars=global_merge_vars)

@receiver(post_save, sender=Comment, dispatch_uid="comment_added_to_question_mailer")
def send_mail_on_comment_added_to_question(sender, instance, created=False, **kwargs):

    if created:
        comment = instance

        if comment.question:
            makey = comment.question.makey
            host_url = "http://www.makeystreet.com"
            makey_url = host_url + makey.get_absolute_url()
            question_url = host_url + reverse('catalog:makey_new_discussion_slug',
                                   args=[makey.user.username, makey.slug, comment.question.id]
                                  )

            global_merge_vars = {
                'MAKEY_URL' : makey_url,
                'MAKEY_NAME' : makey.name,
                'DISCUSSION_URL' : question_url,
                'COMMENT_BODY' : comment.body
            }

            #Creating target list
            target_users = set()
            #question creator
            target_users |= set([comment.question.creator])
            #People on comment thread
            comments_on_question = Comment.objects.filter(question=comment.question)
            target_users |= set([x.user for x in comments_on_question])
            #Remove the creator if present
            target_users.discard(comment.user)

            for user in target_users:
                send_mail = SendMail(to=user.email,
                                     to_name=user.first_name,
                                     mail_type=MailType.comment_makey_question,
                                     actor_id=comment.user.id,
                                     target_id=comment.id,
                                     subject="[Makeystreet] " + comment.user.first_name +\
                                            " commented on a question in Makey '" + makey.name + "'!"
                                     )
                send_mail.save(global_merge_vars=global_merge_vars)

        elif comment.answer:
            makey = comment.answer.question.makey
            host_url = "http://www.makeystreet.com"
            makey_url = host_url + makey.get_absolute_url()
            question_url = host_url + reverse('catalog:makey_new_discussion_slug',
                                   args=[makey.user.username, makey.slug, comment.answer.question.id]
                                  )

            global_merge_vars = {
                'MAKEY_URL' : makey_url,
                'MAKEY_NAME' : makey.name,
                'DISCUSSION_URL' : question_url,
                'COMMENT_BODY' : comment.body
            }

            #Creating target list
            target_users = set()
            #question creator
            target_users |= set([comment.answer.creator])
            #People on comment thread
            comments_on_answer = Comment.objects.filter(answer=comment.answer)
            target_users |= set([x.user for x in comments_on_answer])
            #Remove the creator if present
            target_users.discard(comment.user)

            for user in target_users:
                send_mail = SendMail(to=user.email,
                                     to_name=user.first_name,
                                     mail_type=MailType.comment_makey_answer,
                                     actor_id=comment.user.id,
                                     target_id=comment.id,
                                     subject="[Makeystreet] " + comment.user.first_name +\
                                            " commented on an answer in Makey '" + makey.name + "'!"
                                     )
                send_mail.save(global_merge_vars=global_merge_vars)

