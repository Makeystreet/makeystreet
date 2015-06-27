from django.db import models
from django.utils import timezone

from abstract import AbstractVote
from core import Makey, Tutorial
# from interactions import UserInteraction, Interaction
from review import ProductReview, ShopReview, SpaceReview


class VoteProductReview(AbstractVote):
    review = models.ForeignKey(ProductReview)

    class Meta:
        app_label = 'catalog'
        unique_together = (("user", "review"),)

    def __unicode__(self):
        if self.vote:
            return unicode(self.user) + " upvoted " + unicode(self.review)
        else:
            return unicode(self.user) + " downvoted " + unicode(self.review)

    # def __new_user_interaction(self):
    #     if self.vote:
    #         interaction = UserInteraction(
    #             user=self.user,
    #             event=Interaction.upvote_product_review,
    #             event_id=self.id,
    #             added_time=timezone.now())
    #     else:
    #         interaction = UserInteraction(
    #             user=self.user,
    #             event=Interaction.downvote_product_review,
    #             event_id=self.id,
    #             added_time=timezone.now())
    #     interaction.save()

    def save(self, *args, **kwargs):
        same_vote = self.__class__.objects.filter(user=self.user,
                                                  review=self.review,)
        if same_vote.exists():
            previous_vote = same_vote[0]
            previous_vote.delete()
            if previous_vote.vote:
                if self.vote:
                    self.review.votes -= 1
                    self.review.save()
                else:
                    self.review.votes -= 2
                    self.review.save()
                    super(VoteProductReview, self).save(*args, **kwargs)
                    # self.__new_user_interaction()
            else:
                if self.vote:
                    self.review.votes += 2
                    self.review.save()
                    super(VoteProductReview, self).save(*args, **kwargs)
                    # self.__new_user_interaction()
                else:
                    self.review.votes += 1
                    self.review.save()
        else:
            if self.vote:
                self.review.votes += 1
                self.review.save()
            else:
                self.review.votes -= 1
                self.review.save()
            super(VoteProductReview, self).save(*args, **kwargs)
            # self.__new_user_interaction()

    def delete(self, *args, **kwargs):
        if self.vote:
            # interaction = UserInteraction.objects.get(
            #     user=self.user,
            #     event=Interaction.upvote_product_review,
            #     event_id=self.id)
            self.review.votes -= 1
        else:
            # interaction = UserInteraction.objects.get(
            #     user=self.user,
            #     event=Interaction.downvote_product_review,
            #     event_id=self.id)
            self.review.votes += 1
        self.review.save()
        # interaction.delete()

        super(VoteProductReview, self).delete(*args, **kwargs)


class VoteShopReview(AbstractVote):
    review = models.ForeignKey(ShopReview)

    class Meta:
        app_label = 'catalog'
        unique_together = (("user", "review"),)

    def __unicode__(self):
        if self.vote:
            return unicode(self.user) + " upvoted " + unicode(self.review)
        else:
            return unicode(self.user) + " downvoted " + unicode(self.review)

    # def __new_user_interaction(self):
    #     # if self.vote:
    #         # interaction = UserInteraction(
    #         #     user=self.user,
    #         #     event=Interaction.upvote_shop_review,
    #         #     event_id=self.id,
    #         #     added_time=timezone.now())
    #     # else:
    #         # interaction = UserInteraction(
    #         #     user=self.user,
    #         #     event=Interaction.downvote_shop_review,
    #         #     event_id=self.id,
    #         #     added_time=timezone.now())
    #     # interaction.save()

    def save(self, *args, **kwargs):
        same_vote = self.__class__.objects.filter(user=self.user,
                                                  review=self.review,)
        if same_vote.exists():
            previous_vote = same_vote[0]
            previous_vote.delete()
            if previous_vote.vote:
                if self.vote:
                    self.review.votes -= 1
                    self.review.save()
                else:
                    self.review.votes -= 2
                    self.review.save()
                    super(VoteShopReview, self).save(*args, **kwargs)
                    # self.__new_user_interaction()
            else:
                if self.vote:
                    self.review.votes += 2
                    self.review.save()
                    super(VoteShopReview, self).save(*args, **kwargs)
                    # self.__new_user_interaction()
                else:
                    self.review.votes += 1
                    self.review.save()
        else:
            if self.vote:
                self.review.votes += 1
                self.review.save()
            else:
                self.review.votes -= 1
                self.review.save()
            super(VoteShopReview, self).save(*args, **kwargs)
            # self.__new_user_interaction()

    def delete(self, *args, **kwargs):
        if self.vote:
            # interaction = UserInteraction.objects.get(
            #     user=self.user,
            #     event=Interaction.upvote_shop_review,
            #     event_id=self.id)
            self.review.votes -= 1
        else:
            # interaction = UserInteraction.objects.get(
            #     user=self.user,
            #     event=Interaction.downvote_shop_review,
            #     event_id=self.id)
            self.review.votes += 1
        self.review.save()
        # interaction.delete()

        super(VoteShopReview, self).delete(*args, **kwargs)


