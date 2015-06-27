from _ast import Is
import logging
import operator
import string
import unicodedata

import hmac
import base64
import urllib
from hashlib import sha1
import time
import json

from django.conf import settings
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, Http404,\
    HttpResponseBadRequest
from django.shortcuts import render, render_to_response, redirect,\
    get_object_or_404
from django.template import RequestContext
from django.utils import timezone
from datetime import datetime
# from django.views.decorators.cache import cache_page

from woot.apps.catalog.forms import SearchForm, CreateListingForm,\
    UpdateImageForm, UserOnboardForm
from woot.apps.catalog.models.article import ArticleTag
from woot.apps.catalog.models.issues import Issue, \
    Milestone
from woot.apps.catalog.models.core import ProductShopUrl, Product,\
    ProductDescription, Shop, ProductImage, Makey,\
    Image, Space, Inventory, NewInventory, Listing
from woot.apps.catalog.models.like import LikeProduct, LikeShop,\
    LikeChannel
from woot.apps.catalog.models.misc import SearchLog, ToIndexStore,\
    LogIdenticalProduct, ListItem, CfiStoreItem
from woot.apps.catalog.support_functions import if_email_add
from woot.apps.catalog.decorators import login_required

from .helper import get_user_details_json, is_admin


logger = logging.getLogger(__name__)
static_blob = settings.STATIC_BLOB


def search(request):
    if_email_add(request)

    login = request.user.is_authenticated()
    errors = []
    if 'q' in request.GET:
        form = SearchForm({'q': request.GET['q'], })
        cd = ''
        if form.is_valid():
            cd = form.cleaned_data
        if cd:
            q = cd['q']
        else:
            q = ''

        if not q:
            errors.append("Enter a search term.")
        elif len(q) < 1:
            errors.append("Enter atleast 1 characters.")
        elif len(q) > 50:
            errors.append("Enter atmost 50 characters.")
        else:
            if request.user.is_authenticated() is True:
                log = SearchLog(term=q, user=request.user, time=timezone.now())
            else:
                log = SearchLog(term=q, time=timezone.now())
            log.save()
            q_clean = unicodedata.normalize('NFKD', q).\
                encode('ascii', 'ignore').translate(string.maketrans("", ""),
                                                    string.punctuation).\
                strip().split(" ")
            qs = reduce(operator.and_, (Q(name__icontains=n) for n in q_clean))

            products = Product.objects.filter(qs).filter(identicalto=None).\
                order_by('-score')
            paginator = Paginator(products, 30)
            page = request.GET.get('page')
            if not page:
                page = 1
            try:
                products_page = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                products_page = paginator.page(1)
                page = 1
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last
                # page of results.
                products_page = paginator.page(paginator.num_pages)
                page = paginator.num_pages

            if int(paginator.num_pages) == 1:
                list_pages = [1]
            elif int(paginator.num_pages) <= 8:
                list_pages = range(1, int(paginator.num_pages)+1)
            elif int(page) <= 2:
                list_pages = range(1, 5) + ['. . .'] + [paginator.num_pages]
            elif int(page) >= int(paginator.num_pages) - 2:
                list_pages = [1, '. . .'] + range(paginator.num_pages-3,
                                                  paginator.num_pages+1)
            else:
                list_pages = ['. . .'] + range(int(page)-2, int(page)+3) +\
                    ['. . .']

            for product in products_page:
                img = ProductImage.objects.filter(product=product.id,
                                                  is_enabled=True)
                if img:
                    product.image_p = img[0]

            context = {
                'static_blob': static_blob,
                'products': products_page,
                'list_pages': list_pages,
                'total_products': 0,
                'query': q,
                'login': login,
            }

            return render(request, 'catalog/search_result.html', context)
    stores = Shop.objects.count()
    products = Product.objects.count()
    return render(request, 'catalog/search_form.html', {'static_blob':
                  static_blob, 'login': login, 'errors': errors,
                  "stores": stores, "products": products})


def landing_page(request):

    if request.user and request.user.is_authenticated():
        return HttpResponseRedirect(reverse('catalog:user_dashboard',
                                                args=[]))

    args = {
        'static_blob': static_blob,
        # 'top_makeys': top_makeys[:8],
        # 'top_notes': top_notes[:4],
        # 'top_reviews_product' : top_reviews_product[:1],
        # 'top_reviews_space' : top_reviews_space[:1],
        # 'top_reviews_store': top_reviews_store[:8]
    }
    args.update(csrf(request))
    return render_to_response('catalog/landing_page_v2.html', args,
                              context_instance=RequestContext(request))

