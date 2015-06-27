from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden
from django.shortcuts import render
from django.utils import timezone

from woot.apps.catalog.forms import CreateMakerForm, ReplaceMakerForm
from woot.apps.catalog.models.core import Note, Makey,\
    UserProfile, Image, Article, Space, Comment
from woot.apps.catalog.models.interactions import UserNotification, Interaction
from woot.apps.catalog.models.forum import Question, Answer
from .helper import get_user_details_json, is_admin, get_makey_activities

static_blob = settings.STATIC_BLOB


def get_maker_details(username):
    maker = User.objects.get(username=username)
    maker.no_makeys = maker.collaborators.filter(is_enabled=True).count()
    maker.no_following = maker.profile.following.count()
    maker.no_followers = maker.profile.followers.count()
    maker.no_insights = Note.objects.filter(user=maker, is_enabled=True).count()
    maker.no_reviews = maker.shopreview_set.count() + \
        maker.productreview_set.count() + maker.spacereview_set.count()

    return maker


# @cache_per_user(ttl=60 * 5)
def maker_makeys_page(request, username):
    maker = get_maker_details(username)

    # makeys = maker.makey_set.filter(is_enabled=True).all()
    makeys = Makey.objects.filter(collaborators__in=[maker]).\
        filter(is_enabled=True)

    if not request.user.username == username:
        makeys = makeys.filter(is_private=False)

    context = {
        'static_blob': static_blob,
        'maker': maker,
        'user_details': get_user_details_json(request),
        'tab': 'tab_makeys',
        'makeys': makeys,
        'is_admin': is_admin(request)
    }
    return render(request, 'catalog/maker_page.html', context)


def maker_settings(request):
    if not request.user.is_authenticated():
        return HttpResponseForbidden
    return render(request, 'catalog/account_settings.html')


def maker_profile_page(request, username):
    maker = get_maker_details(username)

    can_edit = False
    if request.user.is_authenticated():
        # is_loggedin = True
        if request.user == maker or is_admin(request):
            can_edit = True
    context = {
        'static_blob': static_blob,
        'maker': maker,
        'can_edit': can_edit,
        'user_details': get_user_details_json(request),
        'is_admin': is_admin(request)
    }
    return render(request, 'catalog/maker_profile_page.html', context)


def maker_insights_page(request, username):
    maker = get_maker_details(username)

    context = {
        'static_blob': static_blob,
        'maker': maker,
        'user_details': get_user_details_json(request),
        'tab': 'tab_following',
        'is_admin': is_admin(request)
    }
    return render(request, 'catalog/maker_insights_page.html', context)


def maker_following_page(request, username):
    maker = get_maker_details(username)

    context = {
        'static_blob': static_blob,
        'maker': maker,
        'user_details': get_user_details_json(request),
        'tab': 'tab_following',
        'is_admin': is_admin(request)
    }
    return render(request, 'catalog/maker_page.html', context)


def maker_followers_page(request, username):
    maker = get_maker_details(username)

    context = {
        'static_blob': static_blob,
        'maker': maker,
        'user_details': get_user_details_json(request),
        'tab': 'tab_followers',
        'is_admin': is_admin(request)
    }
    return render(request, 'catalog/maker_page.html', context)


def maker_reviews_page(request, username):
    maker = get_maker_details(username)

    context = {
        'static_blob': static_blob,
        'maker': maker,
        'user_details': get_user_details_json(request),
        'tab': 'tab_makeys',
        'is_admin': is_admin(request)
    }
    return render(request, 'catalog/maker_reviews_page.html', context)


def maker_create(request):
    if not is_admin(request):
        raise Http404

    if request.method == "POST":
        form = CreateMakerForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            if User.objects.filter(username=username):
                return render(request, 'catalog/maker_create.html', {
                    'static_blob': static_blob,
                    'existing_username': True
                })

            user = User()
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

            user_profile = UserProfile()
            user_profile.added_time = timezone.now()
            user_profile.user = user
            user_profile.save()

            if form.cleaned_data['image_url']:
                image = Image()
                image.user = user
                image.large_url = form.cleaned_data['image_url']
                image.added_time = timezone.now()
                image.save()
                user_profile.profile_pic = image
                user_profile.save()

            return HttpResponseRedirect(reverse('catalog:maker_profile',
                                                args=[user.username]))

    context = {
        'static_blob': static_blob
    }

    return render(request, 'catalog/maker_create.html', context)


