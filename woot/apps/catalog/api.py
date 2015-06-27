from datetime import datetime

from django.conf.urls import url
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from tastypie import fields
from tastypie.authorization import Authorization, ReadOnlyAuthorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpForbidden
from tastypie.resources import ModelResource
from tastypie.throttle import BaseThrottle
from tastypie.utils import trailing_slash

# from allauth.socialaccount.models import SocialAccount

import models.article
import models.core
import models.top
import models.vote
import models.like
import models.forum

from views.helper import is_admin, check_private_access

from apps.core.models import SendMail
import unicodedata
import operator
import string

from opengraph import OpenGraph
from urllib2 import urlopen, Request
import json

from django.db.models import Count
from django.db.models import Q

# Taggit
from taggit.models import Tag


from apps.catalog.views.helper import get_makey_activities,\
    time_elapsed
from woot.apps.catalog.models.interactions import Interaction

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


# allow only collaborators and ADMINS to access private makeys
class MakeyAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        allowed = []

        for obj in object_list:
            if obj.is_private:
                if bundle.request.user in obj.collaborators.all()\
                        or is_admin(bundle.request):
                    allowed.append(obj)
            else:
                allowed.append(obj)

        return allowed

    def read_detail(self, object_list, bundle):
        if bundle.obj.is_private:
            if bundle.request.user in bundle.obj.collaborators.all()\
                    or is_admin(bundle.request):
                    return True
            else:
                return False
        return True

    def update_list(self, object_list, bundle):
        allowed = []

        for obj in object_list:
            if obj.is_private:
                if bundle.request.user in obj.collaborators.all()\
                        or is_admin(bundle.request):
                    allowed.append(obj)
            else:
                allowed.append(obj)

        return allowed

    def update_detail(self, object_list, bundle):
        if bundle.obj.is_private:
            if bundle.request.user in bundle.obj.collaborators.all()\
                    or is_admin(bundle.request):
                    return True
            else:
                return False
        return True

    def delete_list(self, object_list, bundle):
        allowed = []

        for obj in object_list:
            if obj.is_private:
                if bundle.request.user in obj.collaborators.all()\
                        or is_admin(bundle.request):
                    allowed.append(obj)
            else:
                allowed.append(obj)

        return allowed

    def delete_detail(self, object_list, bundle):
        if bundle.obj.is_private:
            if bundle.request.user in bundle.obj.collaborators.all()\
                    or is_admin(bundle.request):
                    return True
            else:
                return False
        return True


# slight variation to the default model resource
class DefaultModelResource(ModelResource):
    def hydrate_added_time(self, bundle):
        if bundle.data['added_time'] == "Now" or\
                bundle.data['added_time'] == "":
            bundle.data["added_time"] = datetime.now()
        return bundle

    def hydrate_user(self, bundle):
        if bundle.request.method == "POST":
            bundle.data["user"] = bundle.request.user
        return bundle

    def obj_delete_list(self, bundle, **kwargs):
        raise ImmediateHttpResponse(
            HttpForbidden("You do not have the required permissions"))


# This is a class that created by Alex - for all common meta settings.
class DefaultMeta:
    authorization = Authorization()
    always_return_data = True
    include_resource_uri = True
    testtest = "inside test meta"


# All the user resources
class UserResource(DefaultModelResource):
    # instructables.

    class Meta:
        queryset = User.objects.all()
        resources = "user"
        fields = ['id', 'username', 'first_name', 'last_name', 'last_login',
                  'first_name', 'last_name' 'facebook_id', 'date_joined',
                  'profile_url', 'makeys_count', 'email']
        authorization = Authorization()
        allowed_methods = ['get']
        filtering = {
            'date_joined': ('lte', 'gte'),
            'last_login': ('lte', 'gte'),
        }

    def dehydrate(self, bundle):
        bundle.data['profile_url'] = bundle.obj.profile.profile_img_url()
        bundle.data['makeys_count'] = models.core.Makey.objects.\
            filter(collaborators__in=[bundle.obj.id]).filter(is_enabled=True).\
            count()
        bundle.data['followers_count'] = bundle.obj.profile.followers.all().\
            count()
        bundle.data['following_count'] = bundle.obj.profile.following.all().\
            count()
        bundle.data['insights_count'] = bundle.obj.note_set.count()
        # bundle.data['github_url'] = bundle.obj.profile.github_url
        # bundle.data['linkedin_url'] = bundle.obj.profile.linkedin_url
        # bundle.data['facebook_url'] = bundle.obj.profile.facebook_url
        # bundle.data['twitter_url'] = bundle.obj.profile.twitter_url
        # bundle.data['yt_channel_url'] = bundle.obj.profile.yt_channel_url
        # bundle.data['blog_url'] = bundle.obj.profile.blog_url
        # bundle.data['website_url'] = bundle.obj.profile.website_url
        try:
            bundle.data['profile_id'] = models.core.UserProfile.objects.\
                get(user=bundle.obj.id).id
        except:
            print("userid: " + str(bundle.obj.id))
        return bundle

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<user_id>\d+)/following/$" %
                self._meta.resource_name,
                self.wrap_view('following'),
                name="api_following"),
            url(r"^(?P<resource_name>%s)/(?P<user_id>\d+)/followers/$" %
                self._meta.resource_name,
                self.wrap_view('followers'),
                name="api_followers"),
            url(r"^(?P<resource_name>%s)/(?P<user_id>\d+)/makeys/$" %
                self._meta.resource_name,
                self.wrap_view('makeys'),
                name="api_makeys"),
            url(r"^(?P<resource_name>%s)/search%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_search'),
                name="api_get_search"),
        ]

    def following(self, request, **kwargs):
        self.is_authenticated(request)
        self.throttle_check(request)

        user_id = kwargs['user_id']
        following_list = User.objects.get(id=user_id).profile.following.all()

        objects = []
        profileResource = UserProfileResource()
        for user in following_list:
            bundle = profileResource.build_bundle(obj=user, request=request)
            bundle = profileResource.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'objects': objects,
        }

        self.log_throttled_access(request)
        return profileResource.create_response(request, object_list)

    def followers(self, request, **kwargs):
        self.is_authenticated(request)
        self.throttle_check(request)

        user_id = kwargs['user_id']
        followers_list = User.objects.get(id=user_id).profile.followers.all()

        objects = []
        profileResource = UserProfileResource()
        for user in followers_list:
            bundle = profileResource.build_bundle(obj=user, request=request)
            bundle = profileResource.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'objects': objects,
        }

        self.log_throttled_access(request)
        return profileResource.create_response(request, object_list)

    def makeys(self, request, **kwargs):
        self.is_authenticated(request)
        self.throttle_check(request)

        user_id = kwargs['user_id']
        makeys_list = models.core.Makey.objects.\
            filter(collaborators__in=user_id).filter(is_enabled=True)

        objects = []
        makeyResource = MakeyResourceMakerPage()
        for makey in makeys_list:
            bundle = makeyResource.build_bundle(obj=makey, request=request)
            bundle = makeyResource.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'objects': objects,
        }

        self.log_throttled_access(request)
        return makeyResource.create_response(request, object_list)

    def get_search(self, request, **kwargs):
        q = request.GET.get('q', '')
        if q:
            users = models.core.User.objects\
                .filter(is_active=True)\
                .filter(Q(first_name__icontains=q) |
                        Q(last_name__icontains=q) |
                        Q(username__icontains=q))[:10]

            results = []
            for user in users:
                bundle = self.build_bundle(obj=user, request=request)
                bundle = self.full_dehydrate(bundle)
                results.append(bundle)
            results_list = {
                'users': results,
            }
            return self.create_response(request, results_list)


class MyTagResource(DefaultModelResource):
    class Meta(DefaultMeta):
        queryset = Tag.objects.all()
        resource_name = "tag"

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_search'), name="api_get_search"),
        ]

    def get_search(self, request, **kwargs):
        q = request.GET.get('q', '')
        if q:
            tags = Tag.objects\
                .filter(Q(name__icontains=q))

            results = []
            for tag in tags:
                bundle = self.build_bundle(obj=tag, request=request)
                bundle = self.full_dehydrate(bundle)
                results.append(bundle)
            results_list = {
                'tags': results,
            }
            return self.create_response(request, results_list)


class CommentResource(DefaultModelResource):
    user = fields.ForeignKey(UserResource, 'user', null=True, blank=True,
                             full=True)

    class Meta(DefaultMeta):
        queryset = models.core.Comment.objects.all()
        resources = "comment"
        authorization = Authorization()
        filtering = {
            'user': 'exact',
        }


class LikeCommentResource(DefaultModelResource):
    liker = fields.ForeignKey(UserResource, 'user', full=True)
    comment = fields.ForeignKey(CommentResource, 'comment',)

    class Meta(DefaultMeta):
        queryset = models.like.LikeComment.objects.order_by('?')
        resource_name = "likes/comment"
        authorization = Authorization()
        filtering = {
            'comment': 'exact',
            'liker': 'exact',
        }