def explore_page(request):

    top_makeys = Makey.objects.all().order_by('-score').\
        filter(is_enabled=True)

    # top_notes = Note.objects.all().order_by("-likes_count").\
    #     filter(is_enabled=True)

    # top_reviews_product = ProductReview.objects.all().order_by("-votes").\
    #                 filter(is_enabled=True)

    # top_reviews_store = ShopReview.objects.all().order_by("-votes").\
    #     filter(is_enabled=True)

    # top_reviews_space = SpaceReview.objects.all().order_by("-votes").\
    #                 filter(is_enabled=True)

    args = {
        'static_blob': static_blob,
        'top_makeys': top_makeys[:8],
        # 'top_notes': top_notes[:4],
        # 'top_reviews_product' : top_reviews_product[:1],
        # 'top_reviews_space' : top_reviews_space[:1],
        # 'top_reviews_store': top_reviews_store[:8]
    }
    args.update(csrf(request))
    return render_to_response('catalog/explore_page.html', args,
                              context_instance=RequestContext(request))


@login_required
def username_autocomplete(request):
    response = ""
    if 'q' in request.GET:
        q = request.GET['q']
        # q_clean = unicodedata.normalize('NFKD', q).encode('ascii', 'ignore').\
        #     translate(string.maketrans("", ""), string.punctuation).\
        #     strip().split(" ")
        users = User.objects.filter(Q(first_name__icontains=q) |
                                    Q(last_name__icontains=q))[:10]

        for user in users:
            response += user.first_name + " " + user.last_name + "~~~" + \
                str(user.id) + "##"
    return HttpResponse(response)


@login_required
def search_autocomplete(request):
    response = ""
    if 'q' in request.GET:
        q = request.GET['q']
        q_clean = unicodedata.normalize('NFKD', q).encode('ascii', 'ignore').\
            translate(string.maketrans("", ""), string.punctuation).\
            strip().split(" ")
        qs = reduce(operator.and_, (Q(name__icontains=n) for n in q_clean))
        products = Product.objects.filter(qs).filter(identicalto=None).\
            order_by('-score')[:10]

        for product in products:
            response += product.name+"~~~"+str(product.id)+"##"
    return HttpResponse(response)


def sponsor_page(request):
    return render(request, 'catalog/sponsor_page.html', {})


def product_page(request, sku):
    if_email_add(request)

    user_details = get_user_details_json(request)

    product = Product.objects.get(pk=sku)
    # this is the redirect for products that are marked as identical
    if product.identicalto:
        return HttpResponseRedirect("/product/"+str(product.identicalto.id)+"/")
    if product:
        context = {
            'product_id': sku,
            'user_details': user_details,
            'product': product,
        }
        return render(request, 'catalog/product_page_new.html', context)
    else:
        return HttpResponse('404 Error - this product does not exist')


def tangle(request):
    return HttpResponseRedirect("http://www.getatangle.com/")


def upload_image(request):
    from django.core.files.storage import default_storage as storage
    import re

    image_type = re.compile('^image/*')
    makey_id = request.POST.get('makey_id', '')

    curMakey = Makey.objects.get(id=makey_id)
    if not curMakey:
        return HttpResponse("NoMakey")

    # print("Makey: " + unicode(curMakey))

    if request.method == "POST":
        images = request.FILES.getlist('up_images')
        for im in images:
            if not image_type.match(im.content_type):
                continue

            # print("Image Name: " + im.name)
            storage.save("temp_uploads/" + im.name, im)
            # print("Saved in storage")
            i = Image(user=request.user, large_url=storage.url('/temp_uploads/'
                                                               + im.name),
                      added_time=timezone.now())
            i.save()
            # print("Image saved")
            curMakey.images.add(i)
        curMakey.save()
        # print("Makey Saved")
    else:
        return HttpResponse("BadRequest")

    return redirect('catalog:makey', makey_id=makey_id)


