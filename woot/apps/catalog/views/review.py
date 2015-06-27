from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.utils import timezone

from woot.apps.catalog.forms import CreateProductReviewForm,\
    CreateShopReviewForm, CreateSpaceReviewForm
from woot.apps.catalog.models.core import Product, Shop, Space, NewProduct
from woot.apps.catalog.models.review import ProductReview, ShopReview,\
    SpaceReview

from .helper import get_user_details_json
static_blob = settings.STATIC_BLOB


def all_reviews(request):
    product_reviews = ProductReview.objects.all()
    shop_reviews = ShopReview.objects.all()
    space_reviews = SpaceReview.objects.all()

    context = {
        'static_blob': static_blob,
        'user_details': get_user_details_json(request),
        'product_reviews': product_reviews,
        'shop_reviews': shop_reviews,
        'space_reviews': space_reviews,
    }

    return render(request, 'catalog/all_reviews.html', context)


def store_review(request, review_id):
    try:
        user_details = get_user_details_json(request)
        review = ShopReview.objects.get(id=review_id)
        review.upvotes = review.voteshopreview_set.filter(vote=True)

        context = {
            'static_blob': static_blob,
            'user_details': user_details,
            'review': review,
        }

        return render(request, 'catalog/store_review.html', context)
    except ShopReview.DoesNotExist:
        raise Http404


def product_review(request, review_id):
    try:
        user_details = get_user_details_json(request)
        review = ProductReview.objects.get(id=review_id)
        review.upvotes = review.voteproductreview_set.filter(vote=True)

        context = {
            'static_blob': static_blob,
            'user_details': user_details,
            'review': review,
        }

        return render(request, 'catalog/product_review.html', context)
    except ProductReview.DoesNotExist:
        raise Http404


def space_review(request, review_id):
    try:
        user_details = get_user_details_json(request)
        review = SpaceReview.objects.get(id=review_id)
        review.upvotes = review.votespacereview_set.filter(vote=True)

        context = {
            'static_blob': static_blob,
            'user_details': user_details,
            'review': review,
        }

        return render(request, 'catalog/space_review.html', context)
    except SpaceReview.DoesNotExist:
        raise Http404


def create_review(request):
    if request.method == "POST":
        if request.POST.get('val_type', '') == 'PART':
            form = CreateProductReviewForm(request.POST)

            if form.is_valid():
                r = ProductReview()
                r.title = form.cleaned_data['val_title']
                r.review = form.cleaned_data['val_review']
                r.user = request.user
                r.rating = form.cleaned_data['val_rating']
                r.added_time = timezone.now()

                product_data_split = form.cleaned_data['val_part'].split('_')
                product_type = product_data_split[0]
                product_id = int(product_data_split[1])

                if product_type == 'old':
                    product = Product.objects.get(id=product_id)
                    r.product = product
                elif product_type == 'new':
                    product = NewProduct.objects.get(id=product_id)
                    r.product = product

                r.save()

                return HttpResponseRedirect(reverse('catalog:all_reviews'))
            else:
                print(form.errors)
        elif request.POST.get('val_type', '') == 'SHOP':
            form = CreateShopReviewForm(request.POST)

            if form.is_valid():
                r = ShopReview()
                r.title = form.cleaned_data['val_title']
                r.review = form.cleaned_data['val_review']
                r.user = request.user
                r.rating = form.cleaned_data['val_rating']
                r.added_time = timezone.now()

                shop_data_split = form.cleaned_data['val_shop'].split('_')
                shop_type = shop_data_split[0]
                shop_id = int(shop_data_split[1])

                if shop_type == 'old':
                    shop = Shop.objects.get(id=shop_id)
                    r.shop = shop
                elif shop_type == 'new':
                    shop = NewProduct.objects.get(id=shop_id)
                    r.shop = shop

                r.save()

                return HttpResponseRedirect(reverse('catalog:all_reviews'))
            else:
                print(form.errors)
        elif request.POST.get('val_type', '') == 'SPACE':
            form = CreateSpaceReviewForm(request.POST)

            if form.is_valid():
                r = SpaceReview()
                r.title = form.cleaned_data['val_title']
                r.review = form.cleaned_data['val_review']
                r.user = request.user
                r.rating = form.cleaned_data['val_rating']
                r.added_time = timezone.now()

                space_data_split = form.cleaned_data['val_space'].split('_')
                space_type = space_data_split[0]
                space_id = int(space_data_split[1])

                if space_type == 'old':
                    space = Space.objects.get(id=space_id)
                    r.space = space
                elif space_type == 'new':
                    space = NewProduct.objects.get(id=space_id)
                    r.space = space

                r.save()

                return HttpResponseRedirect(reverse('catalog:all_reviews'))
            else:
                print(form.errors)
        else:
            pass

    context = {
        'static_blob': static_blob,
        'user_details': get_user_details_json(request),
    }

    return render(request, 'catalog/create_product_review.html', context)