class ArticleResource(DefaultModelResource):
    comments = fields.ManyToManyField(CommentResource, 'comments', null=True,
                                      blank=True)
    tags = fields.ManyToManyField('woot.apps.catalog.api.TagResource',
                                  'tags', null=True, blank=True)
    user = fields.ForeignKey(UserResource, 'user', null=True,
                             blank=True, full=True)
    new_user = fields.ForeignKey('woot.apps.catalog.api.NewUserResource',
                                 'new_user', null=True, blank=True, full=True)

    class Meta(DefaultMeta):
        queryset = models.core.Article.objects.all()
        resource_name = "article"
        authorization = Authorization()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/open_graph%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_open_graph'),
                name="api_get_open_graph"),
        ]

    def get_open_graph(self, request, **kwargs):
        url = request.GET.get('url', '')
        open_graph = {
            'title': '',
            'description': '',
            'image_url': '',
            'url': url,
            'valid': False
        }
        if url:
            try:
                req = Request(url, headers=hdr)
                raw_html = urlopen(req).read()
                open_graph['valid'] = True
                og = OpenGraph(html=raw_html, scrape=True)
                if og.is_valid():
                    _json = json.loads(og.to_json())
                    open_graph['title'] = _json['title']
                    open_graph['description'] = _json['description']
                    open_graph['image_url'] = _json['image']
            except Exception as e:
                print(e.__doc__)
                print(e.message)

        result = {
            'open_graph': open_graph,
        }
        return self.create_response(request, result)


class LikeArticleResource(DefaultModelResource):
    liker = fields.ForeignKey(UserResource, 'user', full=True)
    article = fields.ForeignKey(ArticleResource, 'article',)

    class Meta(DefaultMeta):
        queryset = models.like.LikeArticle.objects.order_by('?')
        resource_name = "likes/article"
        authorization = Authorization()
        filtering = {
            'article': 'exact',
            'liker': 'exact',
        }


class TestResource(ModelResource):
    class Meta:
        queryset = models.core.Product.objects.all()
        resource_name = "test"


class ProductResource(DefaultModelResource):
    class Meta:
        queryset = models.core.Product.objects.all()
        resource_name = "product"
        authorization = Authorization()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" %
                (
                    self._meta.resource_name,
                    trailing_slash()
                ),
                self.wrap_view('get_search'),
                name="api_get_search"),
        ]

    def get_search(self, request, **kwargs):
        q = request.GET.get('q', '')
        if q:
            q_clean = unicodedata.normalize('NFKD', q).\
                encode('ascii', 'ignore').translate(
                    string.maketrans("", ""),
                    string.punctuation).strip().split(" ")
            qs = reduce(operator.and_, (Q(name__icontains=n) for n in q_clean))
            products = models.core.Product.objects\
                .filter(is_enabled=True)\
                .filter(qs)\
                .filter(identicalto=None).order_by('-score')[:10]

            results = []
            for product in products:
                bundle = self.build_bundle(obj=product, request=request)
                bundle = self.full_dehydrate(bundle)
                results.append(bundle)
            results_list = {
                'products': results,
            }
            return self.create_response(request, results_list)


class ImageResource(DefaultModelResource):
    user = fields.ForeignKey(UserResource, 'user', null=True, blank=True,
                             full=True)
    comments = fields.ManyToManyField(CommentResource, 'comments', null=True,
                                      blank=True)
    note = fields.ToManyField('woot.apps.catalog.api.NoteResource', 'note_set',
                              null=True, blank=True)

    class Meta(DefaultMeta):
        queryset = models.core.Image.objects.all().order_by('-order')
        resource_name = "image"
        authorization = Authorization()


class NoteResource(DefaultModelResource):
    user = fields.ForeignKey(UserResource, 'user', null=True, blank=True,
                             full=True)
    comments = fields.ManyToManyField(CommentResource, 'comments', null=True,
                                      blank=True)
    image = fields.ForeignKey(ImageResource, 'image', null=True, blank=True,
                              full=True)

    class Meta(DefaultMeta):
        queryset = models.core.Note.objects.all()
        resource_name = "note"
        authorization = Authorization()
        #authentication = SessionAuthentication()
        filtering = {
            'user': ALL_WITH_RELATIONS,
            # 'user': ALL,
        }

    def hydrate_image(self, bundle, request=None, **kwargs):
        if bundle.data['image'] == '':
            bundle.data['image'] = None

        return bundle


class LikeNoteResource(DefaultModelResource):
    liker = fields.ForeignKey(UserResource, 'user', full=True)
    note = fields.ForeignKey(NoteResource, 'note',)

    class Meta(DefaultMeta):
        queryset = models.like.LikeNote.objects.order_by('?')
        resource_name = "likes/note"
        authorization = Authorization()
        filtering = {
            'note': 'exact',
            'liker': 'exact',
        }


class DocumentationResource(DefaultModelResource):
    user = fields.ForeignKey(UserResource, 'user', null=True, blank=True,
                             full=True)

    class Meta(DefaultMeta):
        queryset = models.core.Documentation.objects.all()
        resource_name = "documentation"
        authorization = Authorization()


class TextDocumentationResource(DefaultModelResource):
    user = fields.ForeignKey(UserResource, 'user', null=True, blank=True,
                             full=True)
    makey = fields.ForeignKey('woot.apps.catalog.api.MakeyResource', 'makey',
                              null=True, blank=True)
    images = fields.ManyToManyField(ImageResource, 'images',
                                    null=True, blank=True, full=True)

    class Meta(DefaultMeta):
        queryset = models.core.TextDocumentation.objects.all()
        resource_name = 'text_documentation'
        authorization = Authorization()


class LikeImageResource(DefaultModelResource):
    liker = fields.ForeignKey(UserResource, 'user', full=True)
    image = fields.ForeignKey(ImageResource, 'image',)

    class Meta(DefaultMeta):
        queryset = models.like.LikeImage.objects.order_by('?')
        resource_name = "likes/image"
        authorization = Authorization()
        filtering = {
            'image': 'exact',
            'liker': 'exact',
        }


class VideoResource(DefaultModelResource):
    user = fields.ForeignKey(UserResource, 'user', null=True, blank=True,
                             full=True)
    comments = fields.ManyToManyField(CommentResource, 'comments', null=True,
                                      blank=True)

    class Meta(DefaultMeta):
        queryset = models.core.Video.objects.all()
        resource_name = "video"
        authorization = Authorization()


class LikeVideoResource(DefaultModelResource):
    liker = fields.ForeignKey(UserResource, 'user', full=True)
    video = fields.ForeignKey(VideoResource, 'video',)

    class Meta(DefaultMeta):
        queryset = models.like.LikeVideo.objects.order_by('?')
        resource_name = "likes/video"
        authorization = Authorization()
        filtering = {
            'video': 'exact',
            'liker': 'exact',
        }


class ImageResourceProductPage(DefaultModelResource):
    product = fields.ForeignKey(ProductResource, 'product',)

    class Meta:
        queryset = models.core.ProductImage.objects.filter(is_enabled=True)
        resource_name = 'image_p'
        authorization = Authorization()
        filtering = {
            'product': ('exact',),
        }


class NewUserResource(DefaultModelResource):
    class Meta(DefaultMeta):
        queryset = models.core.NewUser.objects.all()
        resource_name = "new_user"
        authorization = Authorization()
        # authentication = SessionAuthentication()


class NewProductResource(DefaultModelResource):
    user = fields.ForeignKey(UserResource, 'user', null=True, blank=True,
                             full=True)
    image = fields.ForeignKey(ImageResource, 'image', null=True, blank=True,
                              full=True)

    class Meta(DefaultMeta):
        queryset = models.core.NewProduct.objects.all()
        resource_name = "new_part"
        authorization = Authorization()


class ProductResourceMakeyPage(DefaultModelResource):
    images = fields.ManyToManyField(ImageResourceProductPage, 'productimages',
                                    null=True, blank=True, readonly=True,
                                    full=True)

    class Meta:
        queryset = models.core.Product.objects.all()
        resource_name = "product_m"
        authorization = Authorization()