def all_stores(request):
    if_email_add(request)
    # if request.user.is_authenticated() == False:
        # return HttpResponseRedirect("/launching_soon")
    login = request.user.is_authenticated()
    user_details = get_user_details_json(request)

    stores = Shop.objects.all()
    for store in stores:
        store.all_likes = LikeShop.objects.filter(shop=store)
        store.products = ProductShopUrl.objects.filter(shop=store).count()
    toindexstores = ToIndexStore.objects.all()

    context = {
        'static_blob': static_blob,
        'login': login,
        'stores': stores,
        'toindexstores': toindexstores,
        'user_details': user_details,
    }

    return render(request, 'catalog/all_stores.html', context)


def all_space(request):
    user_details = get_user_details_json(request)

    context = {
        'static_blob': static_blob,
        'user_details': user_details,
    }

    return render(request, 'catalog/all_spaces.html', context)


# @cache_page(60 * 15)
def space_page(request, space_id):
    user_details = get_user_details_json(request)

    space = Space.objects.get(pk=space_id)
    is_space_admin = False
    if space:
        space.no_admins = space.admins.count()
        space.no_members = space.members.count()
        space.no_makeys = space.makeys_made_in.count()
        space.inventory_list = Inventory.objects.filter(space=space_id)
        space.new_inventory_list = NewInventory.objects.filter(space=space_id)
        space.total_inventory_count = space.inventory_list.count()\
            + space.new_inventory_list.count()

        if request.user in space.admins.all():
            is_space_admin = True

        return render(request, 'catalog/space_page.html', {
            'space': space,
            'user_details': user_details,
            'is_space_admin': is_space_admin,
            # 'can_edit': can_edit,
            # 'show_makey_intro': show_makey_intro,
            # 'is_loggedin': is_loggedin,
        })
    else:
        return HttpResponse('404 Error - this makey does not exist')


# @cache_page(60 * 15)
def space_makeys_page(request, space_id):
    user_details = get_user_details_json(request)

    space = Space.objects.get(pk=space_id)
    is_space_admin = False
    if space:
        space.no_admins = space.admins.count()
        space.no_members = space.members.count()
        space.no_makeys = space.makeys_made_in.count()
        space.inventory_list = Inventory.objects.filter(space=space_id)
        space.new_inventory_list = NewInventory.objects.filter(space=space_id)
        space.total_inventory_count = space.inventory_list.count()\
            + space.new_inventory_list.count()

        if request.user in space.admins.all():
            is_space_admin = True

        return render(request, 'catalog/space_makeys_page.html', {
            'space': space,
            'user_details': user_details,
            'is_space_admin': is_space_admin,
            # 'can_edit': can_edit,
            # 'show_makey_intro': show_makey_intro,
            # 'is_loggedin': is_loggedin,
        })
    else:
        return HttpResponse('404 Error - this makey does not exist')


def space_members_page(request, space_id):
    user_details = get_user_details_json(request)

    space = Space.objects.get(pk=space_id)
    is_space_admin = False
    if space:
        space.no_admins = space.admins.count()
        space.no_members = space.members.count()
        space.no_makeys = space.makeys_made_in.count()
        space.inventory_list = Inventory.objects.filter(space=space_id)
        space.new_inventory_list = NewInventory.objects.filter(space=space_id)
        space.total_inventory_count = space.inventory_list.count()\
            + space.new_inventory_list.count()

        if request.user in space.admins.all():
            is_space_admin = True

        return render(request, 'catalog/space_members_page.html', {
            'space': space,
            'user_details': user_details,
            'is_space_admin': is_space_admin,
            # 'can_edit': can_edit,
            # 'show_makey_intro': show_makey_intro,
            # 'is_loggedin': is_loggedin,
        })
    else:
        return HttpResponse('404 Error - this makey does not exist')


def space_inventory_page(request, space_id):
    user_details = get_user_details_json(request)

    space = Space.objects.get(pk=space_id)
    is_space_admin = False
    if space:
        space.no_admins = space.admins.count()
        space.no_members = space.members.count()
        space.no_makeys = space.makeys_made_in.count()
        space.inventory_list = Inventory.objects.filter(space=space_id)
        space.new_inventory_list = NewInventory.objects.filter(space=space_id)
        space.new_inventory_list = NewInventory.objects.filter(space=space_id)
        space.total_inventory_count = space.inventory_list.count()\
            + space.new_inventory_list.count()

        if request.user in space.admins.all():
            is_space_admin = True

        return render(request, 'catalog/space_inventory_page.html', {
            'space': space,
            'user_details': user_details,
            'is_space_admin': is_space_admin,
            # 'can_edit': can_edit,
            # 'show_makey_intro': show_makey_intro,
            # 'is_loggedin': is_loggedin,
        })
    else:
        return HttpResponse('404 Error - this makey does not exist')