class VoteSpaceReview(AbstractVote):
    review = models.ForeignKey(SpaceReview)

    class Meta:
        app_label = 'catalog'
        unique_together = (("user", "review"),)

    def __unicode__(self):
        if self.vote:
            return unicode(self.user) + " upvoted " + unicode(self.review)
        else:
            return unicode(self.user) + " downvoted " + unicode(self.review)

    # def __new_user_interaction(self):
    #     if self.vote:
    #         interaction = UserInteraction(
    #             user=self.user,
    #             event=Interaction.upvote_space_review,
    #             event_id=self.id,
    #             added_time=timezone.now())
    #     else:
    #         interaction = UserInteraction(
    #             user=self.user,
    #             event=Interaction.downvote_space_review,
    #             event_id=self.id,
    #             added_time=timezone.now())
    #     interaction.save()

    def save(self, *args, **kwargs):
        same_vote = self.__class__.objects.filter(user=self.user,
                                                  review=self.review,)
        if same_vote.exists():
            previous_vote = same_vote[0]
            previous_vote.delete()
            if previous_vote.vote:
                if self.vote:
                    self.review.votes -= 1
                    self.review.save()
                else:
                    self.review.votes -= 2
                    self.review.save()
                    super(VoteSpaceReview, self).save(*args, **kwargs)
                    # self.__new_user_interaction()
            else:
                if self.vote:
                    self.review.votes += 2
                    self.review.save()
                    super(VoteSpaceReview, self).save(*args, **kwargs)
                    # self.__new_user_interaction()
                else:
                    self.review.votes += 1
                    self.review.save()
        else:
            if self.vote:
                self.review.votes += 1
                self.review.save()
            else:
                self.review.votes -= 1
                self.review.save()
            super(VoteSpaceReview, self).save(*args, **kwargs)
            # self.__new_user_interaction()

    def delete(self, *args, **kwargs):
        if self.vote:
            # interaction = UserInteraction.objects.get(
            #     user=self.user,
            #     event=Interaction.upvote_space_review,
            #     event_id=self.id)
            self.review.votes -= 1
        else:
            # interaction = UserInteraction.objects.get(
            #     user=self.user,
            #     event=Interaction.downvote_space_review,
            #     event_id=self.id)
            self.review.votes += 1
        self.review.save()
        # interaction.delete()

        super(VoteSpaceReview, self).delete(*args, **kwargs)