class TopMakeysResourceLandingPage(DefaultModelResource):
    user = fields.ForeignKey(UserResource, 'user', null=True, blank=True,
                             full=True)
    images = fields.ManyToManyField(ImageResource, 'images', null=True,
                                    blank=True, full=True)
    collaborators = fields.ManyToManyField(UserResource, 'collaborators',
                                           null=True, blank=True, full=True)
    cover_pic = fields.ForeignKey(ImageResource, 'cover_pic', null=True,
                                  blank=True, full=True)
    notes = fields.ManyToManyField(ImageResource, 'notes', null=True,
                                   blank=True)
    parts = fields.ManyToManyField(ProductResourceMakeyPage, 'partsused',
                                   null=True, blank=True)

    class Meta(DefaultMeta):
        makey = models.core.Makey.objects.all().order_by('-score').\
            filter(is_enabled=True)
        queryset = makey
        resource_name = 'top_makeys'
        authorization = Authorization()
        include_resource_uri = False
        always_return_data = True

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/similar/(?P<makey_id>\d+)/$" %
                self._meta.resource_name,
                self.wrap_view('similar_makeys'),
                name="api_similar_makeys")
        ]

    def similar_makeys(self, request, **kwargs):
        self.is_authenticated(request)
        self.throttle_check(request)

        makey_id = kwargs['makey_id']
        similar_makeys = models.core.Makey.objects.similar(makey_id)[:6]

        objects = []
        for makey in similar_makeys:
            bundle = self.build_bundle(obj=makey, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'objects': objects,
        }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)


class SpaceResource(DefaultModelResource):
    members = fields.ManyToManyField(UserResource, 'members', null=True,
                                     blank=True, full=True)
    makeys = fields.ManyToManyField(TopMakeysResourceLandingPage,
                                    'makeys_made_in', null=True, blank=True,
                                    full=True)

    class Meta(DefaultMeta):
        queryset = models.core.Space.objects.all().order_by('id').reverse().\
            filter(is_enabled=True)
        resource_name = 'space'
        authorization = Authorization()
        include_resource_uri = False
        always_return_data = True
        filtering = {
            # 'parts': ALL,
            # 'collaborators': ALL,
        }

    def hydrate_members(self, bundle):
        if len(bundle.data['members']) > 0 and\
                type(bundle.data['members'][0]) is not unicode:
            return bundle

        space = models.core.Space.objects.get(id=int(bundle.data['id']))

        new_list = bundle.data['members']
        admin_list = ['/api/v1/user/' + str(user.id) + '/'
                      for user in space.admins.all()]
        non_admin_list = [x for x in new_list if x not in admin_list]

        final_list = admin_list + non_admin_list
        bundle.data['members'] = final_list
        return bundle

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_search'), name="api_get_search"),
        ]

    def get_search(self, request, **kwargs):
        q = request.GET.get('q', '')
        if q:
            spaces = models.core.Space.objects\
                .filter(Q(name__icontains=q))[:10]

            results = []
            for space in spaces:
                bundle = self.build_bundle(obj=space, request=request)
                bundle = self.full_dehydrate(bundle)
                results.append(bundle)
            results_list = {
                'spaces': results,
            }
            return self.create_response(request, results_list)


class InventoryResource(DefaultModelResource):
    part = fields.ForeignKey(ProductResource, 'part', full=True)
    space = fields.ForeignKey(SpaceResource, 'space')
    quantity = fields.IntegerField(attribute='quantity')

    class Meta(DefaultMeta):
        queryset = models.core.Inventory.objects.order_by('?')
        resource_name = "inventory"
        authorization = Authorization()
        filtering = {
            'part': 'exact',
            'space': 'exact',
        }


class NewInventoryResource(DefaultModelResource):
    part = fields.ForeignKey(NewProductResource, 'part', full=True)
    space = fields.ForeignKey(SpaceResource, 'space')
    quantity = fields.IntegerField(attribute='quantity')

    class Meta(DefaultMeta):
        queryset = models.core.NewInventory.objects.order_by('?')
        resource_name = "new_inventory"
        authorization = Authorization()
        filtering = {
            'part': 'exact',
            'space': 'exact',
        }


class FileResource(DefaultModelResource):
    user = fields.ForeignKey(UserResource, 'user', null=True, blank=True,
                             full=True)

    class Meta(DefaultMeta):
        queryset = models.core.UpFile.objects.all()
        resource_name = 'file'
        authorization = Authorization()


