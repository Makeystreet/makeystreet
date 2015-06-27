import re
import json

from urllib2 import urlopen
from urlparse import urlparse, parse_qs

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.utils import timezone

from allauth.socialaccount.models import SocialAccount
from dj.choices import Choices, Choice
from opengraph import OpenGraph
from tinymce.models import HTMLField

from .abstract import BaseModel
from .helpers import unique_slugify
from .forum import Answer
from taggit.managers import TaggableManager

class Comment(BaseModel):
    user = models.ForeignKey(User)
    body = models.TextField(null=True, blank=True)
    likes_count = models.IntegerField(default=0)

    question = models.ForeignKey('Question', null=True, blank=True,
                                 related_name='comments')
    answer = models.ForeignKey('Answer', null=True, blank=True,
                               related_name='comments')

    class Meta:
        app_label = 'catalog'
        ordering = ['-added_time']

    def __unicode__(self):
        return self.body

    def short_description(self):
        tail = '...' if len(self.body) > 50 else ''
        return self.body[:50] + tail


# Regular expression to fetch title from a given url
url_title_regex = re.compile('<title>(.*?)</title>', re.IGNORECASE | re.DOTALL)


class Documentation(BaseModel):
    user = models.ForeignKey(User, null=True, blank=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    url = models.URLField(max_length=1000)
    order = models.IntegerField(default=0)

    class Meta:
        app_label = 'catalog'

    def __unicode__(self):
        return self.url

    def save(self, *args, **kwargs):
        if(self.url[:4] != "http"):
            self.url = "http://" + self.url

        # TODO: See if we can return the existing documentation instead of a
        # new one
        # existing = Documentation.objects.filter(url = self.url)
        # if(len(existing) != 0):
        #     self = existing[0]
        # else:
        if not self.title:
            try:
                pageData = urlopen(self.url).read()
                self.title = url_title_regex.search(pageData).\
                    group(1).decode('utf-8')
            except ValueError:
                self.title = self.url
        super(Documentation, self).save(*args, **kwargs)


class UpFile(BaseModel):
    user = models.ForeignKey(User)
    filename = models.CharField(max_length=200)
    filetype = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField(max_length=1000)
    description = models.TextField(max_length=1000, null=True, blank=True)

    makey = models.ForeignKey('Makey', null=True, blank=True,
                              related_name='files')

    tags = TaggableManager(blank=True)

    class Meta:
        app_label = 'catalog'

    def __unicode__(self):
        return self.filename


class Image(BaseModel):
    user = models.ForeignKey(User, null=True, blank=True, related_name="images")
    large_url = models.URLField(max_length=1000, null=True, blank=True)
    small_url = models.URLField(max_length=1000, null=True, blank=True)
    full_url = models.URLField(max_length=1000, null=True, blank=True)
    in_s3 = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    comments = models.ManyToManyField(Comment, null=True, blank=True)
    likes_count = models.IntegerField(default=0)
    description = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        app_label = 'catalog'

    def __unicode__(self):
        return self.large_url

    def save(self, *args, **kwargs):
        if self.large_url[:2] == "//":
            self.large_url = 'http:' + self.large_url
        super(Image, self).save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     super(Image, self).save(*args, **kwargs)
    #     self.create_thumbs()

    # def create_thumbs(self):
    #     if(self.small_url):
    #         # print("Thumb exists")
    #         return

    #     if '/temp_uploads/' not in self.large_url:
    #         return

    #     # print("Thumb doesnt exist")
    #     import os
    #     import urllib
    #     from PIL import Image as Im
    #     from django.core.files.storage import default_storage as storage

    #     year = timezone.now().year
    #     month = timezone.now().month

    #     # print('large_url: ' + self.large_url)
    #     filename = urllib.unquote(self.large_url).\
    #         replace(storage.url('/temp_uploads/'), '').\
    #         replace('/', '')  # image_name.jpg
    #     filename_base, filename_ext = os.path.splitext(filename)
    #     # print("filename: " + filename)

    #     temp_img = Im.open(storage.open('/temp_uploads/' + filename, 'r'))

    #     # Create resized large image 450px x 450px
    #     large_location = "/" + str(year) + "/" + str(month) + "/" + \
    #         filename_base + "_large.jpg"
    #     file_large = storage.open(large_location, 'w')
    #     temp_img.thumbnail((450, 450), Im.ANTIALIAS)
    #     temp_img.save(file_large, "JPEG")
    #     file_large.close()
    #     # print("large: "+ large_location)

    #     # Create thumbnail - 250px x 150px
    #     small_location = "/" + str(year) + "/" + str(month) + "/" + \
    #         filename_base + "_small.jpg"
    #     file_small = storage.open(small_location, 'w')
    #     temp_img.thumbnail((250, 150), Im.ANTIALIAS)
    #     temp_img.save(file_small, "JPEG")
    #     file_small.close()
    #     # print("small: " + small_location)

    #     # Delete temp image
    #     storage.delete('/temp_uploads/' + filename)
    #     # print("temp deleted")

    #     self.large_url = storage.url(large_location)
    #     self.small_url = storage.url(small_location)
    #     super(Image, self).save()
    #     # print("image saved: " + str(self.id))


class TextDocumentation(BaseModel):
    user = models.ForeignKey(User, null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    body = HTMLField()
    images = models.ManyToManyField(Image, null=True, blank=True)

    makey = models.ForeignKey('Makey', null=True, blank=True,
                              related_name='text_documentations')

    order = models.IntegerField(default=0)

    tags = TaggableManager(blank=True)

    class Meta:
        app_label = 'catalog'

    def __unicode__(self):
        return self.title


class Note(BaseModel):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    likes_count = models.IntegerField(default=0,)
    comments = models.ManyToManyField(Comment, null=True, blank=True,)
    order = models.IntegerField(default=0)
    image = models.ForeignKey(Image, null=True, blank=True)
    is_pending_approval = models.BooleanField(default=False)
    tags = TaggableManager(blank=True)

    class Meta:
        app_label = 'catalog'
        ordering = ['order']

    def __unicode__(self):
        return str(self.id) + ' - ' + self.title

    def save(self, *args, **kwargs):
        super(Note, self).save(*args, **kwargs)


class VideoSite(Choices):
    dailymotion = Choice('Dailymotion')
    facebook = Choice('Facebook')
    metacafe = Choice('Metacafe')
    vimeo = Choice('Vimeo')
    yahoo = Choice('Yahoo! Video')
    youtube = Choice('YouTube')


class Video(BaseModel):
    user = models.ForeignKey(User, null=True, blank=True)
    url = models.URLField(max_length=200)
    embed_url = models.URLField(max_length=200)
    thumb_url = models.URLField(max_length=200)
    site = models.IntegerField(choices=VideoSite())
    order = models.IntegerField(default=0)
    comments = models.ManyToManyField(Comment, null=True, blank=True)
    likes_count = models.IntegerField(default=0)
    description = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        app_label = 'catalog'

    def __unicode__(self):
        return self.url

    def save(self, *args, **kwargs):
        current_site = VideoSite.FromID(self.site)
        self.site = current_site

        if current_site == VideoSite.youtube:
            video_id = parse_qs(urlparse(self.url).query)['v'][0]
            self.embed_url = '//www.youtube.com/embed/' + video_id
            self.thumb_url = 'http://img.youtube.com/vi/' + video_id + '/0.jpg'
        elif current_site == VideoSite.vimeo:
            video_id = urlparse(self.url).path.lstrip("/")
            _json = json.loads(urlopen('http://vimeo.com/api/v2/video/' +
                                       str(video_id) + ".json").read())[0]
            self.url = _json['url']
            self.embed_url = '//player.vimeo.com/video/' + video_id
            self.thumb_url = _json['thumbnail_small']

        super(Video, self).save(*args, **kwargs)


def makey_image_upload_to(makey_image_instance, fileName):
    return "makey/" + makey_image_instance.makey_id + "/" + fileName


class MakeyImage(BaseModel):
    makey_id = models.IntegerField()
    image = models.ImageField(upload_to=makey_image_upload_to)


class NewProduct(BaseModel):
    name = models.CharField(max_length=200)
    url = models.URLField()
    user = models.ForeignKey(User, null=True, blank=True)
    image = models.ForeignKey(Image, null=True, blank=True)

    class Meta:
        app_label = 'catalog'

    def __unicode__(self):
        return self.name + " (" + self.url + ")"

    def __fetch_open_graph_details(self):
        try:
            og = OpenGraph(url=self.url)
            if og.is_valid():
                _json = json.loads(og.to_json())
                self.name = _json['title']

                img = Image(user=self.user, large_url=_json['image'],
                            added_time=timezone.now())
                img.save()
                self.image = img
        except Exception as e:
            print(e.__doc__)
            print(e.message)
        return

    def save(self, *args, **kwargs):
        if(self.url[:4] != "http"):
            self.url = "http://" + self.url
        self.__fetch_open_graph_details()
        super(NewProduct, self).save(*args, **kwargs)


class NewUser(BaseModel):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    class Meta:
        app_label = 'catalog'

    def __unicode__(self):
        return self.name


class MakeyManager(models.Manager):
    def __fetch_makeys_with_parts(self, parts, parts_count, present_count):
        _query = super(MakeyManager, self)

        query = _query

        if parts_count == 0:
            return []
        elif parts_count == 1:
            query = query.filter(partsused__in=[parts[0].id, ]).\
                filter(is_enabled=True)
            temp_count = present_count + 1
            for m in query:
                m.sort_id = temp_count
                temp_count += 1
        else:
            for part in parts[:parts_count]:
                query = query.filter(partsused__in=[part.id, ])
            query.filter(is_enabled=True)

            temp_count = present_count + 1
            for m in query:
                m.sort_id = temp_count
                temp_count += 1

            present_count += len(query)
            if present_count < 3:
                query2 = self.__fetch_makeys_with_parts(parts, parts_count-1,
                                                        present_count)

                from itertools import chain
                query = list(set(chain(query, query2)))
                query = sorted(query, key=lambda x: x.sort_id)

        return list(query)

    def __fetch_top_makeys(self):
        _query = super(MakeyManager, self).all().order_by('-score').\
            filter(is_enabled=True)
        return list(_query)

    def __similar_makeys(self, makey):
        parts = makey.partsused.all().order_by('-score')
        list_of_makeys = self.__fetch_makeys_with_parts(parts, len(parts), 0)

        if makey in list_of_makeys:
            list_of_makeys.remove(makey)

        if len(list_of_makeys) == 0:
            list_of_makeys = self.__fetch_top_makeys()
            if makey in list_of_makeys:
                list_of_makeys.remove(makey)

        return list_of_makeys

    def similar(self, makey_id):
        cur_makey = super(MakeyManager, self).get(id=makey_id)
        return self.__similar_makeys(cur_makey)


class Space(BaseModel):
    name = models.CharField(max_length=200)  # null=True, blank=True)
    status = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    kind = models.CharField(max_length=200, null=True, blank=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    twitter = models.URLField(max_length=200, blank=True, null=True)
    facebook = models.URLField(max_length=200, blank=True, null=True)
    logo = models.URLField(max_length=400, blank=True, null=True)
    latitude = models.DecimalField(default=0, decimal_places=10, max_digits=15,
                                   blank=True, null=True)
    longitude = models.DecimalField(default=0, decimal_places=10,
                                    max_digits=15, blank=True, null=True)
    map_zoom_level = models.IntegerField(default=13)
    description = models.TextField(blank=True, null=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    no_of_members = models.CharField(max_length=200, null=True, blank=True)
    membership_fee = models.CharField(max_length=200, null=True, blank=True)
    date_of_founding = models.CharField(max_length=200, null=True, blank=True)
    last_updated_external = models.CharField(max_length=200, null=True,
                                             blank=True)
    # mentors = models.TextField(blank=True, null=True)
    # status = models.TextField(blank=True, null=True)
    # why = models.TextField(blank=True, null=True)
    admins = models.ManyToManyField(User, null=True, blank=True,
                                    related_name='space_admins')
    members = models.ManyToManyField(User, null=True, blank=True,
                                     related_name='space_members')
    new_members = models.ManyToManyField(NewUser,  null=True, blank=True,
                                         related_name='space_new_members')
    new_tools = models.ManyToManyField(NewProduct, null=True, blank=True,
                                       related_name='space_new_tools')
    inventory = models.ManyToManyField('Product', through='Inventory',
                                       related_name='space_inventory')
    new_inventory = models.ManyToManyField('NewProduct', through='NewInventory',
                                       related_name='space_new_inventory')
    comments = models.ManyToManyField(Comment, null=True, blank=True)



    class Meta:
        app_label = 'catalog'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/space/%i/" % self.id

    def pub_date(self):
        return self.added_time


class Inventory(BaseModel):
    part = models.ForeignKey('Product', related_name='inventory_part')
    space = models.ForeignKey(Space, related_name='inventory_space')
    quantity = models.IntegerField(default=1, null=True, blank=True)

    class Meta:
        app_label = 'catalog'
        unique_together = (("part", "space"),)

    def __unicode__(self):
        return '(%s - %s - %s)' % (self.space, self.part, self.quantity)


class NewInventory(BaseModel):
    part = models.ForeignKey('NewProduct', related_name='new_inventory_part')
    space = models.ForeignKey(Space, related_name='new_inventory_space')
    quantity = models.IntegerField(default=1, null=True, blank=True)

    class Meta:
        app_label = 'catalog'
        unique_together = (("part", "space"),)

    def __unicode__(self):
        return '(%s - %s - %s)' % (self.space, self.part, self.quantity)


class BOM(BaseModel):
    name = models.TextField();
    quantity = models.IntegerField(default=1, null=True, blank=True)
    makey = models.ForeignKey('Makey', related_name="bom")
    comments = models.TextField(null=True, blank=True)

    class Meta:
        app_label = 'catalog'

    def __unicode__(self):
        return '(%s - %s - %s)' % (self.name, self.quantity, self.makey)


class Makey(BaseModel):
    #custom manager
    objects = MakeyManager()
    tags = TaggableManager(blank=True)

    user = models.ForeignKey(User, null=True, blank=True)
    name = models.CharField(max_length=200)   # , null=True, blank=True)
    url = models.URLField(max_length=200, blank=True, null=True)
    about = models.CharField(max_length=200, null=True, blank=True)
    why = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    collaborators = models.ManyToManyField(User, null=True, blank=True,
                                           related_name='collaborators')
    comments = models.ManyToManyField(Comment, null=True, blank=True,
                                      related_name='makeycomments')
    notes = models.ManyToManyField(Note, related_name="makeynotes", null=True,
                                   blank=True)
    documentations = models.ManyToManyField(Documentation,
                                            related_name="makeydocumentations",
                                            null=True, blank=True)
    images = models.ManyToManyField(Image, related_name="makeyimages",
                                    null=True, blank=True)
    cover_pic = models.ForeignKey(Image, null=True, blank=True)
    votes = models.IntegerField(default=0, blank=True, null=True)
    new_users = models.ManyToManyField(NewUser,  null=True, blank=True,
                                       related_name='makeys')
    videos = models.ManyToManyField(Video, related_name="makeyvideos",
                                    null=True, blank=True)
    new_parts = models.ManyToManyField(NewProduct, null=True, blank=True,
                                       related_name='makeys_parts')
    new_tools = models.ManyToManyField(NewProduct, null=True, blank=True,
                                       related_name='makeys_tools')
    made_in = models.ForeignKey(Space, null=True, blank=True,
                                related_name='makeys_made_in')

    credits = models.TextField(blank=True, null=True)
    mentors = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)

    removed_collaborators = models.ManyToManyField(User, null=True, blank=True,
                                                   related_name="makey_removed")
    modules_used = models.ManyToManyField('self', null=True, blank=True,
                                          symmetrical=False,
                                          related_name='used_in')
    derived_from = models.ForeignKey('self', null=True, blank=True,
                                     related_name='forked_as')
    as_part = models.ForeignKey('Product', null=True, blank=True,
                                related_name='as_makey')

    as_part_new = models.ForeignKey('NewProduct', null=True, blank=True,
                                    related_name='as_makey')

    is_private = models.BooleanField(default=False)

    is_staff_pick = models.BooleanField(default=False)
    added_time_staff_pick = models.DateTimeField('added time staff pick',
                                                 null=True, blank=True)

    slug = models.SlugField(db_index=True, null=True, blank=True)
    github_url = models.URLField(null=True, blank=True)

    class Meta:
        app_label = 'catalog'
        unique_together = (('user', 'slug'),)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:makey_new_slug', kwargs={
            'username': self.user.username,
            'makey_slug': self.slug,
        })

    def pub_date(self):
        return self.added_time

    def save(self, *args, **kwargs):
        if not self.id:
            unique_slugify(self, self.name)
        super(Makey, self).save(*args, **kwargs)

    def get_parent_makeys(self):
        if self.used_in.count() == 1:
            parent = self.used_in.all()[0]
            return parent.get_parent_makeys() + [parent]
        elif self.used_in.count() == 0:
            return []
        else:
            parents = self.used_in.all();
            parents = sorted(parents, key=lambda x: x.added_time)
            parent = parents[0]
            return parent.get_parent_makeys() + [parent]

    def search_content(self, query):
        notes = self.notes.filter(Q(title__icontains=query) |
                                  Q(body__icontains=query))

        # questions = self.question_set.filter(Q(name__icontains=query) |
        #                                      Q(description__icontains=query))

        # answers = Answer.objects.search_content_in_makey(self, query)

        bom = self.bom.filter(Q(name__icontains=query) |
                            Q(comments__icontains=query))

        result = ((self, {
            'notes': notes,
            # 'answers': answers,
            # 'questions': questions,
            # 'count': notes.count() + answers.count() + questions.count(),
            'bom':bom,
            'count': notes.count() + bom.count(),
        }), )

        return result

    def search_in_submodules(self, query):
        result = self._search_in_submodules(query, [])

        return result

    def _search_in_submodules(self, query, searched_makeys_list):
        if not self.id in searched_makeys_list:
            searched_makeys_list.append(self.id)
            result = self.search_content(query)

            for makey in self.modules_used.exclude(id=self.id):
                result += makey._search_in_submodules(query,
                                                      searched_makeys_list)
            return result
        else:
            return ()


class Tutorial(BaseModel):
    user = models.ForeignKey(User, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField(max_length=200)
    votes = models.IntegerField(default=0)
    images = models.ManyToManyField(Image, related_name="tutorialimages",
                                    null=True, blank=True)

    class Meta:
        app_label = 'catalog'

    def __unicode__(self):
        return self.url


class Product(BaseModel):
    sku = models.IntegerField()
    name = models.CharField(max_length=200)

    makeys = models.ManyToManyField(Makey, blank=True, related_name="partsused")
    makeys_as_tools = models.ManyToManyField(Makey, blank=True,
                                             related_name="tools_used")
    # makey_removed = models.ManyToManyField(Makey, blank=True,
    #                                        related_name="removed_parts")
    space_as_tools = models.ManyToManyField(Space, null=True, blank=True,
                                            related_name='tools_in_space')

    tutorials = models.ManyToManyField(Tutorial, blank=True,
                                       related_name="products")

    # identicalto is forwarding the user to the new product id.
    # This is required when existing products are identified as identical
    # to some other product
    identicalto = models.ForeignKey('self', null=True, blank=True)
    # likers = models.ManyToManyField(User, through="LikeProduct",
    #                                 related_name="product_likes")

    class Meta:
        app_label = 'catalog'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/product/%i/" % self.id

    def pub_date(self):
        return self.added_time


class Location(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = 'catalog'

    def __unicode__(self):
        return self.name


class Shop(BaseModel):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=100, blank=True)
    url = models.URLField(max_length=200)
    location = models.ForeignKey(Location)

    images = models.ManyToManyField(Image, related_name="shopimages", null=True,
                                    blank=True)
    # likes = models.ManyToManyField(Like, null=True, blank=True,
    # related_name='storelikes')
    # likes = models.ManyToManyField(User, through="LikeShop",
    #                                related_name="shop_likes")

    class Meta:
        app_label = 'catalog'

    def __unicode__(self):
        return self.name


class ProductShopUrl(BaseModel):
    url = models.URLField(max_length=200)
    product = models.ForeignKey(Product, related_name='productshopurls')
    shop = models.ForeignKey(Shop)

    class Meta:
        app_label = 'catalog'

    def __unicode__(self):
        return self.url


class ProductImage(BaseModel):
    url = models.URLField(max_length=200)
    user = models.ForeignKey(User, null=True, blank=True)
    shop = models.ForeignKey(Shop, null=True, blank=True)
    product = models.ForeignKey(Product, related_name='productimages')

    class Meta:
        app_label = 'catalog'

    def __unicode__(self):
        return self.url


class ProductDescription(BaseModel):
    description = models.CharField(max_length=100000)
    product = models.ForeignKey(Product, related_name='productdescriptions')
    user = models.ForeignKey(User, blank=True)
    shop = models.ForeignKey(Shop, blank=True)
    #user_or_shop : True for shop, false for user
    user_or_shop = models.BooleanField()

    class Meta:
        app_label = 'catalog'

    def __unicode__(self):
        return self.product.name


class UserFlags(BaseModel):
    show_makey_intro = models.BooleanField(default=True)
    show_maker_intro = models.BooleanField(default=True)
    user = models.ForeignKey(User)

    class Meta:
        app_label = 'catalog'


class UserProfile(BaseModel):
    user = models.OneToOneField(User, related_name='profile')
    following = models.ManyToManyField("self", symmetrical=False,
                                       related_name='followers',
                                       null=True, blank=True)
    instructables_url = models.URLField(max_length=1000, null=True, blank=True)
    github_url = models.URLField(max_length=1000, null=True, blank=True)
    linkedin_url = models.URLField(max_length=1000, null=True, blank=True)
    facebook_url = models.URLField(max_length=1000, null=True, blank=True)
    twitter_url = models.URLField(max_length=1000, null=True, blank=True)
    yt_channel_url = models.URLField(max_length=1000, null=True, blank=True)
    stackoverflow_url = models.URLField(max_length=1000, null=True, blank=True)
    blog_url = models.URLField(max_length=1000, null=True, blank=True)
    website_url = models.URLField(max_length=1000, null=True, blank=True)
    aboutme = models.TextField(blank=True, null=True)
    membership = models.TextField(blank=True, null=True)
    college = models.TextField(blank=True, null=True)
    patent = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, default='Bangalore, India')
    profile_pic = models.ForeignKey(Image, null=True, blank=True)

    class Meta:
        app_label = 'catalog'

    def profile_img_url(self):
        social = SocialAccount.objects.filter(user_id=self.user.id)

        if len(social):
            return social[0].get_avatar_url()

        return "https://makeystatic.s3.amazonaws.com/images/newuser.gif"
        # return "http://www.gravatar.com/avatar/{}?s=150".\
        #     format(hashlib.md5(self.user.email).hexdigest())

    def __unicode__(self):
        return unicode(self.user)


class Listing(BaseModel):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    content = HTMLField()
    likes_count = models.IntegerField(default=0)
    admins = models.ManyToManyField(User, null=True, blank=True)

    class Meta:
        app_label = 'catalog'

    def __unicode__(self):
        return self.company + " - " + self.title


class ArticleTag(BaseModel):
    name = models.CharField(max_length=200)
    url_snippet = models.CharField(max_length=200, unique=True)
    likes_count = models.IntegerField(default=0)

    class Meta:
        app_label = 'catalog'

    def __unicode__(self):
        return self.name


class Article(BaseModel):
    url = models.URLField()
    title = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    rating = models.IntegerField()
    recommendation = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    tags = models.ManyToManyField(ArticleTag, null=True, blank=True)
    comments = models.ManyToManyField(Comment, null=True, blank=True)
    new_user = models.ForeignKey('NewUser', null=True, blank=True)
    is_staff_pick = models.BooleanField(default=False)
    added_time_staff_pick = models.DateTimeField('added time staff pick',null=True,blank=True)

    class Meta:
        app_label = 'catalog'

    def __unicode__(self):
        return self.title + ' (' + self.url + ')'

    def __fetch_open_graph_details(self):
        try:
            og = OpenGraph(url=self.url)
            if og.is_valid():
                _json = json.loads(og.to_json())
                self.title = self.title or _json['title']
                self.description = self.description or _json['description']
                self.image_url = self.image_url or _json['image']
        except Exception as e:
            print(e.__doc__)
            print(e.message)
        return

    def save(self, *args, **kwargs):
        if(self.url[:4] != "http"):
            self.url = "http://" + self.url
        self.__fetch_open_graph_details()
        super(Article, self).save(*args, **kwargs)


class InstructableStep(BaseModel):
    # iid = instructables id
    iid = models.CharField(max_length=50, default=None, null=True)
    user = models.ForeignKey(User)
    url = models.URLField(null=True, default=None)
    title = models.CharField(max_length=200)
    body = HTMLField()
    step = models.IntegerField(default=-1)
    words = models.IntegerField(default=-1)
    images = models.ManyToManyField(Image, null=True, blank=True)
    makey = models.ForeignKey(Makey)

    class Meta:
        app_label = 'catalog'
        ordering = ['-step']

    def __unicode__(self):
        return self.title


class FavoriteMakey(BaseModel):
    user = models.ForeignKey(User)
    makey = models.ForeignKey(Makey)

    class Meta:
        app_label = 'catalog'
        unique_together = (("user", "makey"))

    def __unicode__(self):
        return self.user.username + " fav'ed " + self.makey.name


class Collection(BaseModel):
    name = models.CharField(max_length=300)
    makeys = models.ManyToManyField(Makey, null=True, blank=True,
                                    related_name='collections')

    class Meta:
        app_label = 'catalog'

    def __unicode__(self):
        return self.name

