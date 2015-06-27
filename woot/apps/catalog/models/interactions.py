from django.db import models
# from django_facebook.models import FacebookCustomUser as User
from django.contrib.auth.models import User
from dj.choices import Choices, Choice

from abstract import BaseModel
from core import Makey

# Important: Don't change the order. The id changes with the order
class Interaction(Choices):
    LIKES = Choices.Group(0)
    like_cfi_store_item = Choice("Likes Cfi Store Item")
    like_makey = Choice("Likes Makey")
    like_product = Choice("Likes Product")
    like_shop = Choice("Likes Shop")
    like_note = Choice("Likes Note")
    like_image = Choice("Likes Image")
    like_video = Choice("Likes Video")
    like_comment = Choice("Likes Comment")
    like_listing = Choice("Likes Listing")
    like_channel = Choice("Likes Channel")

    UPVOTES = Choices.Group(100)
    upvote_makey = Choice("Upvotes Makey")
    upvote_product_review = Choice("Upvotes Product Review")
    upvote_shop_review = Choice("Upvotes Shop Review")
    upvote_tutorial = Choice("Upvotes Tutorial")
    upvote_space_review = Choice("Upvotes Space Review")

    DOWNVOTES = Choices.Group(200)
    downvote_makey = Choice("Downvotes Makey")
    downvote_product_review = Choice("Downvotes Product Review")
    downvote_shop_review = Choice("Downvotes Shop Review")
    downvote_tutorial = Choice("Downvotes Tutorial")
    downvote_space_review = Choice("Downvotes Space Review")

    REVIEWS = Choices.Group(300)
    review_product = Choice("Reviews Product")
    review_shop = Choice("Reviews Shop")
    review_space = Choice("Reviews Space")

    CLICKS = Choices.Group(400)
    click_shopurl = Choice("Clicks Shop Url")

    ACTIVITY = Choices.Group(500)
    activity_insight_created = Choice("New Insight Created")
    activity_question_created = Choice("New Question Created")
    activity_answer_created = Choice("New Answer Created")
    activity_insight_comment_created = Choice("New Comment on an Insight")
    activity_question_comment_created = Choice("New Comment on a Question")
    activity_answer_comment_created = Choice("New Comment on an Answer")


class UserInteraction(BaseModel):
    user = models.ForeignKey(User)
    event = models.IntegerField(choices=Interaction())
    # This stores id of the relation about which we have stored an event here,
    # for ex. LikeShop.id for Interaction.like_store
    event_id = models.IntegerField()
    # makey_id = models.IntegerField(null=True)
    makey = models.ForeignKey(Makey, null= True, related_name='interactions')

    class Meta:
        app_label = 'catalog'

    def __unicode__(self):
        return unicode(self.user) + " " +\
            Interaction.name_from_id(self.event) + " " + unicode(self.event_id)

    def save(self, *args, **kwargs):
        print(self)
        super(UserInteraction, self).save(*args, **kwargs)


class UserNotification(BaseModel):
    user = models.ForeignKey(User)
    interaction = models.ForeignKey(UserInteraction)
    read = models.BooleanField(default=False)

    class Meta:
        app_label = 'catalog'
        unique_together = (("user", "interaction"),)

    def __unicode__(self):
        return unicode(self.user) + " " +\
            Interaction.name_from_id(self.interaction.event) + " " + unicode(self.interaction.event_id)