class MakeyResource(DefaultModelResource):
    collaborators = fields.ManyToManyField(UserResource, 'collaborators',
                                           null=True, blank=True)
    user = fields.ForeignKey(UserResource, 'user', null=True, blank=True,
                             full=True)
    made_in = fields.ForeignKey(SpaceResource, 'made_in', null=True, blank=True,
                                )
    new_users = fields.ManyToManyField(NewUserResource, 'new_users', null=True,
                                       blank=True)
    parts = fields.ManyToManyField(ProductResourceMakeyPage, 'partsused',
                                   null=True, blank=True)
    new_parts = fields.ManyToManyField(NewProductResource, 'new_parts',
                                       null=True, blank=True)
    tools = fields.ManyToManyField(ProductResourceMakeyPage, 'tools_used',
                                   null=True, blank=True)
    new_tools = fields.ManyToManyField(NewProductResource, 'new_tools',
                                       null=True, blank=True)
    notes = fields.ManyToManyField(NoteResource, 'notes', null=True, blank=True)
    documentations = fields.ManyToManyField(DocumentationResource,
                                            'documentations', null=True,
                                            blank=True)
    text_documentations = fields.ToManyField(TextDocumentationResource,
                                             'text_documentations',
                                             null=True, blank=True)
    comments = fields.ManyToManyField(CommentResource, 'comments', null=True,
                                      blank=True)
    images = fields.ManyToManyField(ImageResource, 'images', null=True,
                                    blank=True)
    videos = fields.ManyToManyField(VideoResource, 'videos', null=True,
                                    blank=True)
    cover_pic = fields.ForeignKey(ImageResource, 'cover_pic', null=True,
                                  blank=True)

    removed_collaborators = fields.ManyToManyField(UserResource,
                                                   'removed_collaborators',
                                                   null=True, blank=True)
    modules_used = fields.ManyToManyField('self', 'modules_used', null=True,
                                          blank=True)
    derived_from = fields.ForeignKey('self', 'derived_from', null=True,
                                     blank=True)
    as_part = fields.ForeignKey(ProductResource, 'as_part', null=True,
                                blank=True)

    as_part_new = fields.ForeignKey(NewProductResource, 'as_part_new',
                                    null=True, blank=True)

    steps = fields.ManyToManyField('woot.apps.catalog.api.StepResource',
                                   'instructablestep_set', null=True,
                                   blank=True)
    tags = fields.ToManyField(MyTagResource, 'tags', null=True, blank=True,
                              full=True)
    files = fields.ToManyField(FileResource, 'files', null=True, blank=True)

    class Meta(DefaultMeta):
        makey = models.core.Makey.objects.all().order_by('id').reverse().\
            filter(is_enabled=True)
        queryset = makey
        resource_name = 'makey'
        authorization = Authorization()
        include_resource_uri = False
        always_return_data = True
        filtering = {
            'parts': ALL,
            'collaborators': ALL,
        }

    def hydrate_notes(self, bundle):
        if len(bundle.data['notes']) > 0 and\
                type(bundle.data['notes'][0]) is not unicode:
            return bundle

        makey = models.core.Makey.objects.get(id=int(bundle.data['id']))

        old_list = ['/api/v1/note/' + str(note.id) + '/'
                    for note in makey.notes.all()]
        new_list = bundle.data['notes']

        moving = False
        if 'moving' in bundle.data.keys() and bundle.data['moving']:
            moving = True
            moving_id = bundle.data['moving_id']

        # if in old and not in new => note has been deleted or added elsewhere
        # Example: old: [1, 2, 3], new: [1, 2]
        # 3 has been deleted or was added earlier and should be added
        # if deleted => add to final_list and removed again by checking
        # if added => add to final_list and remain there
        #
        # if in new and not in old => note has been added or removed elsewhere
        # old: [1, 2], new: [1, 2, 3]
        # 3 has been added or has been deleted and it has to be ignored
        # if added => add to final_list and remain there
        # if deleted => add to final_list and removed again by checking
        missing_list = [x for x in old_list if x not in new_list]

        pre_final_list = new_list + missing_list
        final_list = []
        for note in pre_final_list:
            if moving:
                if note != moving_id:
                    final_list.append(note)
            else:
                curNote = models.core.Note.objects.get(id=int(note[13:-1]))
                if curNote.is_enabled:
                    final_list.append(note)

        bundle.data['notes'] = final_list
        return bundle

    def hydrate_collaborators(self, bundle):
        if len(bundle.data['collaborators']) > 0 and\
                type(bundle.data['collaborators'][0]) is not unicode:
            return bundle

        makey = models.core.Makey.objects.get(id=int(bundle.data['id']))

        old_list = ['/api/v1/user/' + str(user.id) + '/'
                    for user in makey.collaborators.all()]
        new_list = bundle.data['collaborators']
        missing_list = [x for x in old_list if x not in new_list]

        deleted_list = ['/api/v1/user/' + str(user.id) + '/'
                        for user in makey.removed_collaborators.all()]
        pre_final_list = new_list + missing_list
        final_list = []
        # TODO: Bug - if a user has been removed previously, he can't be added
        # to collaborators again as his name is always there in deleted_list
        for user in pre_final_list:
            # curUser = User.objects.get(id=int(user[13:-1]))
            if user not in deleted_list:
                final_list.append(user)
        bundle.data['collaborators'] = final_list
        return bundle

    def hydrate_documentations(self, bundle):
        if len(bundle.data['documentations']) > 0 and\
                type(bundle.data['documentations'][0]) is not unicode:
            return bundle

        makey = models.core.Makey.objects.get(id=int(bundle.data['id']))

        old_list = ['/api/v1/documentation/' + str(documentation.id) + '/'
                    for documentation in makey.documentations.all()]
        new_list = bundle.data['documentations']

        missing_list = [x for x in old_list if x not in new_list]

        pre_final_list = new_list + missing_list
        final_list = []
        for documentation in pre_final_list:
            curDocumentation = models.core.Documentation.objects.\
                get(id=int(documentation[22:-1]))
            if curDocumentation.is_enabled:
                final_list.append(documentation)
        bundle.data['documentations'] = final_list
        return bundle

    def hydrate_images(self, bundle):
        if len(bundle.data['images']) > 0 and\
                type(bundle.data['images'][0]) is not unicode:
            return bundle

        makey = models.core.Makey.objects.get(id=int(bundle.data['id']))

        old_list = ['/api/v1/image/' + str(image.id) + '/'
                    for image in makey.images.all()]
        new_list = bundle.data['images']

        moving = False
        if 'moving' in bundle.data.keys() and bundle.data['moving']:
            moving = True
            moving_id = bundle.data['moving_id']

        missing_list = [x for x in old_list if x not in new_list]

        pre_final_list = new_list + missing_list
        final_list = []
        for image in pre_final_list:
            if moving:
                if image != moving_id:
                    final_list.append(image)
            else:
                curImage = models.core.Image.objects.get(id=int(image[14:-1]))
                if curImage.is_enabled:
                    final_list.append(image)
        bundle.data['images'] = final_list
        return bundle

    def hydrate_videos(self, bundle):
        if len(bundle.data['videos']) > 0 and\
                type(bundle.data['videos'][0]) is not unicode:
            return bundle

        makey = models.core.Makey.objects.get(id=int(bundle.data['id']))

        old_list = ['/api/v1/video/' + str(video.id) + '/'
                    for video in makey.videos.all()]
        new_list = bundle.data['videos']

        moving = False
        if 'moving' in bundle.data.keys() and bundle.data['moving']:
            moving = True
            moving_id = bundle.data['moving_id']

        missing_list = [x for x in old_list if x not in new_list]

        pre_final_list = new_list + missing_list
        final_list = []
        for video in pre_final_list:
            if moving:
                if video != moving_id:
                    final_list.append(video)
            else:
                curVideo = models.core.Video.objects.get(id=int(video[14:-1]))
                if curVideo.is_enabled:
                    final_list.append(video)
        bundle.data['videos'] = final_list
        return bundle

    def hydrate_new_parts(self, bundle):
        if len(bundle.data['new_parts']) > 0 and\
                type(bundle.data['new_parts'][0]) is not unicode:
            return bundle

        makey = models.core.Makey.objects.get(id=int(bundle.data['id']))

        old_list = ['/api/v1/new_part/' + str(new_part.id) + '/'
                    for new_part in makey.new_parts.all()]
        new_list = bundle.data['new_parts']

        missing_list = [x for x in old_list if x not in new_list]

        pre_final_list = new_list + missing_list
        final_list = []
        for new_part in pre_final_list:
            curNewPart = models.core.NewProduct.objects.\
                get(id=int(new_part[17:-1]))
            if curNewPart.is_enabled:
                final_list.append(new_part)
        bundle.data['new_parts'] = final_list
        return bundle

    def hydrate_as_part(self, bundle):
        if not bundle.data['as_part']:
            bundle.obj.as_part = None
            del bundle.data['as_part']
        return bundle

    def hydrate_as_part_new(self, bundle):
        if not bundle.data['as_part_new']:
            bundle.obj.as_part_new = None
            del bundle.data['as_part_new']
        return bundle

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_search'), name="api_get_search"),
            url(r"^(?P<resource_name>%s)/hierarchy%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_hierarchy'), name="api_get_hierarchy"),
            url(r"^(?P<resource_name>%s)/preview%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_preview'), name="api_get_preview"),
            url(r"^(?P<resource_name>%s)/activities%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_activities'), name="api_get_activities"),
        ]

    def get_search(self, request, **kwargs):
        q = request.GET.get('q', '')
        u = request.GET.get('u', '')

        if q:
            if u:
                user = User.objects.get(id=int(u))
                makeys = models.core.Makey.objects.filter(
                    collaborators__in=[user]).filter(is_enabled=True)
            else:
                makeys = models.core.Makey.objects.filter(is_enabled=True)

            makeys = makeys.filter(Q(name__icontains=q) |
                                   Q(tags__name__icontains=q)).distinct()
            results = []
            for makey in makeys:
                if makey.user:
                    bundle = self.build_bundle(obj=makey, request=request)
                    bundle = self.full_dehydrate(bundle)
                    results.append(bundle)
            results_list = {
                'makeys': results[:10],
            }
            return self.create_response(request, results_list)

    def prepare_makey_hierarchy(self, makey):
        hierarchy = {}
        if not makey:
            return hierarchy
        else:
            hierarchy = {
                "name": makey.name,
                "makey_id": makey.id,
                "insights_count": makey.notes.exclude(is_pending_approval=True).count(),
                "gallery_count": makey.images.count() + makey.videos.count(),
                "discussions_count": makey.question_set.count(),
                "files_count": makey.files.count(),
            }
            if makey.modules_used.count():
                hierarchy["children"] = []
            for module in makey.modules_used.all():
                if module:
                    hierarchy["children"].append(self.prepare_makey_hierarchy(
                        module))

            prev_version = makey.derived_from
            if prev_version:
                hierarchy["versions"] = {}
                hierarchy["versions"]["prev"] = self.prepare_makey_hierarchy(
                    prev_version)

        return hierarchy

    def get_hierarchy(self, request, **kwargs):
        q = request.GET.get('q', '')
        hierarchy = {}
        if q:
            makey = models.core.Makey.objects.get(id=q)
            check_private_access(request, makey)
            hierarchy = self.prepare_makey_hierarchy(makey)

        return self.create_response(request, hierarchy)

    def get_activities(self,request, **kwargs):
        q = request.GET.get('q','')
        if q:
            makey = models.core.Makey.objects.get(id=q)
            activities = get_makey_activities(makey,True)
            activity_set = []
            for activity in activities:
                actinfo = {
                    'added_time' : time_elapsed(activity.added_time),
                    'user_name' : activity.user.username,
                    'user_firstname' : activity.user.first_name,
                    'user_last_name' : activity.user.last_name,
                    'absolute_url' : activity.makey.get_absolute_url(),
                    'event_type' : Interaction.name_from_id(activity.event)
                }

                if actinfo['event_type'] == 'activity_answer_created':
                    actinfo.update({
                        'answer_question_id' : activity.answer.question.id,
                        'action' : 'answered a',
                        'action_value' : 'discussions/' + str(activity.answer.question.id) +'/',
                        'verb' : 'question'
                    })

                elif actinfo['event_type'] == 'activity_insight_created':
                    actinfo.update({
                        'action' : 'added an',
                        'action_value' : 'insights/' + str(activity.event_id) +'/',
                        'verb' : 'insight',
                        'event_id' : activity.event_id
                    })

                elif actinfo['event_type'] == 'activity_question_created':
                    actinfo.update({
                        'action' : 'asked a',
                        'action_value' : 'discussions/'+ str(activity.event_id) +'/',
                        'verb' : 'question',
                        'event_id' : activity.event_id
                    })
                actinfo.update({
                    'makey_name' : activity.makey.name
                })
                activity_set.append(actinfo)

            return self.create_response(request, activity_set[:10])
    def prepare_makey_preview(self, makey):
        preview = {}
        if not makey:
            return preview

        preview["makey_id"] = makey.id
        preview["makey_url"] = reverse('catalog:makey_new_slug', args=[makey.user.username, makey.slug])
        preview["makey_name"] = makey.name
        insights = makey.notes.exclude(is_pending_approval=True)

        insights_recent = sorted(insights, key=lambda x: x.added_time,
                reverse=True)
        insights_top = sorted(insights, key=lambda x: x.comments.count(),
                reverse=True)

        preview["insights"] = {
            "top" : [],
            "recent" : []
        }
        for insight in insights_top:
            insight_obj = {}
            insight_obj["id"] = insight.id
            insight_obj["title"] = insight.title
            insight_obj["description"] = insight.body
            insight_obj["comments"] = insight.comments.count()
            insight_obj["added_time"] = insight.added_time
            insight_obj["username"] = insight.user.username
            insight_obj["makey_id"] = makey.id
            insight_obj["makey_url"] = reverse('catalog:makey_new_slug', args=[makey.user.username, makey.slug])
            insight_obj["makey_name"] = makey.name
            insight_obj["insight_url"] = reverse('catalog:makey_new_insight_slug', args=[makey.user.username, makey.slug, insight.id])
            preview["insights"]["top"].append(insight_obj)

        for insight in insights_recent:
            insight_obj = {}
            insight_obj["id"] = insight.id
            insight_obj["title"] = insight.title
            insight_obj["description"] = insight.body
            insight_obj["comments"] = insight.comments.count()
            insight_obj["added_time"] = insight.added_time
            insight_obj["username"] = insight.user.username
            insight_obj["makey_id"] = makey.id
            insight_obj["makey_url"] = reverse('catalog:makey_new_slug', args=[makey.user.username, makey.slug])
            insight_obj["makey_name"] = makey.name
            insight_obj["insight_url"] = reverse('catalog:makey_new_insight_slug', args=[makey.user.username, makey.slug, insight.id])
            preview["insights"]["recent"].append(insight_obj)

        questions = models.forum.Question.objects.filter(makey=makey)

        questions_recent = sorted(questions, key=lambda x: x.created,
                reverse=True)
        questions_top = sorted(questions, key=lambda x: x.answer_set.count(),
                reverse=True)

        preview["discussions"] = {
            "top" : [],
            "recent" : []
        }
        for question in questions_top:
            discussion = {}
            discussion["id"] = question.id
            discussion["title"] = question.name
            discussion["description"] = question.description
            discussion["added_time"] = question.created
            discussion["answers"] = models.forum.Answer.objects.filter(question=question).count()
            discussion["username"] = question.creator.username
            discussion["makey_id"] = makey.id
            discussion["makey_url"] = reverse('catalog:makey_new_slug', args=[makey.user.username, makey.slug])
            discussion["makey_name"] = makey.name
            discussion["discussion_url"] = reverse('catalog:question', args=[question.id])
            preview["discussions"]["top"].append(discussion)

        for question in questions_recent:
            discussion = {}
            discussion["id"] = question.id
            discussion["title"] = question.name
            discussion["description"] = question.description
            discussion["added_time"] = question.created
            discussion["answers"] = models.forum.Answer.objects.filter(question=question).count()
            discussion["username"] = question.creator.username
            discussion["makey_id"] = makey.id
            discussion["makey_url"] = reverse('catalog:makey_new_slug', args=[makey.user.username, makey.slug])
            discussion["makey_name"] = makey.name
            discussion["discussion_url"] = reverse('catalog:question', args=[question.id])
            preview["discussions"]["recent"].append(discussion)

        return preview

    def get_preview(self, request, **kwargs):
        q = request.GET.get('q', '')
        preview = {}
        if q:
            makey = models.core.Makey.objects.get(id=q)
            check_private_access(request, makey)
            preview = self.prepare_makey_preview(makey)

        return self.create_response(request, preview)


# All Makey page
class TopSpacesResource(DefaultModelResource):
    # user = fields.ForeignKey(UserResource, 'user', null=True, blank=True,
    #                          full=True)
    # images = fields.ManyToManyField(ImageResource, 'images', null=True,
    #                                 blank=True, full=True)
    admins = fields.ManyToManyField(UserResource, 'admins', null=True,
                                    blank=True)
    members = fields.ManyToManyField(UserResource, 'members', null=True,
                                     blank=True)
    tools = fields.ManyToManyField(ProductResource, 'tools', null=True,
                                   blank=True)
    makeys = fields.ManyToManyField(MakeyResource, 'makeys_made_in', null=True,
                                    blank=True)
    # cover_pic = fields.ForeignKey(ImageResource, 'cover_pic', null=True,
    #                               blank=True)
    # notes = fields.ManyToManyField(ImageResource, 'notes', null=True,
    #                                 blank=True,)
    # parts = fields.ManyToManyField(ProductResourceMakeyPage, 'partsused',
                                   # null=True, blank=True)

    class Meta(DefaultMeta):
        users = User.objects.all()
        queryset = models.core.Space.objects.all().\
            annotate(members_count=Count('members')).\
            filter(members__in=users).order_by('-members_count')
        # print "\n"*3
        # print queryset.count()
        # space = models.core.Space.objects.all().order_by('-score').
        #                   filter(is_enabled=True)
        resource_name = 'top_spaces'
        authorization = Authorization()
        include_resource_uri = False
        always_return_data = True

    def dehydrate(self, bundle):
        bundle.data['alex'] = "alex"
        return bundle


class LikeMakeyResource(DefaultModelResource):
    liker = fields.ForeignKey(UserResource, 'user', full=True)
    makey = fields.ForeignKey(MakeyResource, 'makey',)

    class Meta(DefaultMeta):
        queryset = models.like.LikeMakey.objects.order_by('?')
        resource_name = "likes/makey"
        authorization = Authorization()
        filtering = {
            'makey': 'exact',
            'liker': 'exact',
        }


# Resouces for product page
class MakeyResourceProductPage(DefaultModelResource):
    user = fields.ForeignKey(UserResource, 'user', null=True, blank=True,
                             full=True)
    parts = fields.ManyToManyField(ProductResource, 'partsused', null=True,
                                   blank=True,)

    class Meta(DefaultMeta):
        queryset = models.core.Makey.objects.all().filter(is_enabled=True)
        resource_name = 'makey_p'
        # authentication = SessionAuthentication()
        # authorization = Authorization()
        filtering = {
            'parts': ('exact',),
            'user': ('exact',),
            'added_time': ('gte', 'lte',),
            'is_enabled': True,
        }


class TutorialResourceProductPage(DefaultModelResource):
    user = fields.ForeignKey(UserResource, 'user', null=True, blank=True,
                             full=True)
    products = fields.ManyToManyField(ProductResource, 'products', null=True,
                                      blank=True)

    class Meta(DefaultMeta):
        queryset = models.core.Tutorial.objects.all()
        resource_name = 'tutorial_p'
        # authorization = Authorization()
        # authentication = SessionAuthentication()
        filtering = {
            "products": ALL,
            "user": ('exact',),
            "added_time": ('lte', 'gte',),
        }


class TutorialResource(DefaultModelResource):
    products = fields.ManyToManyField(ProductResource, 'products', null=True,
                                      blank=True)

    class Meta(DefaultMeta):
        queryset = models.core.Tutorial.objects.all()
        resource_name = 'tutorial_with_product'
        authorization = Authorization()
        #authentication = SessionAuthentication()
        filtering = {
            "products": ('exact',),
            "user": ('exact',),
        }


class LocationResource(DefaultModelResource):
    class Meta(DefaultMeta):
        queryset = models.core.Location.objects.all()
        resource_name = 'location'
        authorization = Authorization()
        #authentication = SessionAuthentication()


class ShopResource(DefaultModelResource):
    class Meta:
        queryset = models.core.Shop.objects.all()
        resource_name = "shop"
        authorization = Authorization()
        #authentication = SessionAuthentication()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_search'), name="shop_api_get_search"),
        ]

    def get_search(self, request, **kwargs):
        q = request.GET.get('q', '')
        if q:
            shops = models.core.Shop.objects.filter(Q(name__icontains=q))[:10]

            results = []
            for space in shops:
                bundle = self.build_bundle(obj=space, request=request)
                bundle = self.full_dehydrate(bundle)
                results.append(bundle)
            results_list = {
                'shops': results,
            }
            return self.create_response(request, results_list)


class LikeShopResource(DefaultModelResource):
    shop = fields.ForeignKey(ShopResource, 'shop', null=True, blank=True)
    liker = fields.ForeignKey(UserResource, 'user', null=True, blank=True,
                              full=True)

    class Meta(DefaultMeta):
        queryset = models.like.LikeShop.objects.order_by('?')
        resource_name = "likes/shop"
        authorization = Authorization()
        #authentication = SessionAuthentication()
        filtering = {
            "shop": ALL,
            "liker": ('exact',),
            "added_time": ('lte', 'gte',),
        }

    def hydrate_liked_time(self, bundle):
        if bundle.data['liked_time'] == "Now" or \
                bundle.data['liked_time'] == "":
            bundle.data['liked_time'] = datetime.datetime.now()
        return bundle

    def hydrate_liker(self, bundle):
        if bundle.data['liker']:
            bundle.data['liker'] = User.objects.get(
                username=bundle.data['liker']['username'])
        return bundle


class LikeShopWithShopResource(DefaultModelResource):
    shop = fields.ForeignKey(ShopResource, 'shop', null=True, blank=True,
                             full=True)

    class Meta(DefaultMeta):
        queryset = models.like.LikeShop.objects.order_by('?')
        resource_name = "likes/shop_full"
        authorization = Authorization()
        # authentication = SessionAuthentication()
        filtering = {
            "shop": ALL,
            "liker": ('exact',),
        }


class ShopResourceProductPage(DefaultModelResource):
    lambda_query = lambda bundle: bundle.obj.likes.through.objects.\
        filter(shop=bundle.obj)
    # likes = fields.ManyToManyField(LikeShopResource, attribute=lambda_query,
                                   # null=True, blank=True, readonly=True,
                                   # full=True)
    location = fields.ForeignKey(LocationResource, 'location', readonly=True,
                                 full=True)

    class Meta:
        queryset = models.core.Shop.objects.all()
        resource_name = 'shop_p'
        authorization = Authorization()


class ShopUrlResourceProductPage(DefaultModelResource):
    shop = fields.ForeignKey(ShopResourceProductPage, 'shop', readonly=True,
                             full=True)
    product = fields.ForeignKey(ProductResource, 'product', readonly=True)
    # lambda_query = lambda bundle: bundle.obj.shop.likes.through.
    #       objects.filter(shop = bundle.obj)
    # likes = fields.ManyToManyField(LikeShopResource, attribute = lambda_query,
    #  null=True, blank=True, readonly=True, full=True)

    class Meta:
        queryset = models.core.ProductShopUrl.objects.all()
        resource_name = 'shopurl_p'
        authorization = Authorization()
        filtering = {
            "product": ('exact',),
        }


class ProductReviewResourceProductPage(DefaultModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=True)
    product = fields.ForeignKey(ProductResource, 'product', null=True,
                                blank=True)

    class Meta(DefaultMeta):
        queryset = models.review.ProductReview.objects.all()
        resource_name = 'review_p'
        authorization = Authorization()
        #authentication = SessionAuthentication()
        filtering = {
            "product": ('exact',),
            "added_time": ('lte', 'gte'),
        }


class ProductReviewResource(DefaultModelResource):
    product = fields.ForeignKey(ProductResource, 'product')
    user = fields.ForeignKey(UserResource, 'user', full=True)

    class Meta(DefaultMeta):
        queryset = models.review.ProductReview.objects.all()
        resource_name = 'review/product'
        authorization = Authorization()
        # authentication = SessionAuthentication()
        filtering = {
            'user': ('exact',),
        }


class SpaceReviewResource(DefaultModelResource):
    space = fields.ForeignKey(SpaceResource, 'space')
    user = fields.ForeignKey(UserResource, 'user', full=True)

    class Meta(DefaultMeta):
        queryset = models.review.SpaceReview.objects.all()
        resource_name = 'review/space'
        authorization = Authorization()
        # authentication = SessionAuthentication()
        filtering = {
            'user': ('exact',),
        }


class VoteSpaceReviewResource(DefaultModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=True)
    review = fields.ForeignKey(SpaceReviewResource, 'review')

    class Meta(DefaultMeta):
        queryset = models.vote.VoteSpaceReview.objects.all()
        resource_name = "votes/space_review"
        authorization = Authorization()
        #authentication = SessionAuthentication()
        filtering = {
            "review": ('exact',),
            "user": ('exact',),
        }


class DescriptionResourceProductPage(DefaultModelResource):
    shop = fields.ForeignKey(ShopResource, 'shop', readonly=True, full=True)
    product = fields.ForeignKey(ProductResource, 'product', null=True,
                                blank=True)

    class Meta:
        queryset = models.core.ProductDescription.objects.all()
        resource_name = 'description_p'
        authorization = Authorization()
        filtering = {
            "product": ('exact',),
        }


class LikeResourceProductPage(DefaultModelResource):
    product = fields.ForeignKey(ProductResource, 'product', null=True,
                                blank=True)
    liker = fields.ForeignKey(UserResource, 'user', null=True, blank=True,
                              full=True)

    class Meta(DefaultMeta):
        queryset = models.like.LikeProduct.objects.order_by('?')
        # resource_name = "likes_p"
        resource_name = "likes/product_p"
        authorization = Authorization()
        #authentication = SessionAuthentication()
        filtering = {
            "product": ('exact',),
            "liker": ('exact',),
            "added_time": ('lte', 'gte'),
        }

    def hydrate_liker(self, bundle):
        if bundle.data['liker']:
            bundle.data['liker'] = User.objects.\
                get(username=bundle.data['liker']['username'])
        return bundle


class LikeProductResourceWithProduct(DefaultModelResource):
    product = fields.ForeignKey(ProductResource, 'product', null=True,
                                blank=True, full=True)

    class Meta(DefaultMeta):
        queryset = models.like.LikeProduct.objects.order_by('?')
        resource_name = "likes/product_full"
        authorization = Authorization()
        # authentication = SessionAuthentication()
        filtering = {
            "product": ('exact',),
            "added_time": ('lte', 'gte'),
        }


class VoteProductReviewResource(DefaultModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=True)
    review = fields.ForeignKey(ProductReviewResourceProductPage, 'review')

    class Meta(DefaultMeta):
        queryset = models.vote.VoteProductReview.objects.all()
        resource_name = "votes/review_p"
        authorization = Authorization()
        #authentication = SessionAuthentication()
        filtering = {
            "review": ('exact',),
            "user": ('exact',),
        }


class VoteProductReviewWithProductResource(DefaultModelResource):
    review = fields.ForeignKey(ProductReviewResource, 'review', full=True)

    class Meta:
        queryset = models.vote.VoteProductReview.objects.all()
        resource_name = "votes/product_review_full"
        authorization = Authorization()
        # authentication = SessionAuthentication()
        filtering = {
            "review": ('exact',),
            "user": ('exact',),
        }


class VoteMakeyResource(DefaultModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=True)
    makey = fields.ForeignKey(MakeyResourceProductPage, 'makey')

    class Meta(DefaultMeta):
        queryset = models.vote.VoteMakey.objects.all()
        resource_name = "votes/makey_p"
        authorization = Authorization()
        #authentication = SessionAuthentication()
        filtering = {
            "makey": ('exact',),
            "user": ('exact',),
        }


class VoteMakeyWithMakeyResource(DefaultModelResource):
    makey = fields.ForeignKey(MakeyResource, 'makey', full=True)

    class Meta(DefaultMeta):
        queryset = models.vote.VoteMakey.objects.all()
        resource_name = "votes/makey_full"
        authorization = Authorization()
        # authentication = SessionAuthentication()
        filtering = {
            "makey": ('exact',),
            "user": ('exact',),
        }


class VoteTutorialResource(DefaultModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=True)
    tutorial = fields.ForeignKey(TutorialResourceProductPage, 'tutorial')

    class Meta(DefaultMeta):
        queryset = models.vote.VoteTutorial.objects.all()
        resource_name = "votes/tutorial_p"
        authorization = Authorization()
        #authentication = SessionAuthentication()
        filtering = {
            "tutorial": ('exact',),
            "user": ('exact',),
        }


class VoteTutorialWithTutorialResource(DefaultModelResource):
    tutorial = fields.ForeignKey(TutorialResource, 'tutorial', full=True)

    class Meta(DefaultMeta):
        queryset = models.vote.VoteTutorial.objects.all()
        resource_name = "votes/tutorial_full"
        authorization = Authorization()
        # authentication = SessionAuthentication()
        filtering = {
            "tutorial": ('exact',),
            "user": ('exact',),
        }


class ProductResourceProductPage(DefaultModelResource):
    class Meta(DefaultMeta):
        queryset = models.core.Product.objects.all()
        resource_name = "product_p"
        authorization = Authorization()


#Landing page
class ProductResourceLandingPage(DefaultModelResource):
    images = fields.ManyToManyField(ImageResourceProductPage, 'productimages',
                                    null=True, blank=True, readonly=True,
                                    full=True)

    class Meta(DefaultMeta):
        queryset = models.core.Product.objects.all()
        resource_name = "product_l"
        authorization = Authorization()


class ShopResourceLandingPage(DefaultModelResource):
    images = fields.ManyToManyField(ImageResource, 'images', null=True,
                                    blank=True, readonly=True, full=True)

    class Meta(DefaultMeta):
        queryset = models.core.Shop.objects.all()
        resource_name = 'shop_l'
        authorization = Authorization()


class TopProductsResourceLandingPage(DefaultModelResource):
    product = fields.ForeignKey(ProductResourceLandingPage, 'product',
                                null=True, blank=True, readonly=True, full=True)

    class Meta(DefaultMeta):
        queryset = models.top.TopProducts.objects.all().order_by('-score')[:4]
        resource_name = "top_products"
        authorization = Authorization()


class TopUsersResourceLandingPage(DefaultModelResource):
    class Meta(DefaultMeta):
        queryset = models.core.User.objects.all().\
            exclude(username__isnull=True).\
            exclude(username__exact='').\
            exclude(first_name__isnull=True).\
            exclude(first_name__exact='').\
            annotate(makey_count=Count('makey')).\
            order_by('-makey_count')
        fields = ['id', 'username', 'first_name', 'last_name',
                  'first_name', 'last_name' 'facebook_id', 'date_joined',
                  'email']
        resource_name = "top_users"
        authorization = Authorization()


class TopUsersResourceRecoSubPage(DefaultModelResource):
    class Meta(DefaultMeta):
        queryset = models.core.User.objects.all().\
            exclude(username__isnull=True).\
            exclude(username__exact='').\
            exclude(first_name__isnull=True).\
            exclude(first_name__exact='').\
            annotate(article_count=Count('article')).\
            order_by('-article_count')
        fields = ['id', 'username', 'first_name', 'last_name',
                  'first_name', 'last_name' 'facebook_id', 'date_joined',
                  'email']
        resource_name = "top_reco_users"
        authorization = Authorization()


class TopShopsResourceLandingPage(DefaultModelResource):
    store = fields.ForeignKey(ShopResourceLandingPage, 'shop', null=True,
                              blank=True, readonly=True, full=True)

    class Meta(DefaultMeta):
        queryset = models.top.TopShops.objects.all().order_by('-score')[:4]
        resource_name = "top_stores"
        authorization = Authorization()


# Cfi Store Item Resources

class CfiStoreItemResource(DefaultModelResource):
    item = fields.OneToOneField(ProductResource, 'item', null=True, blank=True,
                                readonly=True, full=True)

    class Meta(DefaultMeta):
        queryset = models.misc.CfiStoreItem.objects.order_by('-score')
        resource_name = "cfi_store_item"
        authorization = Authorization()


class LikeCfiStoreItemResource(DefaultModelResource):
    cfi_store_item = fields.ForeignKey(CfiStoreItemResource, 'cfi_store_item',
                                       null=True, blank=True)
    liker = fields.ForeignKey(UserResource, 'user', null=True, blank=True,
                              full=True)

    class Meta(DefaultMeta):
        queryset = models.like.LikeCfiStoreItem.objects.order_by('?')
        resource_name = "likes/cfi_store_item"
        authorization = Authorization()
        #authentication = SessionAuthentication()

    def hydrate_liked_time(self, bundle):
        if bundle.data['liked_time'] == "Now" or \
                bundle.data['liked_time'] == "":
            bundle.data['liked_time'] = datetime.datetime.now()
        return bundle

    def hydrate_liker(self, bundle):
        if bundle.data['liker']:
            bundle.data['liker'] = User.objects.get(
                username=bundle.data['liker']['username'])
        return bundle


class LikeCfiStoreItemWithProductResource(DefaultModelResource):
    cfi_store_item = fields.ForeignKey(CfiStoreItemResource, 'cfi_store_item',
                                       null=True, blank=True, full=True)

    class Meta(DefaultMeta):
        queryset = models.like.LikeCfiStoreItem.objects.order_by('?')
        resource_name = "likes/cfi_store_item_with_product"
        authorization = Authorization()
        # authentication = SessionAuthentication()


class CfiStoreItemFullResource(DefaultModelResource):
    item = fields.OneToOneField(ProductResourceLandingPage, 'item', null=True,
                                blank=True, readonly=True, full=True)

    lambda_query = lambda bundle: bundle.obj.likers.through.objects.\
        filter(cfi_store_item=bundle.obj).order_by('?')
    likes = fields.ManyToManyField(LikeCfiStoreItemResource,
                                   attribute=lambda_query, null=True,
                                   blank=True, readonly=True, full=True)

    def obj_create(self, bundle, **kwargs):
        # some reason the onetoone field was not auto creating data.
        # so I had to manually create the item. - Alex

        # things to do before creating the object
        # print bundle.data["item_id"]
        # bundle.data["user"] = bundle.request.user
        # print bundle.data

        p = models.core.Product.objects.get(id=bundle.data["item_id"])
        if not models.misc.CfiStoreItem.objects.filter(item=p):
            cfistoreitem = models.misc.CfiStoreItem(item=p, added_time=
                                                    datetime.datetime.now())
            cfistoreitem.save()

        return

    class Meta(DefaultMeta):
        queryset = models.misc.CfiStoreItem.objects.order_by('-score')
        resource_name = "cfi_store_item_full"
        authorization = Authorization()
        throttle = BaseThrottle()


# Resources for Store page
class ProductShopUrlResource(DefaultModelResource):
    product = fields.ForeignKey(ProductResourceLandingPage, 'product',
                                full=True)
    shop = fields.ForeignKey(ShopResource, 'shop', full=True)

    class Meta(DefaultMeta):
        queryset = models.core.ProductShopUrl.objects.all()
        resource_name = "product_shop_url"
        authorization = Authorization()
        filtering = {
            "shop": ALL,
        }


class ShopReviewResource(DefaultModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=True)
    shop = fields.ForeignKey(ShopResource, 'shop')

    class Meta(DefaultMeta):
        queryset = models.review.ShopReview.objects.all()
        resource_name = "review/shop"
        authorization = Authorization()
        #authentication = SessionAuthentication()
        filtering = {
            "shop": ('exact',),
            "added_time": ('gte', 'lte',),
            "user": ('exact',),
        }


class VoteShopReviewResource(DefaultModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=True)
    review = fields.ForeignKey(ShopReviewResource, 'review')

    class Meta(DefaultMeta):
        queryset = models.vote.VoteShopReview.objects.all()
        resource_name = "votes/shop_review"
        authorization = Authorization()
        #authentication = SessionAuthentication()
        filtering = {
            "review": ('exact',),
            "user": ('exact',),
        }


class ShopReviewWithShopResource(DefaultModelResource):
    shop = fields.ForeignKey(ShopResource, 'shop', full=True)

    class Meta(DefaultMeta):
        queryset = models.review.ShopReview.objects.all()
        resource_name = "shop_review_with_shop"
        authorization = Authorization()
        # authentication = SessionAuthentication()
        filtering = {
            "shop": ('exact',),
        }


class VoteShopReviewWithReviewResource(DefaultModelResource):
    review = fields.ForeignKey(ShopReviewWithShopResource, 'review', full=True)

    class Meta(DefaultMeta):
        queryset = models.vote.VoteShopReview.objects.all()
        resource_name = "votes/shop_review_full"
        authorization = Authorization()
        #authentication = SessionAuthentication()
        filtering = {
            "review": ('exact',),
            "user": ('exact',),
        }


# User Interactions
class UserInteractionResource(DefaultModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=True)

    class Meta(DefaultMeta):
        queryset = models.interactions.UserInteraction.objects.\
            exclude(event=models.interactions.Interaction.click_shopurl).\
            order_by('-id')
        resource_name = "user_interactions"
        authorization = Authorization()
        # authentication = SessionAuthentication()
        filtering = {
            'user': ('exact',),
            'event': ALL,
            'added_time': ('lte', 'gte',),
        }


class ShopUrlClicks(DefaultModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=True)

    class Meta(DefaultMeta):
        queryset = models.interactions.UserInteraction.objects.\
            filter(event=models.interactions.Interaction.click_shopurl).\
            order_by('-id')
        resource_name = "shop_url_clicks"
        authorization = Authorization()
        #authentication = SessionAuthentication()
        filtering = {
            'user': ('exact',),
            'added_time': ('lte', 'gte',),
        }


# Maker page
class MakeyResourceMakerPage(DefaultModelResource):
    user = fields.ForeignKey(UserResource, 'user', null=True, blank=True,
                             full=True)
    collaborators = fields.ManyToManyField(UserResource, 'collaborators',
                                           null=True, blank=True, full=True)
    images = fields.ManyToManyField(ImageResource, 'images', null=True,
                                    blank=True, full=True)
    parts = fields.ManyToManyField(ProductResourceMakeyPage, 'partsused',
                                   null=True, blank=True)
    notes = fields.ManyToManyField(NoteResource, 'notes', null=True, blank=True)

    class Meta(DefaultMeta):
        queryset = models.core.Makey.objects.all().order_by('id').\
            filter(is_enabled=True)
        resource_name = 'makey_m'
        #authentication = SessionAuthentication()
        authorization = MakeyAuthorization()
        filtering = {
            'user': ('exact',),
            'added_time': ('gte', 'lte',),
            'collaborators': ALL,
            # 'made_in':ALL_WITH_RELATIONS,
            'made_in': ALL,
            'parts': ALL,
            'notes': ALL
        }

    # def dehydrate(self, bundle):
    #     requestor = bundle.request.user
    #     if bundle.obj.is_private:
    #         if requestor not in bundle.obj.collaborators.all()\
    #             and requestor not in API_ADMINS:
    #             return

    #     return bundle


# Search page
class MakeyResourceSearchPage(DefaultModelResource):
    collaborators = fields.ManyToManyField(UserResource, 'collaborators',
                                           null=True, blank=True, full=True)
    tags = fields.ToManyField(MyTagResource, 'tags', null=True, blank=True,
                              full=True)

    class Meta(DefaultMeta):
        queryset = models.core.Makey.objects.all().order_by('id').reverse().\
            filter(is_enabled=True)
        resource_name = 'makey_s'
        authorization = ReadOnlyAuthorization()
        always_return_data = True

    def dehydrate(self, bundle):
        bundle.data['images_count'] = bundle.obj.images.count()
        bundle.data['insights_count'] = bundle.obj.notes.count()
        bundle.data['parts_count'] = bundle.obj.partsused.count() +\
            bundle.obj.new_parts.count()
        cover_pic_url = ""
        if bundle.obj.cover_pic:
            cover_pic_url = bundle.obj.cover_pic.large_url
        elif bundle.obj.images.count():
            cover_pic_url = bundle.obj.images.all()[0].large_url
        else:
            cover_pic_url = "static_default"
        bundle.data["cover_pic_url"] = cover_pic_url
        return bundle

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_search'), name="api_get_search"),
        ]

    def get_search(self, request, **kwargs):
        q = request.GET.get('q', '')
        if q:
            makeys = models.core.Makey.objects\
                .filter(is_enabled=True)\
                .filter(Q(name__icontains=q) |
                        Q(tags__name__icontains=q))\
                .distinct()

            results = []
            for makey in makeys:
                if makey.user:
                    bundle = self.build_bundle(obj=makey, request=request)
                    bundle = self.full_dehydrate(bundle)
                    results.append(bundle)
            results_list = {
                'makeys': results,
            }
            return self.create_response(request, results_list)