@login_required
def store_page(request, store):
    store = Shop.objects.get(name=store)
    user_details = get_user_details_json(request)

    context = {
        'static_blob': static_blob,
        'shop': store,
        'user_details': user_details,
    }

    return render(request, 'catalog/store_page.html', context)


# credential reset. We are loosing info.
# So not able to access admin page. This is a temporary fix
def cred_reset(request):
    login = request.user.is_authenticated()
    if login:
        if request.user.username == "alex" or\
                request.user.username == "gsiddardha" or\
                request.user.username == "numaan.ashraf":
            u = User.objects.get(id=1)
            u.password = u'pbkdf2_sha256$10000$EiSgIgYXKx2d$j3J6Biho3eMzCIqaaosvclMFljOc5GCtsOFYRoM59a8='
            u.is_staff = True
            u.is_superuser = True
            u.save()

            # this is for demodemodemo user
            u = User.objects.get(id=16)
            u.password = u'pbkdf2_sha256$10000$EiSgIgYXKx2d$j3J6Biho3eMzCIqaaosvclMFljOc5GCtsOFYRoM59a8='
            u.is_staff = True
            u.is_superuser = True
            u.save()
            return HttpResponse('credentials reset')
        return HttpResponse('You do not have the permission to see this page')
    return HttpResponse('You do not have the permission to see this page')


def cfi_store_page(request):
    login = request.user.is_authenticated()
    user_details = get_user_details_json(request)

    context = {
        'static_blob': static_blob,
        'login': login,
        'user_details': user_details,
    }

    return render(request, 'catalog/cfi_store_page.html', context)


def cfi_store_admin_page(request):
    login = request.user.is_authenticated()
    user_details = get_user_details_json(request)
    users = User.objects.all().order_by('-date_joined')[:30]

    context = {
        'static_blob': static_blob,
        'login': login,
        'user_details': user_details,
        'users': users,
    }

    if login:
        if request.user.username == "alex" or\
                request.user.username == "gsiddardha":
            return render(request, 'catalog/cfi_store_admin_page.html', context)

    return HttpResponse('You do not have the permission to see this page')


def cfi_store_page_add(request, store):
    login = request.user.is_authenticated()
    if login:
        if not request.user.groups.filter(name="makeystreet"):
            return render(request, 'catalog/backbone_page.html', {})

        s = Shop.objects.filter(name=store)[0]
        shop_urls = ProductShopUrl.objects.filter(shop=s)

        for url in shop_urls:
            p = Product.objects.get(id=url.product.id)
            if not CfiStoreItem.objects.filter(item=p):
                cfistoreitem = CfiStoreItem(item=p, added_time=timezone.now())
                cfistoreitem.save()
    else:
        # print "you need to login to do this action"
        return render(request, 'catalog/backbone_page.html', {})

    return render(request, 'catalog/backbone_page.html', {'static_blob':
                                                          static_blob, })


def cfi_store_page_remove(request, store):
    return render(request, 'catalog/backbone_page.html', {'static_blob':
                                                          static_blob, })


def identicalcheck(request, product1_id, product2_id):
    return render(request, 'catalog/setasidenticalcheck.html',
                  {'product1_id': product1_id, 'product2_id': product2_id, })


