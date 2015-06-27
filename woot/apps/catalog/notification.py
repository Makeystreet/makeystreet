from django.core.urlresolvers import reverse
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.utils import timezone

from models.core import Note, Makey, Comment
from models.forum import Question, Answer
from models.interactions import Interaction, UserInteraction, UserNotification

@receiver(m2m_changed, sender=Makey.notes.through, dispatch_uid="insight_added_to_makey_notification")
def create_notification_on_insight_added_to_makey(sender, instance, action, model, pk_set, **kwargs):

    if action == "post_add":
        makey = instance
        insight_id =  max(pk_set)
        insight = model.objects.get(id=insight_id)

        interaction = UserInteraction(user=insight.user,
                                      event=Interaction.activity_insight_created,
                                      event_id=insight.id,
                                      makey=makey,
                                      added_time=timezone.now())
        interaction.save()

        #Creating target list
        target_users = set()
        #collaborators
        target_users |= set(makey.collaborators.all())
        #Watchers
        target_users |= set([x.user for x in makey.makeylikes.all()])
        #Remove the insight creator if present
        target_users.discard(insight.user)

        for user in target_users:
            notif = UserNotification(user=user, interaction=interaction)
            notif.save()


@receiver(post_save, sender=Question, dispatch_uid="question_created_notification")
def create_notification_on_question_created(sender, instance, created=False, **kwargs):

    if created:
        question = instance

        interaction = UserInteraction(user=question.creator,
                                      event=Interaction.activity_question_created,
                                      event_id=question.id,
                                      makey=question.makey,
                                      added_time=timezone.now())
        interaction.save()

        #Creating target list
        target_users = set()
        #collaborators
        target_users |= set(question.makey.collaborators.all())
        #Watchers
        target_users |= set([x.user for x in question.makey.makeylikes.all()])
        #Remove the insight creator if present
        target_users.discard(question.creator)

        for user in target_users:
            notif = UserNotification(user=user, interaction=interaction)
            notif.save()


@receiver(post_save, sender=Answer, dispatch_uid="answer_created_notification")
def create_notification_on_answer_created(sender, instance, created=False, **kwargs):

    if created:
        answer = instance

        interaction = UserInteraction(user=answer.creator,
                                      event=Interaction.activity_answer_created,
                                      event_id=answer.id,
                                      makey=answer.question.makey,
                                      added_time=timezone.now())
        interaction.save()

        #Creating target list
        target_users = set()
        #question creator
        target_users |= set([answer.question.creator])
        #collaborators
        target_users |= set(answer.question.makey.collaborators.all())
        #Watchers
        target_users |= set([x.user for x in answer.question.makey.makeylikes.all()])
        #Remove the insight creator if present
        target_users.discard(answer.creator)

        for user in target_users:
            notif = UserNotification(user=user, interaction=interaction)
            notif.save()


@receiver(m2m_changed, sender=Note.comments.through, dispatch_uid="comment_added_to_insight_notification")
def create_notification_on_comment_added_to_insight(sender, instance, action, model, pk_set, **kwargs):

    if action == "post_add":
        insight = instance
        comment_id =  max(pk_set)
        comment = model.objects.get(id=comment_id)
        makey = None
        if insight.makeynotes.count() == 1:
          makey = insight.makeynotes.all()[0]

        interaction = UserInteraction(user=comment.user,
                                      event=Interaction.activity_insight_comment_created,
                                      event_id=comment.id,
                                      makey=makey,
                                      added_time=timezone.now())
        interaction.save()

        #Creating target list
        target_users = set()
        #insight owner
        target_users |= set([insight.user])
        #Everybody in the thread
        target_users |= set([x.user for x in insight.comments.all()])
        #Remove the comment creator from the list
        target_users.discard(comment.user)

        for user in target_users:
            notif = UserNotification(user=user, interaction=interaction)
            notif.save()
            print notif

        print target_users
        print interaction


@receiver(post_save, sender=Comment, dispatch_uid="comment_added_to_question_notification")
def create_notification_on_comment_added_to_question(sender, instance, created=False, **kwargs):

    if created:
        comment = instance

        if comment.question:
            interaction = UserInteraction(user=comment.user,
                                          event=Interaction.activity_question_comment_created,
                                          event_id=comment.id,
                                          makey=comment.question.makey,
                                          added_time=timezone.now())
            interaction.save()

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
                notif = UserNotification(user=user, interaction=interaction)
                notif.save()

        elif comment.answer:
            interaction = UserInteraction(user=comment.user,
                                          event=Interaction.activity_answer_comment_created,
                                          event_id=comment.id,
                                          makey=comment.answer.question.makey,
                                          added_time=timezone.now())
            interaction.save()

            #Creating target list
            target_users = set()
            #answer creator
            target_users |= set([comment.answer.creator])
            #People on comment thread
            comments_on_answer = Comment.objects.filter(answer=comment.answer)
            target_users |= set([x.user for x in comments_on_answer])
            #Remove the creator if present
            target_users.discard(comment.user)

            for user in target_users:
                notif = UserNotification(user=user, interaction=interaction)
                notif.save()