class SpaceResourceMakerPage(DefaultModelResource):
    # user = fields.ForeignKey(UserResource, 'user', null=True, blank=True,
    #                          full=True)
    members = fields.ManyToManyField(UserResource, 'members', null=True,
                                     blank=True, full=True)
    makeys = fields.ManyToManyField(TopMakeysResourceLandingPage,
                                    'makeys_made_in', null=True, blank=True,
                                    full=True)
    # tools = fields.ManyToManyField(ProductResource, 'tools',null=True,
    #    blank=True, full=True)
    # images = fields.ManyToManyField(ImageResource, 'images', null=True,
    #                                 blank=True, full=True)

    class Meta(DefaultMeta):
        queryset = models.core.Space.objects.all().order_by('id').\
            filter(is_enabled=True)
        resource_name = 'space_m'
        #authentication = SessionAuthentication()
        authorization = Authorization()
        filtering = {
            'user': ('exact',),
            'added_time': ('gte', 'lte',),
            'members': ALL,
        }


class UserProfileResource(DefaultModelResource):
    user = fields.ForeignKey(UserResource, 'user', null=True, blank=True,
                             full=True)
    following = fields.ManyToManyField("self", 'following', null=True,
                                       blank=True,)
    followers = fields.ManyToManyField("self", 'followers', null=True,
                                       blank=True,)

    class Meta(DefaultMeta):
        queryset = models.core.UserProfile.objects.all()
        resource_name = 'profile'
        authorization = Authorization()
        filtering = {
            'user': ('exact', ),
        }

    def dehydrate(self, bundle):
        bundle.data['makeys_count'] = models.core.Makey.objects.\
            filter(collaborators__in=[bundle.obj.user.id]).\
            filter(is_enabled=True).count()
        return bundle


