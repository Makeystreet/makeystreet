from django.conf.urls import patterns, include, url
from tastypie.api import Api

from api import *


v1_api = Api(api_name='v1')

v1_api.register(MyTagResource())
v1_api.register(UserProfileResource())
v1_api.register(MakeyResource())
v1_api.register(UserResource())
v1_api.register(LikeMakeyResource())
v1_api.register(TestResource())
v1_api.register(CommentResource())
v1_api.register(ProductResource())
v1_api.register(NoteResource())
v1_api.register(Note2Resource())
v1_api.register(DocumentationResource())
v1_api.register(TextDocumentationResource())
v1_api.register(ImageResource())
v1_api.register(LocationResource())
v1_api.register(ShopResource())
v1_api.register(VideoResource())
v1_api.register(StepResource())
v1_api.register(FileResource())

# product page resources
v1_api.register(ProductResourceProductPage())
v1_api.register(MakeyResourceProductPage())
v1_api.register(TutorialResourceProductPage())
v1_api.register(ShopUrlResourceProductPage())
v1_api.register(ImageResourceProductPage())
v1_api.register(DescriptionResourceProductPage())
v1_api.register(LikeResourceProductPage())
v1_api.register(ProductReviewResourceProductPage())
v1_api.register(VoteProductReviewResource())
v1_api.register(VoteTutorialResource())
v1_api.register(VoteMakeyResource())

# Landing page resources
v1_api.register(TopProductsResourceLandingPage())
v1_api.register(ProductResourceLandingPage())
v1_api.register(ShopResourceLandingPage())
v1_api.register(TopUsersResourceLandingPage())
v1_api.register(TopUsersResourceRecoSubPage())
v1_api.register(TopShopsResourceLandingPage())
v1_api.register(TopMakeysResourceLandingPage())
v1_api.register(TopSpacesResource())
v1_api.register(TopTagsResource())

#Cfi Store Resources
v1_api.register(LikeCfiStoreItemResource())
v1_api.register(CfiStoreItemResource())
v1_api.register(CfiStoreItemFullResource())

#Likes
v1_api.register(LikeShopResource())
v1_api.register(LikeNoteResource())
v1_api.register(LikeImageResource())
v1_api.register(LikeVideoResource())
v1_api.register(LikeCommentResource())
v1_api.register(LikeArticleResource())

#Store Page Resoureces
v1_api.register(ProductShopUrlResource())
v1_api.register(ShopReviewResource())
v1_api.register(VoteShopReviewResource())
v1_api.register(ShopResourceProductPage())

#User Interactions
v1_api.register(UserInteractionResource())
v1_api.register(LikeCfiStoreItemWithProductResource())
v1_api.register(LikeProductResourceWithProduct())
v1_api.register(LikeShopWithShopResource())
v1_api.register(VoteMakeyWithMakeyResource())
v1_api.register(TutorialResource())
v1_api.register(VoteTutorialWithTutorialResource())
v1_api.register(ProductReviewResource())
v1_api.register(VoteProductReviewWithProductResource())
v1_api.register(ShopReviewWithShopResource())
v1_api.register(VoteShopReviewWithReviewResource())
v1_api.register(ShopUrlClicks())

#Makey Page
v1_api.register(NewUserResource())
v1_api.register(NewProductResource())
v1_api.register(ProductResourceMakeyPage())
v1_api.register(FavoriteMakeyResource())

#Maker Page
v1_api.register(MakeyResourceMakerPage())
v1_api.register(SpaceResourceMakerPage())

#Search Page
v1_api.register(MakeyResourceSearchPage())

# Space Page
v1_api.register(SpaceResource())
v1_api.register(SpaceReviewResource())
v1_api.register(VoteSpaceReviewResource())
v1_api.register(InventoryResource())
v1_api.register(NewInventoryResource())

#Article Page
v1_api.register(ArticleResource())
v1_api.register(TagResource())
v1_api.register(LikeChannelResource())

#Listing
v1_api.register(ListingResource())
v1_api.register(LikeListingResource())

# Send Mail
# v1_api.register(SendMailResource())

# Forum
v1_api.register(QuestionResource())
v1_api.register(AnswerResource())


urlpatterns = patterns('',
                       url(r'', include(v1_api.urls)),
                       )