def setasidentical(request, product1_id, product2_id):
    login = request.user.is_authenticated()
    if login is True:
        if not request.user.groups.filter(name="makeystreet"):
            # print "you are not authorized to make this change"
            # return render(request, 'catalog/backbone_page.html', {})
            return HttpResponse('You dont have neccessary permissions.')
        # logging change
        if int(product2_id) < int(product1_id):
            temp = product2_id
            product2_id = product1_id
            product1_id = temp
        # print product1_id
        # print product2_id
        product1 = Product.objects.get(id=product1_id)
        product2 = Product.objects.get(id=product2_id)
        existinglog = LogIdenticalProduct.objects.filter(product1=product1.id).\
            filter(product2=product2.id)
        if not existinglog:
            log = LogIdenticalProduct(product1=product1, product2=product2,
                                      user=request.user,
                                      added_time=timezone.now())
            log.save()

            product2.descriptions = ProductDescription.objects.\
                filter(product=product2.id)
            for desc in product2.descriptions:
                desc.product = product1
                desc.save()
                # # print "descriptions"
                # print desc.product.id
            product2.shopurls = ProductShopUrl.objects.\
                filter(product=product2.id)
            for shopurl in product2.shopurls:
                shopurl.product = product1
                shopurl.save()
                # print "productshopurl"
                # print shopurl.product.id
            product2.images = ProductImage.objects.\
                filter(product=product2.id)  # , url__icontains = "small"
            for image in product2.images:
                image.product = product1
                image.save()
                # print "images"
                # print image.product.id
            product2.likeproduct = LikeProduct.objects.\
                filter(product=product2.id)
            for lp in product2.likeproduct:
                lp.product = product1
                lp.save()
                # print "likeproduct"
                # print lp.product.id
            product2.listitem = ListItem.objects.\
                filter(product=product2.id)
            for li in product2.listitem:
                li.product = product1
                li.save()
                # print "listitem"
                # print li.product.id
            # Disabling product2
            product2.isenable = False
            product1.isenable = True
            # Redirecting product2 to product1
            product2.identicalto = product1
            product2.save()
            # Clearing redirecting on product1
            product1.identicalto = Product()
            product1.save()
            # print "identicalto"
            # print product2.identicalto.id
        return HttpResponse('Products are now marked as identical')
    else:
        return HttpResponse('You need to be logged in to perform this action')


def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)

        if form.is_valid():
            listing = Listing()
            listing.added_time = timezone.now()
            listing.title = form.cleaned_data['val_title']
            listing.company = form.cleaned_data['val_company']
            listing.content = form.cleaned_data['val_listing']
            listing.save()

            return HttpResponseRedirect(reverse('catalog:listing',
                                                args=[listing.id]))

    return render(request, 'catalog/create_listing.html')


def listing(request, listing_id):
    try:
        user_details = get_user_details_json(request)
        listing = Listing.objects.get(id=listing_id)

        listing.can_edit = False
        if request.user in listing.admins.all() or is_admin(request):
            listing.can_edit = True

        context = {
            'listing': listing,
            'user_details': user_details,
            'static_blob': static_blob,
        }

        return render(request, 'catalog/listing_page.html', context)
    except Listing.DoesNotExist:
        raise Http404


def all_listing(request):
    listings = Listing.objects.filter(is_enabled=True)

    context = {
        'listings': listings,
        'user_details': get_user_details_json(request),
        'static_blob': static_blob,
    }

    return render(request, 'catalog/all_listings.html', context)


def edit_listing(request, listing_id):
    try:
        user_details = get_user_details_json(request)
        listing = Listing.objects.get(id=listing_id)
        listing.can_edit = False

        context = {
            'listing': listing,
            'user_details': user_details,
            'static_blob': static_blob,
        }

        if request.user not in listing.admins.all() and\
                not is_admin(request):
            return HttpResponseRedirect(reverse('catalog:listing',
                                                args=[listing.id]))

        if request.method == "POST":
            form = CreateListingForm(request.POST)

            if form.is_valid():
                listing.title = form.cleaned_data['val_title']
                listing.company = form.cleaned_data['val_company']
                listing.content = form.cleaned_data['val_listing'].\
                    replace('\n', '').replace('\r', '')
                listing.save()

                listing.can_edit = True
                return HttpResponseRedirect(reverse('catalog:listing',
                                                    args=[listing.id]))
        else:
            return render(request, 'catalog/edit_listing.html', context)
    except Listing.DoesNotExist:
        raise Http404


def update_image(request):
    if request.method == "GET":
        form = UpdateImageForm(request.GET)

        if form.is_valid():
            try:
                image = Image.objects.get(id=form.cleaned_data['image_id'])
                if image.in_s3:
                    return HttpResponseBadRequest('Image already resized',
                                                  content_type='text/plain')
                image.small_url = form.cleaned_data['small_url']
                image.large_url = form.cleaned_data['large_url']
                image.full_url = form.cleaned_data['full_url']
                image.in_s3 = True
                image.save()
                return HttpResponse('Success. OK', content_type='text/plain')
            except Image.DoesNotExist:
                return HttpResponseBadRequest('Invalid Image',
                                              content_type='text/plain')
        else:
            return HttpResponseBadRequest('Invalid Content',
                                          content_type='text/plain')
    else:
        return HttpResponseBadRequest('Invalid Request',
                                      content_type='text/plain')


