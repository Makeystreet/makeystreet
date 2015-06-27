from difflib import SequenceMatcher

from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from woot.apps.catalog.forms import CreateArticleForm, EditArticleForm
from woot.apps.catalog.models.article import ArticleTag, ArticleEmail
from woot.apps.catalog.models.core import Article
# from woot.apps.catalog.models.like import LikeChannel

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404

from django.utils import timezone

# from woot.apps.catalog.decorators import cache_per_user
from woot.apps.catalog.forms import ArticleEmailForm
from .helper import get_user_details_json, is_admin
from django.conf import settings

static_blob = settings.STATIC_BLOB


def get_fav_channel(request):
    fav_channel = []

    login = request.user.is_authenticated()
    if login:
        cur_user = User.objects.get(username=request.user.username)
        if cur_user:
            fav_channel = ArticleTag.objects.annotate(
                num_articles=Count('article')).\
                filter(likechannel__user=cur_user).\
                order_by('-num_articles')

    return fav_channel


def get_popular_users():
    users = User.objects.annotate(article_count=Count('article')).\
        order_by('-article_count')

    popular_users = []
    for user in users:
        if user.article_count > 0:
            popular_users.append(user)

    return popular_users


def merge_sequences(seq1, seq2):
    sm = SequenceMatcher(a=seq1, b=seq2)
    res = []
    for (op, start1, end1, start2, end2) in sm.get_opcodes():
        if op == 'equal' or op == 'delete':
            #This range appears in both sequences, or only in the first one.
            res += seq1[start1:end1]
        elif op == 'insert':
            #This range appears in only the second sequence.
            res += seq2[start2:end2]
        elif op == 'replace':
            #There are different ranges in each sequence - add both.
            res += seq1[start1:end1]
            res += seq2[start2:end2]
    return res


def article_page(request, article_id):
    user_details = get_user_details_json(request)

    article = Article.objects.get(pk=article_id)
    article_count = Article.objects.count()
    if article:
        tags = ArticleTag.objects.annotate(num_articles=Count('article')).\
            order_by('-num_articles')

        fav_channel = get_fav_channel(request)

        tags = merge_sequences(list(tags)[:10], list(fav_channel))

        popular_users = get_popular_users()

        editable = False
        if request.user == article.user or is_admin(request):
            editable = True

        return render(request, 'catalog/article_page.html', {
            'article': article,
            'article_count': article_count,
            'user_details': user_details,
            'article_id': article_id,
            'all_tags': tags,
            'popular_users': popular_users[:10],
            'fav_channel': fav_channel,
            'editable': editable
        })
    else:
        return HttpResponse('404 Error - this page does not exist')


def all_tags(request):
    user_details = get_user_details_json(request)
    context = {
        'user_details': user_details,
    }

    username = request.GET.get('user')
    if username:
        try:
            user = User.objects.get(username=username)
            articles = Article.objects.filter(user=user).\
                annotate(num_likes=Count('likearticle')).\
                order_by('-num_likes')
            context['filter_user'] = user
        except User.DoesNotExist:
            articles = Article.objects.\
                annotate(num_likes=Count('likearticle')).\
                order_by('-num_likes')
    else:
        articles = Article.objects.annotate(num_likes=Count('likearticle')).\
            order_by('-num_likes')

    q_sort = request.GET.get('sort')
    if q_sort and q_sort.lower() == 'latest':
            articles = articles.order_by('-added_time')

    article_count = Article.objects.count()
    tags = ArticleTag.objects.annotate(num_articles=Count('article')).\
        order_by('-num_articles')

    fav_channel = get_fav_channel(request)
    tags = merge_sequences(list(tags)[:10], list(fav_channel))

    popular_users = get_popular_users()

    context['articles'] = articles
    context['article_count'] = article_count
    context['all_tags'] = tags
    context['current_tag'] = 'all'
    context['popular_users'] = popular_users[:10]
    context['fav_channel'] = fav_channel

    return render(request, 'catalog/article_tag_page.html', context)