class UserFullResource(DefaultModelResource):
    profile = fields.ForeignKey(UserProfileResource, 'profile', full=True)

    class Meta(DefaultMeta):
        queryset = User.objects.all()
        resource_name = "user_full"
        fields = ['id', 'username', 'first_name', 'last_name', 'last_login',
                  'first_name', 'last_name', 'date_joined']
        authorization = Authorization()
        allowed_methods = ['get']
        filtering = {
            'date_joined': ('lte', 'gte'),
        }


class Note2Resource(DefaultModelResource):
    user = fields.ForeignKey(UserResource, 'user', null=True, blank=True,
                             full=True)
    comments = fields.ManyToManyField(CommentResource, 'comments', null=True,
                                      blank=True)
    image = fields.ForeignKey(ImageResource, 'image', null=True, blank=True)
    makey = fields.ManyToManyField(MakeyResourceMakerPage, 'makeynotes',
                                   full=True)

    class Meta(DefaultMeta):
        queryset = models.core.Note.objects.all()
        resource_name = "note2"
        authorization = Authorization()
        #authentication = SessionAuthentication()
        filtering = {
            'user': ALL_WITH_RELATIONS,
            # 'user': ALL,
        }

    def hydrate_image(self, bundle, request=None, **kwargs):
        if bundle.data['image'] == '':
            bundle.data['image'] = None

        return bundle

    # def dehydrate(self, bundle):
    #     try:
    #         social = SocialAccount.objects.get(user_id=bundle.obj.id)
    #         bundle.data['profile_url'] = social.get_avatar_url()

    #         fb_account = SocialAccount.objects.get(user_id=bundle.obj.id,
    #                                                provider='facebook')
    #         bundle.data['facebook_id'] = fb_account.uid
    #     except:
    #         pass
    #     return bundle