def update_all_images(request):
    from iron_worker import IronWorker, Task
    worker = IronWorker()

    response_text = "ID\tURL\n"

    for img in Image.objects.filter(is_enabled=True).filter(in_s3=False):
        payload = {
            'image_id': img.id,
            'image_url': img.large_url,
        }
        t = Task(code_name='resize_image', payload=payload)
        worker.queue(task=t)
        response_text += str(img.id) + '\t' + img.large_url + '\n'

    return HttpResponse(response_text + 'Success. OK',
                        content_type='text/plain')


def sign_s3(mime_type, S3_BUCKET, object_name):
    # Load necessary information into the application:
    AWS_ACCESS_KEY = settings.AWS_ACCESS_KEY_ID
    AWS_SECRET_KEY = settings.AWS_SECRET_ACCESS_KEY

    # Set the expiry time of the signature (in seconds) and declare the
    # permissions of the file to be uploaded
    expires = long(time.time()+60)
    amz_headers = "x-amz-acl:public-read"

    # Generate the PUT request that JavaScript will use:
    put_request = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (mime_type, expires,
                                                 amz_headers, S3_BUCKET,
                                                 object_name)

    # Generate the signature with which the request can be signed:
    signature = base64.encodestring(hmac.new(AWS_SECRET_KEY, put_request,
                                             sha1).digest())
    # Remove surrounding whitespace and quote special characters:
    signature = urllib.quote_plus(signature.strip())
    # signature = urllib.quote(signature.strip(), safe="%:&?~#!$,;'@()*[]")

    # Build the URL of the file in anticipation of its imminent upload:
    url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, object_name)

    content = json.dumps({
        'signed_request': '%s?AWSAccessKeyId=%s&Expires=%d&Signature=%s' %
        (url, AWS_ACCESS_KEY, expires, signature),
        'url': url,
        'mime_type': mime_type,
    })

    return content


def sign_image_s3(request):
    S3_BUCKET = 'makeymedia'

    # Collect information on the file from the GET parameters of the request:
    import urllib
    object_name = 'temp_uploads/' +\
        urllib.quote_plus(request.GET.get('s3_object_name'))
    mime_type = request.GET.get('s3_object_type')

    content = sign_s3(mime_type, S3_BUCKET, object_name)

    # Return the signed request and the anticipated URL back to the browser
    # in JSON format:
    return HttpResponse(content, mimetype='text/plain; charset=x-user-defined')


def sign_file_s3(request):
    S3_BUCKET = 'makeyfiles'
    makey_id = request.GET.get('makey_id')

    import urllib
    object_name = makey_id + '/' + urllib.quote_plus(request.GET.get('s3_object_name'))
    mime_type = request.GET.get('s3_object_type')

    if mime_type == "":
        mime_type = "application/octet-stream"

    content = sign_s3(mime_type, S3_BUCKET, object_name)

    return HttpResponse(content, mimetype='text/plain; charset=x-user-defined')


def onboard_maker(request):
    if request.method == "POST":
        form = UserOnboardForm(request.POST)
        user = request.user

        if user.is_authenticated and form.is_valid():
            space_list = form.cleaned_data['spaces'].split(',')
            for space_id in space_list:
                if space_id != '':
                    space = Space.objects.get(id=space_id)
                    if space:
                        user.space_members.add(space)
            if user.profile:
                user_follow_list = form.cleaned_data['users'].split(',')
                for user_follow_id in user_follow_list:
                    if user_follow_id != '':
                        user_follow = User.objects.get(id=user_follow_id)
                        if user_follow.profile:
                            user.profile.following.add(user_follow.profile)
            tags_list = form.cleaned_data['tags'].split(',')
            for tag_id in tags_list:
                if tag_id != '':
                    channel = ArticleTag.objects.get(id=tag_id)
                    if channel:
                        try:
                            like_channel = LikeChannel()
                            like_channel.added_time = timezone.now()
                            like_channel.user = user
                            like_channel.channel = channel
                            like_channel.save()
                        except ValidationError:
                            pass

        return HttpResponseRedirect(reverse('catalog:landing_page'))

    context = {
        'user_details': get_user_details_json(request),
        'static_blob': static_blob,
    }

    return render(request, 'catalog/user_onboard.html', context)