# @cache_per_user(ttl=60 * 5)
def tag_page(request, tag_id):
    user_details = get_user_details_json(request)

    tag = ArticleTag.objects.get(url_snippet=tag_id)
    if tag:
        articles = Article.objects.filter(tags=tag).\
            annotate(num_likes=Count('likearticle')).\
            order_by('-num_likes')

        q_sort = request.GET.get('sort')

        if q_sort and q_sort.lower() == 'latest':
            articles = Article.objects.filter(tags=tag).order_by('-added_time')
        article_count = Article.objects.count()
        tags = ArticleTag.objects.annotate(num_articles=Count('article')).\
            order_by('-num_articles')
        fav_channel = get_fav_channel(request)
        tags = merge_sequences(list(tags)[:10], list(fav_channel))

        email_submitted = request.session.get('email_' + tag_id, False)

        popular_users = get_popular_users()

        return render(request, 'catalog/article_tag_page.html', {
            'articles': articles,
            'article_count': article_count,
            'user_details': user_details,
            'all_tags': tags,
            'current_tag': tag,
            'popular_users': popular_users[:10],
            'fav_channel': fav_channel,
            'email_submitted': email_submitted
        })
    else:
        return HttpResponse('404 Error - this page does not exist')


def user_page(request, username):
    user_details = get_user_details_json(request)

    user_filter = User.objects.get(username=username)
    if user_filter:
        articles = Article.objects.filter(user=user_filter).\
            annotate(num_likes=Count('likearticle')).\
            order_by('-num_likes')

        q_sort = request.GET.get('sort')

        if q_sort and q_sort.lower() == 'latest':
            articles = Article.objects.filter(user=user_filter).\
                order_by('-added_time')
        article_count = Article.objects.count()

        popular_users = get_popular_users()

        tags = ArticleTag.objects.annotate(num_articles=Count('article')).\
            order_by('-num_articles')
        fav_channel = get_fav_channel(request)
        tags = merge_sequences(list(tags)[:10], list(fav_channel))

        # email_submitted = request.session.get('email_' + tag_id, False)

        return render(request, 'catalog/article_user_page.html', {
            'articles': articles,
            'article_count': article_count,
            'user_details': user_details,
            'all_tags': tags,
            'popular_users': popular_users[:10],
            'current_user': user_filter,
            'fav_channel': fav_channel,
            # 'email_submitted': email_submitted
        })
    else:
        return HttpResponse('404 Error - this page does not exist')


def create_article(request):
    if request.method == "POST":
            form = CreateArticleForm(request.POST)
            user = request.user

            if form.is_valid():
                article = Article()
                article.added_time = timezone.now()
                article.title = form.cleaned_data['title']
                article.url = form.cleaned_data['url']
                article.description = form.cleaned_data['desc']
                article.image_url = form.cleaned_data['image_url']
                article.recommendation = form.cleaned_data['reco']
                article.rating = 5

                user_id = form.cleaned_data['user']
                if user_id:
                    user = User.objects.get(id=user_id)
                    if user:
                        article.user = user

                article.save()
                tags_list = form.cleaned_data['tags'].split(',')
                for tag_id in tags_list:
                    if tag_id != '':
                        tag = ArticleTag.objects.get(id=tag_id)
                        if tag:
                            article.tags.add(tag)

                return HttpResponseRedirect(reverse('catalog:article_page',
                                                    args=[article.id]))

    user_details = get_user_details_json(request)

    admin_user = False
    if is_admin(request):
        admin_user = True

    context = {
        'user_details': user_details,
        'is_admin_user': admin_user
    }
    return render(request, 'catalog/article_create_page_2.html', context)


def edit_article(request, article_id):

    article = Article.objects.get(id=article_id)
    if not article:
        raise Http404

    if request.user == article.user or is_admin(request):
        return HttpResponseRedirect(reverse('catalog:article_page',
                                    args=[article.id]))

    if request.method == "POST":
        form = EditArticleForm(request.POST)

        if form.is_valid():
            article.title = form.cleaned_data['title']
            article.description = form.cleaned_data['description']
            article.image_url = form.cleaned_data['image_url']
            article.recommendation = form.cleaned_data['recommendation']

            article.save()
            article.tags.clear()
            tags_list = form.cleaned_data['tags'].split(',')
            for tag_id in tags_list:
                if tag_id != '':
                    tag = ArticleTag.objects.get(id=tag_id)
                    if tag:
                        article.tags.add(tag)

            return HttpResponseRedirect(reverse('catalog:article_page',
                                                args=[article.id]))

    admin_user = False
    if is_admin(request):
        admin_user = True

    current_tags = {
        'tags': []
    }

    for tag in article.tags.all():
        tag = {
            'name': str(tag.name),
            'id': tag.id
        }
        current_tags['tags'].append(tag)

    context = {
        'is_admin_user': admin_user,
        'article': article,
        'current_tags': current_tags
    }
    return render(request, 'catalog/edit_article.html', context)