def maker_replace(request):
    if not is_admin(request):
        raise Http404

    if request.method == "POST":
        form = ReplaceMakerForm(request.POST)

        if form.is_valid():
            source_user_id = form.cleaned_data['user_source']
            target_user_id = form.cleaned_data['user_target']

            source_user = User.objects.get(id=source_user_id)
            target_user = User.objects.get(id=target_user_id)

            #Copy User data
            target_user.email = source_user.email
            target_user.first_name = source_user.first_name
            target_user.last_name = source_user.last_name

            #Copy Profile
            source_profile = UserProfile.objects.get(user=source_user)
            target_profile = UserProfile.objects.get(user=target_user)

            target_profile.instructables_url = source_profile.instructables_url
            target_profile.github_url = source_profile.github_url
            target_profile.linkedin_url = source_profile.linkedin_url
            target_profile.facebook_url = source_profile.facebook_url
            target_profile.twitter_url = source_profile.twitter_url
            target_profile.yt_channel_url = source_profile.yt_channel_url
            target_profile.stackoverflow_url = source_profile.stackoverflow_url
            target_profile.blog_url = source_profile.blog_url
            target_profile.website_url = source_profile.website_url
            target_profile.aboutme = source_profile.aboutme
            target_profile.membership = source_profile.membership
            target_profile.college = source_profile.college
            target_profile.patent = source_profile.patent
            target_profile.location = source_profile.location
            target_profile.profile_pic = source_profile.profile_pic
            target_profile.save()

            #Migrate Makeys
            source_makeys = Makey.objects.filter(user=source_user)
            for makey in source_makeys:
                makey.user = target_user
                makey.save()
                makey.collaborators.remove(source_user)
                makey.collaborators.add(target_user)

            #Migrate Article
            source_articles = Article.objects.filter(user=source_user)
            for article in source_articles:
                article.user = target_user
                article.save()

            #Migrate Space Memberships
            source_spaces = Space.objects.filter(members=source_user)
            for space in source_spaces:
                space.members.remove(source_user)
                space.members.add(target_user)

            source_user.is_active = False
            source_user.save()

            return HttpResponseRedirect(reverse('catalog:maker_profile',
                                                args=[target_user.username]))

    context = {
        'static_blob': static_blob
    }

    return render(request, 'catalog/maker_replace.html', context)


def user_dashboard(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('catalog:landing_page'))

    makeys = Makey.objects.filter(is_enabled=True, collaborators__in=[request.user]).order_by('-added_time')

    activities = []

    for makey in makeys:
        activities += get_makey_activities(makey)

    activities = [x for x in activities if x.user != request.user]

    #sorting according to date of interaction
    activities = sorted(activities, key=lambda x: x.added_time,
                        reverse=True)

    makeys = [x for x in makeys if x.used_in.count() == 0]
    makeys = sorted(makeys, key=lambda x: x.added_time,
                        reverse=True)

    context = {
        'user': request.user,
        'activities': activities[:15],
        'makeys': makeys
    }

    return render(request, 'catalog/user_dashboard_v2.html', context)

def read_notification(request, notif_id):
    if not request.user or not request.user.is_authenticated():
        raise Http404

    try:
        notif = UserNotification.objects.get(id=notif_id)
        if notif.user != request.user:
            raise Http404

        try:
            if notif.interaction.event == Interaction.activity_insight_created:
                insight = Note.objects.get(id=notif.interaction.event_id)
                notif.read = True
                notif.save()
                return HttpResponseRedirect(reverse('catalog:makey_new_insight_slug',
                        args=[notif.interaction.makey.user.username,notif.interaction.makey.slug,insight.id]))

            if notif.interaction.event == Interaction.activity_question_created:
                question = Question.objects.get(id=notif.interaction.event_id)
                notif.read = True
                notif.save()
                return HttpResponseRedirect(reverse('catalog:makey_new_discussion_slug',
                        args=[question.makey.user.username, question.makey.slug, question.id]))

            if notif.interaction.event == Interaction.activity_answer_created:
                answer = Answer.objects.get(id=notif.interaction.event_id)
                notif.read = True
                notif.save()
                return HttpResponseRedirect(reverse('catalog:makey_new_discussion_slug',
                        args=[answer.question.makey.user.username, answer.question.makey.slug, answer.question.id]))

            if notif.interaction.event == Interaction.activity_insight_comment_created:
                comment = Comment.objects.get(id=notif.interaction.event_id)
                notif.read = True
                notif.save()
                insight = comment.note_set.all()[0]
                return HttpResponseRedirect(reverse('catalog:makey_new_insight_slug',
                        args=[notif.interaction.makey.user.username,notif.interaction.makey.slug,insight.id]))

            if notif.interaction.event == Interaction.activity_question_comment_created:
                comment = Comment.objects.get(id=notif.interaction.event_id)
                notif.read = True
                notif.save()
                question = comment.question
                return HttpResponseRedirect(reverse('catalog:makey_new_discussion_slug',
                        args=[question.makey.user.username, question.makey.slug, question.id]))

            if notif.interaction.event == Interaction.activity_answer_comment_created:
                comment = Comment.objects.get(id=notif.interaction.event_id)
                notif.read = True
                notif.save()
                answer = comment.answer
                return HttpResponseRedirect(reverse('catalog:makey_new_discussion_slug',
                        args=[answer.question.makey.user.username, answer.question.makey.slug, answer.question.id]))

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        except Note.DoesNotExist:
            notif.delete()
            raise Http404

        except Question.DoesNotExist:
            notif.delete()
            raise Http404

        except Answer.DoesNotExist:
            notif.delete()
            raise Http404

        except Comment.DoesNotExist:
            notif.delete()
            raise Http404

    except UserNotification.DoesNotExist:
        raise Http404