class SendMailResource(DefaultModelResource):
    class Meta(DefaultMeta):
        queryset = SendMail.objects.all()
        resource_name = 'send_mail'
        authorization = Authorization()


class ListingResource(DefaultModelResource):
    class Meta(DefaultMeta):
        queryset = models.core.Listing.objects.all()
        resource_name = "listing"
        authorization = Authorization()


class LikeListingResource(DefaultModelResource):
    liker = fields.ForeignKey(UserResource, 'user', full=True)
    listing = fields.ForeignKey(ListingResource, 'listing',)

    class Meta(DefaultMeta):
        queryset = models.like.LikeListing.objects.order_by('?')
        resource_name = "likes/listing"
        authorization = Authorization()
        filtering = {
            'listing': 'exact',
            'liker': 'exact',
        }


class TopTagsResource(DefaultModelResource):
    class Meta(DefaultMeta):
        queryset = models.core.ArticleTag.objects.all().\
            annotate(article_count=Count('article')).\
            order_by('-article_count')

        resource_name = 'top_tags'
        authorization = Authorization()
        include_resource_uri = False
        always_return_data = True

    def dehydrate(self, bundle):
        bundle.data['article_count'] = models.core.Article.objects.\
            filter(tags=bundle.obj.id).\
            filter(is_enabled=True).\
            count()
        return bundle


