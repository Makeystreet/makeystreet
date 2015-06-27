from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import views.article
import views.auth
import views.embed
import views.makey
import views.maker
import views.review
import views.stats
import views.views
import views.forum

from django.views.generic import TemplateView, RedirectView
from django.core.urlresolvers import reverse_lazy


class RedirectCustom(RedirectView):
    def get_redirect_url(self, **kwargs):
        params = self.kwargs
        name = self.kwargs.get('redirectname')
        if name:
            del params['redirectname']
            return reverse_lazy(name, kwargs=params)
        else:
            raise ValueError, "redirectname not set in RedirectCustom call."


urlpatterns = \
    patterns('',
             url(r'^tangle/$', views.views.tangle),
             url(r'^logout/$', views.auth.logout, name="logout"),
             url(r'^settings/$', views.maker.maker_settings,
                 name="maker_settings"),
             url(r'^dashboard/$', views.maker.user_dashboard,
                 name="user_dashboard"),

             # Basic
             url(r'^$', views.views.landing_page, name='landing_page'),
             url(r'^explore/$', views.views.explore_page, name='explore_page'),
             url(r'^mostawesomepeople/$', views.views.sponsor_page,
                 name="list_new"),
             url(r'^sponsor/$', views.views.sponsor_page, name="list_new"),

             # Search
             url(r'^search/$',  views.views.search, name='search'),
             url(r'^search_autocomplete/$', views.views.search_autocomplete,
                 name='search_autocomplete'),

             # Product
             url(r'^product/(?P<sku>\d+)/$', views.views.product_page,
                 name="product"),

             # Image
             url(r'^image/update/$', views.views.update_image),
             url(r'^image/upload/$', TemplateView.as_view(
                 template_name='catalog/image_upload.html')),
             url(r'^image/sign_image_s3/$', views.views.sign_image_s3,
                 name='sign_image_s3'),
             url(r'^image/sign_file_s3/$', views.views.sign_file_s3,
                 name='sign_file_s3'),
             url(r'^image/update/all/$', views.views.update_all_images),

             # Makey
             url(r'^makey/what/$', TemplateView.as_view(
                 template_name='catalog/what_makey.html'), name="what_makey"),
             url(r'^makey/(?P<makey_id>\d+)/$', views.makey.makey_page_new,
                 name="makey"),
             url(r'^makey_action/$', views.makey.makey_action,
                 name="makey_action"),
             url(r'^makey/(?P<makey_id>\d+)/edit/$',
                 views.makey.edit_makey_page, name="edit_makey"),
             url(r'^makey/(?P<makey_id>\d+)/save/$',
                 views.makey.save_makey, name="save_makey"),
             url(r'^makey/create/$', views.makey.create_makey,
                 name='create_makey'),
             url(r'^makey/add-submodule/(?P<makey_id>\d+)/$',
                 views.makey.makey_add_submodule,
                 name='makey_add_submodule'),
             url(r'^makey/get_instructable/$', views.makey.get_instructable,
                 name='get_instructable'),
             url(r'^makey/all/$', views.makey.all_makeys,
                 name='all_makeys'),
             url(r'^makey/search/$', views.makey.makey_search,
                 name='makey_search'),
             url(r'^user_autocomplete/$', views.views.username_autocomplete,
                 name="user_autocomplete"),
             url(r'^embed/makey/(?P<makey_id>\d+)/$',
                 views.embed.makey_page, name="embed_makey"),

             # embed hierarchy
             url(r'^embed/makey_hierarchy/(?P<makey_id>\d+)/$',
                 views.embed.makey_hierarchy, name="makey_hierarchy"),

             #Collection
             #MiT DIY
             url(r'^wall/mit-di-2015/$',
                 views.makey.collections_mit, name="collection_mit"),
             url(r'^wall/mit-di-2015/all/$',
                 views.makey.collections_mit_all, name="collection_mit_all"),
             #WeHack
             url(r'^wall/wehack/$',
                 views.makey.collections_wehack, name="collection_wehack"),
             url(r'^wall/wehack/all/$',
                 views.makey.collections_wehack_all, name="collection_wehack_all"),
             #SnT IITK
             url(r'^wall/snt15/$',
                 views.makey.collections_snt15, name="collection_snt15"),
             url(r'^wall/snt15/all/$',
                 views.makey.collections_snt15_all, name="collection_snt15_all"),

             url(r'^wall/(?P<collection_id>\d+)/$',
                 views.makey.collection_wall, name="collection_wall"),


             # Space
             url(r'^space/what/$', TemplateView.as_view(
                 template_name='catalog/what_space.html'), name="what_space"),
             url(r'^space/(?P<space_id>\d+)/$', views.views.space_page,
                 name="space"),
             # url(r'^space/create/$', views.create_makey,
             # name='create_space'),
             url(r'^space/all/$', views.views.all_space,
                 name='all_space'),
             url(r'^space/(?P<space_id>[^/]+)/members/$',
                 views.views.space_members_page,
                 name="space_members"),
             url(r'^space/(?P<space_id>[^/]+)/makeys/$',
                 views.views.space_makeys_page,
                 name="space_makey"),
             url(r'^space/(?P<space_id>[^/]+)/inventory/$',
                 views.views.space_inventory_page,
                 name="space_inventory"),
             url(r'^embed/space/(?P<space_id>\d+)/$', views.embed.space_page,
                 name="embed_space"),

             # Maker
             url(r'^maker/what/$', TemplateView.as_view(
                 template_name='catalog/what_maker.html'), name="what_maker"),
             url(r'^onboard/maker/$', views.views.onboard_maker,
                 name="onboard_maker"),
             url(r'^maker/create/$', views.maker.maker_create,
                 name="maker_create"),
             url(r'^maker/replace/$', views.maker.maker_replace,
                 name="maker_replace"),
             url(r'^maker/(?P<username>[^/]+)/$',
                 views.maker.maker_makeys_page,
                 name="maker"),
             url(r'^maker/(?P<username>[^/]+)/makeys/$',
                 views.maker.maker_makeys_page),
             url(r'^maker/(?P<username>[^/]+)/profile/$',
                 views.maker.maker_profile_page,
                 name="maker_profile"),
             url(r'^maker/(?P<username>[^/]+)/insights/$',
                 views.maker.maker_insights_page,
                 name="maker_insights"),
             url(r'^maker/(?P<username>[^/]+)/following/$',
                 views.maker.maker_following_page,
                 name="maker_following"),
             url(r'^maker/(?P<username>[^/]+)/followers/$',
                 views.maker.maker_followers_page,
                 name="maker_followers"),
             url(r'^maker/(?P<username>[^/]+)/reviews/$',
                 views.maker.maker_reviews_page,
                 name="maker_reviews"),

             # Recommendation
             url(r'^recommendation/$', views.article.landing_page,
                 name="reco_landing"),
             url(r'^recommendation/what/$', TemplateView.as_view(
                 template_name='catalog/what_article.html'),
                 name="what_article"),
             url(r'^recommendation/create/$', views.article.create_article,
                 name="create_article"),
             url(r'^recommendation/all/$',
                 views.article.all_tags,
                 name="all_articles"),
             url(r'^recommendation/subscribe/$',
                 views.article.subscribe_page,
                 name="article_subscribe_page"),
             url(r'^recommendation/(?P<article_id>[^/]+)/$',
                 views.article.article_page,
                 name="article_page"),
             url(r'^recommendation/(?P<article_id>[^/]+)/edit/$',
                 views.article.edit_article,
                 name="article_edit_page"),
             url(r'^recommendation/email/submit$', views.article.article_email,
                 name='article_email'),
             url(r'^recommendation/tags/all/$',
                 views.article.all_tags,
                 name="all_tags"),
             url(r'^recommendation/tags/(?P<tag_id>[^/]+)/$',
                 views.article.tag_page,
                 name="tag_page"),
             url(r'^recommendation/by/(?P<username>[^/]+)/$',
                 views.article.user_page,
                 name="article_user_page"),

             url(r'^recommendations/all/$',
                 RedirectView.as_view(
                 url=reverse_lazy('catalog:all_articles')),
                 name="all_articles_2"),
             url(r'^recommendations/by/(?P<username>[^/]+)/$',
                 RedirectCustom.as_view(),
                 kwargs={'redirectname':'catalog:article_user_page'},
                 name="article_user_page_2"),

             # Legacy article urls
             url(r'^article/what/$', RedirectView.as_view(
                 url=reverse_lazy('catalog:what_article')),
                 name="what_article_legacy"),
             url(r'^article/create/$', RedirectView.as_view(
                 url=reverse_lazy('catalog:create_article')),
                 name="create_article_legacy"),
             url(r'^article/all/$', RedirectView.as_view(
                 url=reverse_lazy('catalog:all_articles')),
                 name="all_articles_legacy"),
             url(r'^article/(?P<article_id>[^/]+)/$',
                 RedirectCustom.as_view(),
                 kwargs={'redirectname':'catalog:article_page'},
                 name="article_page_legacy"),
             url(r'^article/email/submit$', RedirectView.as_view(
                 url=reverse_lazy('catalog:article_email')),
                 name='article_email_legacy'),
             url(r'^article/tags/all/$',
                 RedirectView.as_view(
                 url=reverse_lazy('catalog:all_tags')),
                 name="all_tags_legacy"),
             url(r'^article/tags/(?P<tag_id>[^/]+)/$',
                 RedirectCustom.as_view(),
                 kwargs={'redirectname':'catalog:tag_page'},
                 name="tag_page_legacy"),
             url(r'^article/by/(?P<username>[^/]+)/$',
                 RedirectCustom.as_view(),
                 kwargs={'redirectname':'catalog:article_user_page'},
                 name="article_user_page_legacy"),

             # Store
             url(r'^store/all', views.views.all_stores, name="all_stores"),
             url(r'^store/(?P<store>[^/]+)/$', views.views.store_page,
                 name="store_page"),

             # Reviews
             url(r'^review/product/(?P<review_id>\d+)/$',
                 views.review.product_review, name='product_review'),
             url(r'^review/store/(?P<review_id>\d+)/$',
                 views.review.store_review, name='store_review'),
             url(r'^review/space/(?P<review_id>\d+)/$',
                 views.review.space_review, name='space_review'),
             url(r'^review/create/$', views.review.create_review,
                 name='create_review'),
             url(r'review/all/$', views.review.all_reviews, name='all_reviews'),

             # CFI Store
             url(r'^cfistore/$', views.views.cfi_store_page),
             url(r'^cfistore/admin/$', views.views.cfi_store_admin_page),
             url(r'^cfistore/reset/$', views.views.cred_reset),
             url(r'^cfistore/(?P<store>.+)/add/$',
                 views.views.cfi_store_page_add),
             url(r'^cfistore/(?P<store>.+)/remove/$',
                 views.views.cfi_store_page_remove),
             url(r'^cfistore/curatemakey/$', views.makey.curate_makey,
                 name='curate_makey'),
             url(r'^cfistore/staffpick/$', views.makey.staff_pick,
                 name='staff_pick'),
             url(r'^cfistore/staffpick/add/(?P<makey_id>\d+)/$', views.makey.staff_pick_add,
                 name='staff_pick_add'),
             url(r'^cfistore/staffpick/remove/(?P<makey_id>\d+)/$', views.makey.staff_pick_remove,
                 name='staff_pick_remove'),
             url(r'^cfistore/staffpick_reco/$', views.article.staff_pick,
                 name='staff_pick_reco'),
             url(r'^cfistore/staffpick_reco/add/(?P<article_id>\d+)/$', views.article.staff_pick_add,
                 name='staff_pick_reco_add'),
             url(r'^cfistore/staffpick_reco/remove/(?P<article_id>\d+)/$', views.article.staff_pick_remove,
                 name='staff_pick_reco_remove'),
             url(r'^cfistore/collections/(?P<collection_id>\d+)/$', views.makey.collection,
                 name='makey_collection'),
             url(r'^cfistore/collections/(?P<collection_id>\d+)/add/(?P<makey_id>\d+)/$', views.makey.add_makey_to_collection,
                 name='makey_collection_add'),
             url(r'^cfistore/collections/(?P<collection_id>\d+)/remove/(?P<makey_id>\d+)/$', views.makey.remove_makey_from_collection,
                 name='makey_collection_remove'),
             url(r'^cfistore/makey/(?P<makey_id>\d+)/add/(?P<user_id>\d+)/$', views.makey.add_user_to_makey,
                 name='makey_collab_add'),
             url(r'^cfistore/makey/(?P<makey_id>\d+)/remove/(?P<user_id>\d+)/$', views.makey.remove_user_from_makey,
                 name='makey_collab_remove'),

             # Listings
             url(r'^listing/what/$', TemplateView.as_view(
                 template_name='catalog/what_listing.html'),
                 name="what_listing"),
             url(r'^listing/create/$', views.views.create_listing,
                 name='create_listing'),
             url(r'^listing/(?P<listing_id>\d+)/$', views.views.listing,
                 name='listing'),
             url(r'^listing/(?P<listing_id>\d+)/edit/$',
                 views.views.edit_listing, name='edit_listing'),
             url(r'^listing/all/$', views.views.all_listing,
                 name='all_listing'),

             # Questions
             url(r'^question/(?P<question_id>\d+)/$', views.forum.question,
                 name='question'),
             url(r'^question/ask/(?P<makey_id>\d+)/$', views.forum.ask_question,
                 name='ask_question'),
             url(r'^question/comment/$', views.forum.add_comment,
                 name='add_comment'),

             # Support
             url(r'^setasidentical/(?P<product1_id>\d+)/(?P<product2_id>\d+)/$',
                 views.views.identicalcheck,
                 name="backbone"),
             url(r'^setasidentical/(?P<product1_id>\d+)/' +
                 '(?P<product2_id>\d+)/set/$', views.views.setasidentical,
                 name="backbone"),

             # Backend
             url(r'^backend/stats$', views.stats.backend_stats),
             url(r'^backend/stats_old$', views.stats.backend_stats_old),
             url(r'^backend/stats_temp$', views.stats.backend_stats_temp),
             url(r'^backend/makey_diff/(?P<makey_id>\d+)/$',
                 views.stats.makey_diff),

             #Robot.txt
             url(r'^robots\.txt$',
                 TemplateView.as_view(template_name='robots.html')),
             url(r'^privacy-policy/$',
                 TemplateView.as_view(template_name='privacy.html'),
                 name="privacy"),

             url(r'^notification/read/(?P<notif_id>\d+)/$',
                 views.maker.read_notification,
                 name="read_notification"),

             url(r'^(?P<username>[^/]+)/(?P<makey_slug>[^/]+)/search/$', views.makey.search_in_makey_submodules,
                 name="search_in_makey"),
             url(r'^(?P<username>[^/]+)/(?P<makey_slug>[^/]+)/$', views.makey.makey_page_v2_slug,
                 name="makey_new_slug"),
             url(r'^(?P<username>[^/]+)/(?P<makey_slug>[^/]+)/settings/$', views.makey.makey_page_v2_settings,
                 name="makey_new_settings"),
             url(r'^(?P<username>[^/]+)/(?P<makey_slug>[^/]+)/bom/$',
                 views.makey.makey_page_v2_bom,
                 name="makey_new_bom"),
             url(r'^(?P<username>[^/]+)/(?P<makey_slug>[^/]+)/issues/$',
                 views.makey.makey_page_v2_issues,
                 name="makey_new_issues"),
             url(r'^(?P<username>[^/]+)/(?P<makey_slug>[^/]+)/issues/add/$',
                 views.makey.makey_page_v2_issue_add,
                 name="makey_new_issue_add"),
             url(r'^(?P<username>[^/]+)/(?P<makey_slug>[^/]+)/issues/(?P<issue_id>\d+)/$',
                 views.makey.makey_page_v2_issue,
                 name="makey_new_issue"),
             url(r'^(?P<username>[^/]+)/(?P<makey_slug>[^/]+)/(?P<tab>[^/]+)/$', views.makey.makey_page_v2_slug,
                 name="makey_new_tab_slug"),
             url(r'^(?P<username>[^/]+)/(?P<makey_slug>[^/]+)/insights/add/$',
                 views.makey.makey_page_v2_insight_add,
                 name="makey_new_insight_add"),
             url(r'^(?P<username>[^/]+)/(?P<makey_slug>[^/]+)/insights/(?P<insight_id>\d+)/$',
                 views.makey.makey_page_v2_insight_slug,
                 name="makey_new_insight_slug"),
             url(r'^(?P<username>[^/]+)/(?P<makey_slug>[^/]+)/insights/(?P<insight_id>\d+)/edit/$',
                 views.makey.makey_page_v2_insight_edit,
                 name="makey_new_insight_edit"),
             url(r'^(?P<username>[^/]+)/(?P<makey_slug>[^/]+)/image/(?P<gallery_id>\d+)/$',
                 views.makey.makey_page_v2_image_slug,
                 name="makey_new_image_slug"),
             url(r'^(?P<username>[^/]+)/(?P<makey_slug>[^/]+)/discussions/(?P<discussion_id>\d+)/$',
                 views.makey.makey_page_v2_discussion_slug,
                 name="makey_new_discussion_slug"),
             url(r'^(?P<username>[^/]+)/(?P<makey_slug>[^/]+)/docs/add/$',
                 views.makey.makey_page_v2_doc_add,
                 name="makey_new_doc_add"),
             )


urlpatterns += staticfiles_urlpatterns()