def article_email(request):
    if request.method == "POST":
        form = ArticleEmailForm(request.POST)

        if form.is_valid():
            subscription = ArticleEmail()
            subscription.added_time = timezone.now()
            subscription.email = form.cleaned_data['email_id']
            subscription.temp_id = form.cleaned_data['temp_id']

            tag_id = form.cleaned_data['tag_id']
            subscription.tag = ArticleTag.objects.get(url_snippet=tag_id)
            subscription.save()

            request.session['email_' + request.POST.get('tag_id')] = True
        return redirect('catalog:tag_page', tag_id=request.POST.get('tag_id'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def subscribe_page(request):
    if request.method == "POST":
        form = ArticleEmailForm(request.POST)

        if form.is_valid():
            if form.cleaned_data['step'] not in ["start", "complete"]:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if form.cleaned_data['step'] == "start":
                return render(request, 'catalog/reco_subscribe.html', {
                    'user_details': get_user_details_json(request),
                    'static_blob': static_blob,
                    'step': 'start',
                    'email_id': form.cleaned_data['email_id'],
                    'temp_id': form.cleaned_data['temp_id'],
                    'redirect': request.META.get('HTTP_REFERER')
                })

            if form.cleaned_data['step'] == "complete":
                tags_list = form.cleaned_data['tags'].split(',')
                for tag_id in tags_list:
                    if tag_id != '':
                        channel = ArticleTag.objects.get(id=tag_id)
                        if channel:
                            try:
                                subscription = ArticleEmail()
                                subscription.added_time = timezone.now()
                                subscription.email = form.cleaned_data['email_id']
                                subscription.temp_id = form.cleaned_data['temp_id']
                                subscription.tag = ArticleTag.objects.get(id=channel.id)
                                subscription.save()
                                request.session['email_' + channel.id] = True
                            except:
                                pass

                user_follow_list = form.cleaned_data['users'].split(',')
                for user_follow_id in user_follow_list:
                    if user_follow_id != '':
                        user_follow = User.objects.get(id=user_follow_id)
                        if user_follow:
                            try:
                                subscription = ArticleEmail()
                                subscription.added_time = timezone.now()
                                subscription.email = form.cleaned_data['email_id']
                                subscription.temp_id = form.cleaned_data['temp_id']
                                subscription.user = User.objects.get(id=user_follow.id)
                                subscription.save()
                                request.session['email_' + user_follow.username] = True
                            except:
                                pass

                if form.cleaned_data['redirect']:
                    messages.info(request, 'Subscribed to recommendations')
                    return HttpResponseRedirect(form.cleaned_data['redirect'])
                else:
                    messages.info(request, 'Subscribed to recommendations')
                    return redirect('catalog:all_articles')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def landing_page(request):
    staff_picks = Article.objects.filter(is_staff_pick=True)\
        .order_by('-added_time_staff_pick')[:4]

    context = {
        'staff_picks': staff_picks,
        'user_details': get_user_details_json(request)
    }

    return render(request, 'catalog/reco_landing_page.html', context)


def staff_pick(request):
    recommendations = Article.objects.filter(is_staff_pick=True)\
        .order_by('-added_time_staff_pick')[:100]
    context = {
        'recommendations': recommendations,
        'user_details': get_user_details_json(request),
    }

    return render(request, 'catalog/staffpick_reco.html', context)


def staff_pick_add(request, article_id):
    recommendation = Article.objects.get(pk=article_id)
    recommendation.is_staff_pick = True
    recommendation.added_time_staff_pick = timezone.now()
    recommendation.save()

    response_text = 'Recommendation id = ' + str(recommendation.id) +\
        ' has been added as a staff pick'
    return HttpResponse(response_text)


def staff_pick_remove(request, article_id):
    recommendation = Article.objects.get(pk=article_id)
    recommendation.is_staff_pick = False
    recommendation.added_time_staff_pick = timezone.now()
    recommendation.save()

    response_text = 'Recommendation id = ' + str(recommendation.id) +\
        ' has been removed from staff pick'
    return HttpResponse(response_text)