class VoteMakey(AbstractVote):
    makey = models.ForeignKey(Makey)

    class Meta:
        app_label = 'catalog'
        unique_together = (("user", "makey"),)

    def __unicode__(self):
        if self.vote:
            return unicode(self.user) + " upvoted " + unicode(self.makey)
        else:
            return unicode(self.user) + " downvoted " + unicode(self.makey)

    # def __new_user_interaction(self):
    #     if self.vote:
    #         interaction = UserInteraction(
    #             user=self.user,
    #             event=Interaction.upvote_makey,
    #             event_id=self.id,
    #             added_time=timezone.now())
    #     else:
    #         interaction = UserInteraction(
    #             user=self.user,
    #             event=Interaction.downvote_makey,
    #             event_id=self.id,
    #             added_time=timezone.now())
    #     interaction.save()

    def save(self, *args, **kwargs):
        same_vote = self.__class__.objects.filter(user=self.user,
                                                  makey=self.makey,)
        if same_vote.exists():
            previous_vote = same_vote[0]
            previous_vote.delete()
            if previous_vote.vote:
                if self.vote:
                    self.makey.votes -= 1
                    self.makey.save()
                else:
                    self.makey.votes -= 2
                    self.makey.save()
                    super(VoteMakey, self).save(*args, **kwargs)
                    # self.__new_user_interaction()
            else:
                if self.vote:
                    self.makey.votes += 2
                    self.makey.save()
                    super(VoteMakey, self).save(*args, **kwargs)
                    # self.__new_user_interaction()
                else:
                    self.makey.votes += 1
                    self.makey.save()
        else:
            if self.vote:
                self.makey.votes += 1
                self.makey.save()
            else:
                self.makey.votes -= 1
                self.makey.save()
            super(VoteMakey, self).save(*args, **kwargs)
            # self.__new_user_interaction()

    def delete(self, *args, **kwargs):
        if self.vote:
            # interaction = UserInteraction.objects.get(
            #     user=self.user,
            #     event=Interaction.upvote_makey,
            #     event_id=self.id)
            self.makey.votes -= 1
        else:
            # interaction = UserInteraction.objects.get(
            #     user=self.user,
            #     event=Interaction.downvote_makey,
            #     event_id=self.id)
            self.makey.votes += 1
        self.makey.save()
        # interaction.delete()

        super(VoteMakey, self).delete(*args, **kwargs)


class VoteTutorial(AbstractVote):
    tutorial = models.ForeignKey(Tutorial)

    class Meta:
        app_label = 'catalog'
        unique_together = (("user", "tutorial"),)

    def __unicode__(self):
        if self.vote:
            return unicode(self.user) + " upvoted " + self.tutorial.url
        else:
            return unicode(self.user) + " downvoted " + self.tutorial.url

    # def __save_user_interaction(self):
    #     if self.vote:
    #         # interaction = UserInteraction(
    #         #     user=self.user,
    #         #     event=Interaction.upvote_tutorial,
    #         #     event_id=self.id,
    #         #     added_time=timezone.now())
    #     else:
    #         # interaction = UserInteraction(
    #         #     user=self.user,
    #         #     event=Interaction.downvote_tutorial,
    #         #     event_id=self.id,
    #         #     added_time=timezone.now())
    #     interaction.save()

    def save(self, *args, **kwargs):
        same_vote = self.__class__.objects.filter(user=self.user,
                                                  tutorial=self.tutorial,)
        if same_vote.exists():
            previous_vote = same_vote[0]
            previous_vote.delete()
            if previous_vote.vote:
                if self.vote:
                    self.tutorial.votes -= 1
                    self.tutorial.save()
                else:
                    self.tutorial.votes -= 2
                    self.tutorial.save()
                    super(VoteTutorial, self).save(*args, **kwargs)
                    # self.__save_user_interaction()
            else:
                if self.vote:
                    self.tutorial.votes += 2
                    self.tutorial.save()
                    super(VoteTutorial, self).save(*args, **kwargs)
                    # self.__save_user_interaction()
                else:
                    self.tutorial.votes += 1
                    self.tutorial.save()
        else:
            if self.vote:
                self.tutorial.votes += 1
                self.tutorial.save()
            else:
                self.tutorial.votes -= 1
                self.tutorial.save()
            super(VoteTutorial, self).save(*args, **kwargs)
            # self.__save_user_interaction()

    def delete(self, *args, **kwargs):
        if self.vote:
            # interaction = UserInteraction.objects.get(
            #     user=self.user,
            #     event=Interaction.upvote_tutorial,
            #     event_id=self.id)
            self.tutorial.votes -= 1
        else:
            # interaction = UserInteraction.objects.get(
            #     user=self.user,
            #     event=Interaction.downvote_tutorial,
            #     event_id=self.id)
            self.tutorial.votes += 1
        self.tutorial.save()
        # interaction.delete()

        super(VoteTutorial, self).delete(*args, **kwargs)