class TagResource(DefaultModelResource):
    class Meta(DefaultMeta):
        queryset = models.core.ArticleTag.objects.all()
        resource_name = "tags"
        authorization = Authorization()

    def dehydrate(self, bundle):
        bundle.data['article_count'] = models.core.Article.objects.\
            filter(tags=bundle.obj.id).\
            filter(is_enabled=True).\
            count()
        return bundle

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_search'), name="api_get_search"),
        ]

    def get_search(self, request, **kwargs):
        q = request.GET.get('q', '')
        if q:
            tags = models.core.ArticleTag.objects\
                .filter(is_enabled=True)\
                .filter(Q(name__icontains=q))

            results = []
            for tag in tags:
                bundle = self.build_bundle(obj=tag, request=request)
                bundle = self.full_dehydrate(bundle)
                results.append(bundle)
            results_list = {
                'tags': results,
            }
            return self.create_response(request, results_list)


class LikeChannelResource(DefaultModelResource):
    liker = fields.ForeignKey(UserResource, 'user', full=True)
    channel = fields.ForeignKey(TagResource, 'channel',)

    class Meta(DefaultMeta):
        queryset = models.like.LikeChannel.objects.order_by('?')
        resource_name = "likes/channel"
        authorization = Authorization()
        filtering = {
            'channel': 'exact',
            'liker': 'exact',
        }


class StepResource(DefaultModelResource):
    makey = fields.ForeignKey(MakeyResource, 'makey')

    class Meta(DefaultMeta):
        queryset = models.core.InstructableStep.objects.all()
        resource_name = "step"
        authorization = Authorization()


class FavoriteMakeyResource(DefaultModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=True)
    makey = fields.ForeignKey(MakeyResource, 'makey',)

    class Meta(DefaultMeta):
        queryset = models.core.FavoriteMakey.objects.order_by('?')
        resource_name = "favorites/makey"
        authorization = Authorization()
        filtering = {
            'makey': 'exact',
            'user': 'exact',
        }


class QuestionResource(DefaultModelResource):
    creator = fields.ForeignKey(UserResource, 'creator', null=True, blank=True,
                                full=True)
    accepted_answer = fields.ForeignKey('woot.apps.catalog.api.AnswerResource',
                                        'accepted_answer', null=True,
                                        blank=True)
    makey = fields.ForeignKey(MakeyResource, 'makey')

    class Meta(DefaultMeta):
        queryset = models.forum.Question.objects.all()
        resource_name = 'question'
        authorization = Authorization()


class AnswerResource(DefaultModelResource):
    question = fields.ForeignKey(QuestionResource, 'question')
    creator = fields.ForeignKey(UserResource, 'creator', null=True, blank=True,
                                full=True)

    class Meta(DefaultMeta):
        queryset = models.forum.Answer.objects.all()
        resource_name = 'answer'
        authorization = Authorization()