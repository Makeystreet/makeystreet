from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, Http404,\
    HttpResponsePermanentRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

import os
import unirest

from woot.apps.catalog.decorators import cache_per_user
from woot.apps.catalog.forms import *
from woot.apps.catalog.models.core import *
from woot.apps.catalog.models.issues import Issue, Milestone
from woot.apps.catalog.models.like import LikeNote, LikeMakey
from woot.apps.catalog.models.forum import Question, Answer

from .helper import get_user_details_json, is_admin, \
                get_makey_activities, get_makey_insights,\
                check_private_access, get_user_notifications
from woot.apps.catalog.models.interactions import Interaction, UserInteraction

static_blob = settings.STATIC_BLOB


def create_makey(request):
    if request.method == "POST" and request.user.is_authenticated():
        form = CreateMakeyForm(request.POST)

        if form.is_valid():
            m = Makey()
            m.user = request.user
            m.name = form.cleaned_data['val_name']
            m.about = form.cleaned_data['val_about']
            # m.status = form.cleaned_data['status_chosen']
            # if form.cleaned_data['val_privacy'] == 'private':
            #     m.is_private = True
            # else:
            #     m.is_private = False
            m.added_time = timezone.now()
            m.save()
            m.collaborators.add(request.user)

            return HttpResponseRedirect(reverse('catalog:makey', args=[m.id]))

    if request.method == "POST" and not request.user.is_authenticated():
        messages.error(request, 'Please login and try again!')

    if not request.user or not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('account_signup', args=[]))

    context = {
        'static_blob': static_blob,
    }

    return render(request, 'catalog/create_makey.html', context)


def curate_makey(request):
    makeys = Makey.objects.filter(is_enabled=True).order_by('-added_time')[:100]
    context = {
        'makeys': makeys,
        'user_details': get_user_details_json(request),
        # 'is_admin_user': is_admin_user
    }

    return render(request, 'catalog/curate_makey.html', context)


def staff_pick(request):
    makeys = Makey.objects.filter(is_staff_pick=True).\
        order_by('-added_time_staff_pick')[:100]
    context = {
        'makeys': makeys,
        'user_details': get_user_details_json(request),
        # 'is_admin_user': is_admin_user
    }

    return render(request, 'catalog/staffpick_makey.html', context)


def staff_pick_add(request, makey_id):
    makey = Makey.objects.get(pk=makey_id)
    makey.is_staff_pick = True
    makey.added_time_staff_pick = timezone.now()
    makey.save()
    # context = {
    #     'makey': makey,
    #     'user_details': get_user_details_json(request),
    #     # 'is_admin_user': is_admin_user
    # }
    response_text = 'Makey id = ' + str(makey.id) + ' -- Makey name = ' +\
        makey.name + ' has been added as a staff pick'
    return HttpResponse(response_text)


def staff_pick_remove(request, makey_id):
    makey = Makey.objects.get(pk=makey_id)
    makey.is_staff_pick = False
    makey.added_time_staff_pick = timezone.now()
    makey.save()
    # context = {
    #     'makey': makey,
    #     'user_details': get_user_details_json(request),
    #     # 'is_admin_user': is_admin_user
    # }
    response_text = 'Makey id = ' + str(makey.id) + ' -- Makey name = ' +\
        makey.name + ' has been removed from staff pick'
    return HttpResponse(response_text)


def makey_page_new(request, makey_id):
    makey = get_object_or_404(Makey, id=makey_id)

    return HttpResponsePermanentRedirect(makey.get_absolute_url())

def optimizeimages(imgs):
    images = []
    for image in imgs:
        imageinfo = {
        'url' : image.small_url,
        'id' : image.id
        }
        images.append(imageinfo)
    return images

def makey_page_v2_slug(request, username, makey_slug, tab=None):

    u = get_object_or_404(User, username=username)
    try:
        makey = u.makey_set.get(slug=makey_slug)
        check_private_access(request, makey)

        if tab and tab not in ["overview", "insights", "files", "docs"]:
            raise Http404

        makey_query_set = Makey.objects.filter(slug=makey.slug).prefetch_related('notes','images','videos')

        notes = makey_query_set[0].notes.all().order_by('order')
        # imgs = makey_query_set[0].images.all().order_by('order')
        # vids = makey_query_set[0].videos.all().order_by('order')


        makey_url = ''.join(['http://www.makeystreet.com',
                             makey.get_absolute_url()])
        user_details = get_user_details_json(request)

        can_edit = False
        if request.user in makey.collaborators.all() or is_admin(request):
            can_edit = True

        # images = optimizeimages(imgs)

        # imgslen = imgs.count()
        # vidslen = vids.count()

        # for img in imgs:
        #     img.url = img.small_url if img.small_url else img.large_url
        # gallery_length = int(len(imgs))+int(len(vids))

        approved_notes = makey.notes.exclude(is_pending_approval=True)
        pending_notes = makey.notes.filter(is_pending_approval=True)

        for note in notes:
            if request.user.is_authenticated():
                note_upvotes = LikeNote.objects.filter(note=note,
                                                     user=request.user)
                note.tags_count = note.tags.count()
                note.tags_all = note.tags.all()
                if len(note_upvotes) > 0:
                    note.user_upvoted = True
            else:
                note.user_upvoted = False

            note.upvote_count = LikeNote.objects.filter(note=note).count()

        user_notes_approved = None
        user_notes_pending = None
        if request.user and request.user.is_authenticated():
            user_notes_approved = makey.notes.filter(user=request.user).exclude(is_pending_approval=True)
            user_notes_pending = makey.notes.filter(user=request.user, is_pending_approval=True)

        notes = sorted(notes, key=lambda x: x.added_time,
                        reverse=True)

        notifications = []
        if request.user and request.user.is_authenticated():
            notifications = get_user_notifications(request.user)

        if request.user and request.user.is_authenticated():
            user_watching = LikeMakey.objects.filter(user=request.user,
                                                    makey=makey)

            if len(user_watching) > 0:
                makey.user_watching = True
            else:
                makey.user_watching = False

        makey.watchers_count = LikeMakey.objects.filter(makey=makey).count()

        parents = makey.get_parent_makeys()

        context = {
            'makey': makey,
            'makey_url': makey_url,
            # 'gallery_length': gallery_length,
            # 'imgs': images,
            # 'imgslen':imgslen,
            # 'vids': vids,
            # 'vidslen' : vidslen,
            'notes': notes,
            'issues_count' : makey.issues.filter(status=Issue.OPEN).count(),
            'bom_count' : makey.bom.count(),
            'approved_notes': approved_notes,
            'user_notes_approved': user_notes_approved,
            'user_notes_pending': user_notes_pending,
            'pending_notes': pending_notes,
            'user_details': user_details,
            'can_edit': can_edit,
            'parents': parents,
            'notifications': notifications
        }

        return render(request, 'catalog/makey_page_v2.html', context)
    except Makey.DoesNotExist:
        raise Http404


def makey_page_v2_settings(request, username, makey_slug):

    u = get_object_or_404(User, username=username)
    try:
        makey = u.makey_set.get(slug=makey_slug)

        check_private_access(request, makey)

        is_makey_collaborator = False
        if request.user in makey.collaborators.all() or is_admin(request):
            is_makey_collaborator = True

        is_makey_owner = False
        if request.user == makey.user or is_admin(request):
            is_makey_owner = True

        if not is_makey_collaborator or not is_makey_owner:
            raise Http404

        notifications = []
        if request.user and request.user.is_authenticated():
            notifications = get_user_notifications(request.user)

        context = {
            "makey" : makey,
            "insights_count" : makey.notes.exclude(is_pending_approval=True).count(),
            "discussions_count" : makey.question_set.count(),
            "files_count" : makey.files.count(),
            "gallery_count" : makey.images.count() + makey.videos.count(),
            "docs_count" : makey.text_documentations.count(),
            "is_makey_collaborator" : is_makey_collaborator,
            "is_makey_owner" : is_makey_owner,
            "parents" : makey.get_parent_makeys(),
            "notifications": notifications
        }

        return render(request, 'catalog/makey_page_v2_settings.html', context)

    except Makey.DoesNotExist:
        raise Http404



def makey_page_v2_insight_slug(request, username, makey_slug, insight_id):

    u = get_object_or_404(User, username=username)
    try:
        makey = u.makey_set.get(slug=makey_slug)
        check_private_access(request, makey)

        insight = Note.objects.get(id=insight_id)

        if makey not in insight.makeynotes.all():
            raise Http404

        insight_admin = False
        if request.user in makey.collaborators.all() or request.user == insight.user or is_admin(request):
            insight_admin = True

        if insight.is_pending_approval and not insight_admin:
            raise Http404

        if request.user and request.user.is_authenticated():
            note_upvotes = LikeNote.objects.filter(note=insight,
                                                     user=request.user)
            if len(note_upvotes) > 0:
                insight.user_upvoted = True
        else:
            insight.user_upvoted = False

        insight.upvote_count = LikeNote.objects.filter(note=insight).count()

        notifications = []
        if request.user and request.user.is_authenticated():
            notifications = get_user_notifications(request.user)

        context = {
            "insight" : insight,
            "makey" : makey,
            "insights_count" : makey.notes.exclude(is_pending_approval=True).count(),
            "discussions_count" : makey.question_set.count(),
            "files_count" : makey.files.count(),
            "gallery_count" : makey.images.count() + makey.videos.count(),
            "docs_count" : makey.text_documentations.count(),
            "notifications": notifications,
            "parents" : makey.get_parent_makeys()
        }

        return render(request, 'catalog/makey_page_v2_insight.html', context)

    except Makey.DoesNotExist:
        raise Http404

    except Note.DoesNotExist:
        raise Http404


def makey_page_v2_discussion_slug(request, username, makey_slug, discussion_id):

    u = get_object_or_404(User, username=username)
    try:
        makey = u.makey_set.get(slug=makey_slug)
        check_private_access(request, makey)

        question = Question.objects.get(id=discussion_id)

        if makey != question.makey:
            raise Http404

        question_admin = False
        if request.user:
            if request.user == makey.user or is_admin(request):
                question_admin = True

        notifications = []
        if request.user and request.user.is_authenticated():
            notifications = get_user_notifications(request.user)

        context = {
            "question" : question,
            "makey" : makey,
            "insights_count" : makey.notes.exclude(is_pending_approval=True).count(),
            "discussions_count" : makey.question_set.count(),
            "files_count" : makey.files.count(),
            "gallery_count" : makey.images.count() + makey.videos.count(),
            "docs_count" : makey.text_documentations.count(),
            "notifications": notifications,
            "parents" : makey.get_parent_makeys()
        }

        return render(request, 'catalog/makey_page_v2_discussion.html', context)

    except Makey.DoesNotExist:
        raise Http404

    except Question.DoesNotExist:
        raise Http404


def makey_page_v2_insight_add(request, username, makey_slug):

    if not request.user or not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('account_signup', args=[]))

    u = get_object_or_404(User, username=username)
    try:
        makey = u.makey_set.get(slug=makey_slug)
        check_private_access(request, makey)

        can_edit = False
        if request.user in makey.collaborators.all() or is_admin(request):
            can_edit = True

        images = makey.images.all().order_by('-added_time')
        for img in images:
            img.url = img.small_url if img.small_url else img.large_url

        notifications = []
        if request.user and request.user.is_authenticated():
            notifications = get_user_notifications(request.user)

        context = {
            "makey" : makey,
            "images" : images,
            "insights_count" : makey.notes.exclude(is_pending_approval=True).count(),
            "discussions_count" : makey.question_set.count(),
            "files_count" : makey.files.count(),
            "gallery_count" : makey.images.count() + makey.videos.count(),
            "docs_count" : makey.text_documentations.count(),
            "notifications": notifications,
            "parents" : makey.get_parent_makeys()
        }

        return render(request, 'catalog/makey_page_v2_insight_add.html', context)

    except Makey.DoesNotExist:
        raise Http404


def makey_page_v2_insight_edit(request, username, makey_slug, insight_id):

    if not request.user or not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('account_signup', args=[]))

    u = get_object_or_404(User, username=username)
    try:
        makey = u.makey_set.get(slug=makey_slug)
        check_private_access(request, makey)
        insight = Note.objects.get(id=insight_id)

        if request.user != insight.user and not is_admin(request):
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        images = makey.images.all().order_by('-added_time')
        for img in images:
            img.url = img.small_url if img.small_url else img.large_url

        notifications = []
        if request.user and request.user.is_authenticated():
            notifications = get_user_notifications(request.user)

        context = {
            "makey" : makey,
            "insight" : insight,
            "images" : images,
            "insights_count" : makey.notes.exclude(is_pending_approval=True).count(),
            "discussions_count" : makey.question_set.count(),
            "files_count" : makey.files.count(),
            "gallery_count" : makey.images.count() + makey.videos.count(),
            "docs_count" : makey.text_documentations.count(),
            "notifications": notifications,
            "parents" : makey.get_parent_makeys()
        }

        return render(request, 'catalog/makey_page_v2_insight_edit.html', context)

    except Makey.DoesNotExist:
        raise Http404

    except Note.DoesNotExist:
        raise Http404


def makey_page_v2_image_slug(request, username, makey_slug, gallery_id):

    u = get_object_or_404(User, username=username)
    try:
        makey = u.makey_set.get(slug=makey_slug)
        check_private_access(request, makey)

        image = Image.objects.get(id=gallery_id)

        notifications = []
        if request.user and request.user.is_authenticated():
            notifications = get_user_notifications(request.user)

        context = {
            "makey" : makey,
            "image" : image,
            "insights_count" : makey.notes.exclude(is_pending_approval=True).count(),
            "discussions_count" : makey.question_set.count(),
            "files_count" : makey.files.count(),
            "gallery_count" : makey.images.count() + makey.videos.count(),
            "docs_count" : makey.text_documentations.count(),
            "notifications": notifications,
            "parents" : makey.get_parent_makeys()
        }

        return render(request, 'catalog/makey_page_v2_image.html', context)

    except Makey.DoesNotExist:
        raise Http404

    except Note.DoesNotExist:
        raise Http404


def makey_page_v2_doc_add(request, username, makey_slug):

    if not request.user or not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('account_signup', args=[]))

    u = get_object_or_404(User, username=username)
    try:
        makey = u.makey_set.get(slug=makey_slug)
        check_private_access(request, makey)

        can_edit = False
        if request.user in makey.collaborators.all() or is_admin(request):
            can_edit = True

        if not can_edit:
            raise Http404

        images = makey.images.all().order_by('-added_time')
        for img in images:
            img.url = img.small_url if img.small_url else img.large_url

        notifications = []
        if request.user and request.user.is_authenticated():
            notifications = get_user_notifications(request.user)

        context = {
            "makey" : makey,
            "images" : images,
            "insights_count" : makey.notes.exclude(is_pending_approval=True).count(),
            "discussions_count" : makey.question_set.count(),
            "files_count" : makey.files.count(),
            "gallery_count" : makey.images.count() + makey.videos.count(),
            "docs_count" : makey.text_documentations.count(),
            "notifications": notifications,
            "parents" : makey.get_parent_makeys()
        }

        return render(request, 'catalog/makey_page_v2_doc_add.html', context)

    except Makey.DoesNotExist:
        raise Http404

def makey_page_v2_bom(request, username, makey_slug):

    u = get_object_or_404(User, username=username)
    try:
        makey = u.makey_set.get(slug=makey_slug)
        check_private_access(request, makey)

        can_edit = False
        if request.user in makey.collaborators.all() or is_admin(request):
            can_edit = True

        notifications = []
        if request.user and request.user.is_authenticated():
            notifications = get_user_notifications(request.user)

        context = {
            "makey" : makey,
            "insights_count" : makey.notes.exclude(is_pending_approval=True).count(),
            "issues_count" : makey.issues.filter(status=Issue.OPEN).count(),
            "files_count" : makey.files.count(),
            "bom_count" : makey.bom.count(),
            "docs_count" : makey.text_documentations.count(),
            "notifications": notifications,
            "parents" : makey.get_parent_makeys(),
            "can_edit" : can_edit
        }

        return render(request, 'catalog/makey_page_v2_bom.html', context)

    except Makey.DoesNotExist:
        raise Http404


def makey_page_v2_issues(request, username, makey_slug):

    u = get_object_or_404(User, username=username)
    try:
        makey = u.makey_set.get(slug=makey_slug)
        check_private_access(request, makey)

        can_edit = False
        if request.user in makey.collaborators.all() or is_admin(request):
            can_edit = True

        notifications = []
        if request.user and request.user.is_authenticated():
            notifications = get_user_notifications(request.user)

        issues_open = makey.issues.filter(status=Issue.OPEN).order_by('-added_time')
        issues_closed = makey.issues.filter(status=Issue.CLOSED).order_by('-added_time')

        issues = {
            "open" : issues_open,
            "open_count" : issues_open.count(),
            "closed" : issues_closed,
            "closed_count" : issues_closed.count(),
        }

        context = {
            "makey" : makey,
            "insights_count" : makey.notes.exclude(is_pending_approval=True).count(),
            "issues_count" : makey.issues.filter(status=Issue.OPEN).count(),
            "files_count" : makey.files.count(),
            "bom_count" : makey.bom.count(),
            "docs_count" : makey.text_documentations.count(),
            "notifications": notifications,
            "parents" : makey.get_parent_makeys(),
            "can_edit" : can_edit,
            "issues" : issues
        }

        return render(request, 'catalog/makey_page_v2_issues.html', context)

    except Makey.DoesNotExist:
        raise Http404


def makey_page_v2_issue_add(request, username, makey_slug):

    if not request.user or not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('account_signup', args=[]))

    u = get_object_or_404(User, username=username)
    try:
        makey = u.makey_set.get(slug=makey_slug)
        check_private_access(request, makey)

        if request.method == "POST":
            form = AddIssueForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data["title"]
                description = form.cleaned_data["description"]

                issue = Issue(owner=request.user,
                                title=title,
                                makey = makey
                                )
                issue.save()

                tag_names = request.POST.getlist('tag_name')
                for tag_name in tag_names:
                    issue.labels.add(tag_name)

                if description:
                    comment = Comment(user=request.user, body=description)
                    comment.save()
                    issue.comments.add(comment)

            return HttpResponseRedirect(reverse('catalog:makey_new_issue', args=[makey.user.username, makey.slug, issue.id]))

        else:

            notifications = []
            if request.user and request.user.is_authenticated():
                notifications = get_user_notifications(request.user)

            context = {
                "makey" : makey,
                "insights_count" : makey.notes.exclude(is_pending_approval=True).count(),
                "issues_count" : makey.issues.filter(status=Issue.OPEN).count(),
                "files_count" : makey.files.count(),
                "bom_count" : makey.bom.count(),
                "docs_count" : makey.text_documentations.count(),
                "notifications": notifications,
                "parents" : makey.get_parent_makeys()
            }

            return render(request, 'catalog/makey_page_v2_issue_add.html', context)

    except Makey.DoesNotExist:
        raise Http404


def makey_page_v2_issue(request, username, makey_slug, issue_id):

    u = get_object_or_404(User, username=username)
    try:
        makey = u.makey_set.get(slug=makey_slug)
        check_private_access(request, makey)
        issue = Issue.objects.get(id=issue_id)

        if makey != issue.makey:
            raise Http404

        issue_admin = False
        if request.user in makey.collaborators.all() or is_admin(request):
            issue_admin = True

        if request.method == "POST":
            if not request.user or not request.user.is_authenticated():
                return HttpResponseRedirect(reverse('account_signup', args=[]))

            action = request.POST.get("action", "")
            if action == "add-issue-comment":
                form = AddIssueCommentForm(request.POST)
                if form.is_valid():
                    body = form.cleaned_data["body"]

                    comment = Comment(user=request.user, body=body)
                    comment.save()
                    issue.comments.add(comment)

                return HttpResponseRedirect(reverse('catalog:makey_new_issue', args=[makey.user.username, makey.slug, issue.id]))

            elif action == "add-assignee":
                form = AddIssueAssigneeForm(request.POST)
                if form.is_valid():
                    user_id = form.cleaned_data["user_id"]

                    assignee = User.objects.get(id=user_id)
                    issue.assignee = assignee
                    issue.save()

                return HttpResponseRedirect(reverse('catalog:makey_new_issue', args=[makey.user.username, makey.slug, issue.id]))

            elif action == "remove-assignee":
                issue.assignee = None
                issue.save()

                return HttpResponseRedirect(reverse('catalog:makey_new_issue', args=[makey.user.username, makey.slug, issue.id]))

            elif action == "close-issue":
                issue.status = Issue.CLOSED
                issue.closed_time = timezone.now()
                issue.save()

                return HttpResponseRedirect(reverse('catalog:makey_new_issue', args=[makey.user.username, makey.slug, issue.id]))

            elif action == "reopen-issue":
                issue.status = Issue.OPEN
                issue.closed_time = None
                issue.save()

                return HttpResponseRedirect(reverse('catalog:makey_new_issue', args=[makey.user.username, makey.slug, issue.id]))

        else:

            notifications = []
            if request.user and request.user.is_authenticated():
                notifications = get_user_notifications(request.user)

            context = {
                "issue" : issue,
                "makey" : makey,
                "insights_count" : makey.notes.exclude(is_pending_approval=True).count(),
                "issues_count" : makey.issues.filter(status=Issue.OPEN).count(),
                "files_count" : makey.files.count(),
                "bom_count" : makey.bom.count(),
                "docs_count" : makey.text_documentations.count(),
                "notifications": notifications,
                "parents" : makey.get_parent_makeys(),
                "issue_admin": issue_admin
            }

            return render(request, 'catalog/makey_page_v2_issue.html', context)

    except Makey.DoesNotExist:
        raise Http404

    except Issue.DoesNotExist:
        raise Http404


def makey_page_v2_milestones(request, username, makey_slug):

    u = get_object_or_404(User, username=username)
    try:
        makey = u.makey_set.get(slug=makey_slug)
        check_private_access(request, makey)

        can_edit = False
        if request.user in makey.collaborators.all() or is_admin(request):
            can_edit = True

        notifications = []
        if request.user and request.user.is_authenticated():
            notifications = get_user_notifications(request.user)

        # milestones_open = makey.milestones.filter(status=Issue.OPEN)
        # milestones_closed = makey.milestones.filter(status=Issue.CLOSED)

        print issues_open.query
        print issues_closed.query

        issues = {
            "open" : issues_open,
            "open_count" : issues_open.count(),
            "closed" : issues_closed,
            "closed_count" : issues_closed.count(),
        }

        context = {
            "makey" : makey,
            "insights_count" : makey.notes.exclude(is_pending_approval=True).count(),
            "issues_count" : makey.issues.filter(status=Issue.OPEN).count(),
            "files_count" : makey.files.count(),
            "bom_count" : makey.bom.count(),
            "docs_count" : makey.text_documentations.count(),
            "notifications": notifications,
            "parents" : makey.get_parent_makeys(),
            "can_edit" : can_edit,
        }

        return render(request, 'catalog/makey_page_v2_milestones.html', context)

    except Makey.DoesNotExist:
        raise Http404
def edit_makey_page(request, makey_id):

    try:
        user_details = get_user_details_json(request)
        makey = Makey.objects.get(id=makey_id)
        makey.can_edit = False

        if request.user not in makey.collaborators.all() and\
                not is_admin(request):
            return HttpResponseRedirect(reverse('catalog:makey',
                                                args=[makey.id]))
        else:
            can_edit = True
            makey_url = ''.join(['http://www.makeystreet.com',
                                 makey.get_absolute_url()])

            context = {
                'makey': makey,
                'makey_url': makey_url,
                'makey_id': makey.id,
                'makey_name': makey.name,
                'can_edit': can_edit,
                'user_details': user_details,
                'static_blob': static_blob,
            }
            return render(request, 'catalog/edit_makey_page.html', context)
    except Makey.DoesNotExist:
        raise Http404

def makey_action(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse('catalog:landing_page',
                                    args=[]))

    # TODO: Redirect to login page
    if not request.user or not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('catalog:landing_page',
                                    args=[]))


    action = request.POST.get("action", "")
    makey_id = request.POST.get("makey_id", "")
    insight_id = request.POST.get("insight_id", "")

    if not makey_id or not action:
        return HttpResponseRedirect(reverse('catalog:landing_page',
                                    args=[]))

    makey = Makey.objects.get(id=makey_id)
    check_private_access(request, makey)

    if action == "delete-makey":
        if request.user != makey.user:
            return HttpResponseForbidden()

        parent_makey = None
        if makey.used_in.count() == 1:
            parent_makey = makey.used_in.all()[0]
        makey.used_in.clear()
        makey.is_enabled = False
        makey.save()

        if parent_makey:
            return HttpResponseRedirect(reverse('catalog:makey_new_slug',
                            args=[parent_makey.user.username, parent_makey.slug]))

        return HttpResponseRedirect(reverse('catalog:user_dashboard', args=[]))

    elif action == "add-insight":
        form = AddInsightForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]

            insight = Note(user=request.user,
                            title=title,
                            body=description
                            )

            if request.user not in makey.collaborators.all():
                insight.is_pending_approval = True

            insight.save()
            makey.notes.add(insight)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif action == "delete-insight":
        form = DeleteInsightForm(request.POST)
        if form.is_valid():
            insight = Note.objects.get(id=insight_id)
            if insight and insight.user == request.user:
                insight.delete()
                return HttpResponseRedirect(reverse('catalog:makey_new_tab_slug',
                    args=[makey.user.username,makey.slug,'insights']))

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif action == "ask-question":
        form = AskQuestionForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]

            question = Question(creator=request.user,
                            name=title,
                            description=description,
                            makey=makey
                            )

            question.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif action == "add-insight-comment":
        form = AddInsightCommentForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data["body"]
            insight_id = form.cleaned_data["insight_id"]

            insight = Note.objects.get(id=insight_id)

            if insight:
                comment = Comment(user=request.user,
                    body=body)
                comment.save()
                insight.comments.add(comment)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif action == "add-image-comment":
        form = AddImageCommentForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data["body"]
            image_id = form.cleaned_data["image_id"]

            image = Image.objects.get(id=image_id)

            if image:
                comment = Comment(user=request.user,
                    body=body)
                comment.save()
                image.comments.add(comment)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif action == "add-answer-comment":
        form = AddAnswerCommentForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data["body"]
            answer_id = form.cleaned_data["answer_id"]

            answer = Answer.objects.get(id=answer_id)

            if answer:
                comment = Comment(user=request.user,
                    body=body,
                    answer=answer)
                comment.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif action == "add-question-comment":
        form = AddQuestionCommentForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data["body"]
            question_id = form.cleaned_data["question_id"]

            question = Question.objects.get(id=question_id)

            if question:
                comment = Comment(user=request.user,
                    body=body, question=question)
                comment.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif action == "add-answer":
        form = AddAnswerForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data["description"]
            question_id = form.cleaned_data["question_id"]

            question = Question.objects.get(id=question_id)

            if question:
                answer = Answer(creator=request.user,
                                description=description,
                                question=question)
                answer.save()
                question.answer_set.add(answer)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif action == "toggle-upvote-insight":
        form = UpvoteInsight(request.POST)
        if form.is_valid():
            insight_id = form.cleaned_data["insight_id"]
            insight = Note.objects.get(id=insight_id)

            if not insight:
                raise Http404

            upvotes = LikeNote.objects.filter(user=request.user,
                                    note=insight)

            if not upvotes:
                upvote = LikeNote(user=request.user,
                    note=insight)
                upvote.save()
            else:
                upvotes[0].delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif action == "toggle-makey-watch":
        form = WatchMakey(request.POST)
        if form.is_valid():
            watches = LikeMakey.objects.filter(user=request.user,
                                    makey=makey)

            if not watches:
                watch = LikeMakey(user=request.user,
                    makey=makey)
                watch.save()
            else:
                watches[0].delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif action == "add-image":
        form = AddImageForm(request.POST)
        if form.is_valid():
            image_urls = request.POST.getlist('image_url')
            for image_url in image_urls:
                image = Image(user=request.user,
                    large_url=image_url)

                image.save()
                makey.images.add(image)

            # Calling image resize job
            if os.environ.get('DJANGO_SETTINGS_MODULE', '') != 'woot.settings.dev':
                unirest.get('http://www.makeystreet.com/image/update/all/')
            else:
                print('Image Update Called')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif action == "add-insight-image":
        form = AddInsightImageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]

            insight = Note(user=request.user,
                            title=title,
                            body=description
                            )

            if request.user not in makey.collaborators.all():
                insight.is_pending_approval = True

            insight.save()
            makey.notes.add(insight)

            tag_names = request.POST.getlist('tag_name')
            for tag_name in tag_names:
                insight.tags.add(tag_name)

            image_id = form.cleaned_data['image_id']
            image_url = form.cleaned_data['image_url']

            if not image_id and not image_url:
                return HttpResponseRedirect(reverse('catalog:makey_new_insight_slug',
                    args=[makey.user.username,makey.slug,insight.id]))

            if image_url:
                image = Image(user=request.user,
                    large_url=image_url)

                image.save()
                insight.image = image
                insight.save()
                makey.images.add(image)

                # Calling image resize job
                if os.environ.get('DJANGO_SETTINGS_MODULE', '') != 'woot.settings.dev':
                    unirest.get('http://www.makeystreet.com/image/update/all/')
                else:
                    print('Image Update Called')

                return HttpResponseRedirect(reverse('catalog:makey_new_insight_slug',
                    args=[makey.user.username,makey.slug,insight.id]))

            if image_id:
                image = Image.objects.get(id=image_id)
                insight.image = image
                insight.save()
                return HttpResponseRedirect(reverse('catalog:makey_new_insight_slug',
                    args=[makey.user.username,makey.slug,insight.id]))

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif action == "edit-insight-image":
        form = EditInsightImageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            insight_id = form.cleaned_data["insight_id"]

            insight = Note.objects.get(id=insight_id)
            insight.title=title
            insight.body=description
            insight.save()

            tag_names = request.POST.getlist('tag_name')
            insight.tags.clear()
            for tag_name in tag_names:
                insight.tags.add(tag_name)

            image_id = form.cleaned_data['image_id']
            image_url = form.cleaned_data['image_url']

            if not image_id and not image_url:
                return HttpResponseRedirect(reverse('catalog:makey_new_insight_slug',
                    args=[makey.user.username,makey.slug,insight.id]))

            if image_url:
                image = Image(user=request.user,
                    large_url=image_url)

                image.save()
                insight.image = image
                insight.save()
                makey.images.add(image)

                # Calling image resize job
                if os.environ.get('DJANGO_SETTINGS_MODULE', '') != 'woot.settings.dev':
                    unirest.get('http://www.makeystreet.com/image/update/all/')
                else:
                    print('Image Update Called')

                return HttpResponseRedirect(reverse('catalog:makey_new_insight_slug',
                    args=[makey.user.username,makey.slug,insight.id]))

            if insight.image and insight.image.id != image_id:
                if image_id:
                    image = Image.objects.get(id=image_id)
                    insight.image = image
                else:
                    insight.image = None
                insight.save()
                return HttpResponseRedirect(reverse('catalog:makey_new_insight_slug',
                    args=[makey.user.username,makey.slug,insight.id]))

            return HttpResponseRedirect(reverse('catalog:makey_new_insight_slug',
                    args=[makey.user.username,makey.slug,insight.id]))

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif action == "add-video":
        form = AddVideoForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            site = form.cleaned_data['site']
            video = Video(user=request.user,
                url=url, site=site)

            video.save()
            makey.videos.add(video)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif action == "add-file":
        form = AddFileForm(request.POST)
        if form.is_valid():
            file_url = form.cleaned_data['file_url']
            file_desc = form.cleaned_data['file_desc']
            file_name = form.cleaned_data['file_name']
            file_type = form.cleaned_data['file_type']
            upfile = UpFile(user=request.user,
                url=file_url, filename=file_name,
                filetype=file_type, description=file_desc)

            upfile.makey = makey
            upfile.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif action == "add-collaborator":
        form = AddCollaboratorForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            collab = User.objects.get(id=user_id)
            if collab:
                makey.collaborators.add(collab)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif action == "remove-collaborator":
        form = RemoveCollaboratorForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            collab = User.objects.get(id=user_id)
            if collab:
                makey.collaborators.remove(collab)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif action == "edit-makey-name-desc":
        form = EditMakeyNameDescForm(request.POST)
        if form.is_valid():
            makey_name = form.cleaned_data['makey_name']
            makey_desc = form.cleaned_data['makey_desc']
            makey_github = form.cleaned_data['makey_github']
            makey.name = makey_name
            makey.about = makey_desc
            makey.github_url = makey_github
            makey.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif action == "add-doc":
        form = AddDocForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]

            doc = TextDocumentation(user=request.user,
                            title=title,
                            body=body,
                            makey=makey
                            )

            doc.save()

            tag_names = request.POST.getlist('tag_name')
            for tag_name in tag_names:
                doc.tags.add(tag_name)

            return HttpResponseRedirect(reverse('catalog:makey_new_tab_slug',
                    args=[makey.user.username,makey.slug,'docs']))

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif action == "add-bom":
        form = AddBOMForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            quantity = form.cleaned_data["quantity"]
            comments = form.cleaned_data["comments"]

            bom = BOM(name=name,
                        quantity=quantity,
                        comments=comments,
                        makey=makey
                        )

            bom.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif action == "edit-bom":
        form = EditBOMForm(request.POST)
        if form.is_valid():
            bom_id = form.cleaned_data["bom_id"]
            bom = BOM.objects.get(id=bom_id)
            name = form.cleaned_data["name"]
            quantity = form.cleaned_data["quantity"]
            comments = form.cleaned_data["comments"]

            bom.name = name
            bom.quantity = quantity
            bom.comments = comments
            bom.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif action == "delete-bom":
        form = DeleteBOMForm(request.POST)
        if form.is_valid():
            bom_id = form.cleaned_data["bom_id"]
            bom = BOM.objects.get(id=bom_id)
            bom.delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def all_makeys(request):
    user_details = get_user_details_json(request)

    q = request.GET.get('q', '')
    if q:
        makeys = Makey.objects.filter(is_enabled=True).\
            filter(Q(name__icontains=q))
    else:
        makeys = Makey.objects.filter(is_enabled=True).\
            filter(is_private=False).order_by('-score')
    q_sort = request.GET.get('sort')
    if q_sort and q_sort.lower() == 'latest':
        makeys = makeys.order_by('-added_time')

    paginator = Paginator(makeys, 12)

    page = request.GET.get('page')
    if not page:
        page = 1
    try:
        makeys_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        makeys_page = paginator.page(1)
        page = 1
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last
        # page of results.
        makeys_page = paginator.page(paginator.num_pages)
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

    enable_search = is_admin(request)

    context = {
        'makeys': makeys_page,
        'list_pages': list_pages,
        'static_blob': static_blob,
        'user_details': user_details,
        'query': q,
        'enable_search': enable_search,
    }

    return render(request, 'catalog/all_makeys.html', context)


def makey_search(request):
    user_details = get_user_details_json(request)

    context = {
        'static_blob': static_blob,
        'user_details': user_details,
    }

    return render(request, 'catalog/makey_search.html', context)


def search_in_makey(request, username, makey_slug):
    user = get_object_or_404(User, username=username)

    try:
        m = user.makey_set.get(slug=makey_slug)
        q = request.GET.get('q', '')

        if q:
            context = {
                'results': m.search_content(q),
                'q': q,
                'makey': m,
            }

            return render(request, 'catalog/search_in_makey.html', context)
    except Makey.DoesNotExist:
        return Http404


def search_in_makey_submodules(request, username, makey_slug):
    user = get_object_or_404(User, username=username)

    try:
        m = user.makey_set.get(slug=makey_slug)
        q = request.GET.get('q', '')

        results = m.search_in_submodules(query=q)

        notifications = []
        if request.user and request.user.is_authenticated():
            notifications = get_user_notifications(request.user)

        count = 0
        for makey, result_set in results:
            count += result_set['count']
        if q:
            context = {
                'results': results,
                'q': q,
                'count': count,
                'makey': m,
                'insights_count' : m.notes.exclude(is_pending_approval=True).count(),
                'discussions_count' : m.question_set.count(),
                'files_count' : m.files.count(),
                'gallery_count' : m.images.count() + m.videos.count(),
                'docs_count' : m.text_documentations.count(),
                'notifications': notifications,
                'parents' : m.get_parent_makeys()
            }

            return render(request, 'catalog/makey_page_v2_search.html', context)

    except Makey.DoesNotExist:
        return Http404


def save_makey(request, makey_id):
    try:
        m = Makey.objects.get(id=makey_id)
        if os.environ.get('DJANGO_SETTINGS_MODULE', '') != 'woot.settings.dev':
            unirest.get('http://www.makeystreet.com/image/update/all/')
        else:
            print('Image Update Called')
        return HttpResponseRedirect(m.get_absolute_url())
    except Makey.DoesNotExist:
        raise Http404


def makey_add_submodule(request, makey_id):
    makey = get_object_or_404(Makey, id=makey_id)

    if request.user not in makey.collaborators.all() and not is_admin(request):
        raise Http404

    if request.method == "GET":
        return render(request, 'catalog/makey_add_submodule.html', {
            'makey': makey
        });

    elif request.method == "POST":
        try:
            form = CreateMakeyForm(request.POST)

            if form.is_valid():
                m = Makey()

                m.user = request.user
                m.name = form.cleaned_data['val_name']
                m.about = form.cleaned_data['val_about']
                # m.status = form.cleaned_data['status_chosen']
                # if form.cleaned_data['val_privacy'] == 'private':
                #     m.is_private = True
                # else:
                #     m.is_private = False
                m.added_time = timezone.now()
                m.save()
                m.collaborators.add(request.user)

                for collaborator in makey.collaborators.all():
                    m.collaborators.add(collaborator)

                makey.modules_used.add(m);

                return HttpResponseRedirect(reverse('catalog:makey', args=[makey.id]))

            else:
                return render(request, 'catalog/makey_add_submodule.html', {
                    'makey': makey,
                    'form' : form
                });

        except Exception as e:
            print e.__doc__
            print e.message

    else:
        raise Http404


def get_instructable(request):
    if request.method == "POST":
        i_url = request.POST.get('url', '')
        iid = i_url[i_url.find('id/')+3:]
        iid = iid[:iid.find('/')]

        request_url = "https://devru-instructables.p.mashape.com/json-api/showInstructable?id=%s" % iid
        response = unirest.get(request_url, headers={"X-Mashape-Key": "bFwgqo4DgkmshN0WngKeteya4503p1YiqAFjsnbiOJQ2YWRTQc"})

        makey = Makey()
        makey.added_time = timezone.now()
        makey.user = request.user
        makey.name = response.body['title']
        makey.url = i_url
        makey.collaborators.add(request.user)

        steps = response.body['steps']
        makey.why = steps[0]['body']
        makey.status = 'Completed'
        makey.save()

        if response.body['coverImage']:
            coverPic = Image()
            coverPic.added_time = timezone.now()
            coverPic.user = request.user
            coverPic.large_url = response.body['coverImage']['downloadUrl']
            coverPic.save()
            makey.cover_pic = coverPic
            makey.save()

        for f in response.body['files']:
            if not f['image']:
                continue
            img = Image()
            img.added_time = timezone.now()
            img.user = request.user
            img.large_url = f['downloadUrl']
            img.save()
            makey.images.add(img)

        for f in steps[0]['files']:
            if not f['image']:
                continue
            img = Image()
            img.added_time = timezone.now()
            img.user = request.user
            img.large_url = f['downloadUrl']
            img.save()
            makey.images.add(img)

        for i in range(1, len(steps)):
            step = steps[i]

            s = InstructableStep()
            s.added_time = timezone.now()
            s.user = request.user
            s.iid = step['id']
            s.url = step['url']
            s.title = step['title']
            s.body = step['body']
            s.step = step['stepIndex']
            s.words = step['wordCount']
            s.makey = makey
            s.save()

            for f in step['files']:
                if not f['image']:
                    continue
                img = Image()
                img.added_time = timezone.now()
                img.user = request.user
                img.large_url = f['downloadUrl']
                img.save()
                makey.images.add(img)
                s.images.add(img)
        return HttpResponseRedirect(reverse('catalog:makey', args=[makey.id]))

    context = {
        'static_blob': static_blob,
        'user_details': get_user_details_json(request),
    }
    return render(request, 'catalog/get_instructable.html', context)


def collection(request, collection_id):
    # if not is_admin(request):
    #     raise Http404

    collection = Collection.objects.get(id=collection_id)
    context = {
        'collection' : collection
    }
    return render(request, 'catalog/collection.html', context)


def add_makey_to_collection(request, collection_id, makey_id):
    # if not is_admin(request):
    #     raise Http404

    try:
        collection = Collection.objects.get(id=collection_id)
        makey = Makey.objects.get(id=makey_id)

        collection.makeys.add(makey)

        return HttpResponseRedirect(reverse('catalog:makey_collection', args=[collection.id]))

    except Makey.DoesNotExist:
        raise Http404

    except Collection.DoesNotExist:
        raise Http404


def remove_makey_from_collection(request, collection_id, makey_id):
    # if not is_admin(request):
    #     raise Http404

    try:
        collection = Collection.objects.get(id=collection_id)
        makey = Makey.objects.get(id=makey_id)

        collection.makeys.remove(makey)

        return HttpResponseRedirect(reverse('catalog:makey_collection', args=[collection.id]))

    except Makey.DoesNotExist:
        raise Http404

    except Collection.DoesNotExist:
        raise Http404


def add_user_to_makey(request, makey_id, user_id):
    # if not is_admin(request):
    #     raise Http404

    try:
        makey = Makey.objects.get(id=makey_id)
        user = User.objects.get(id=user_id)

        makey.collaborators.add(user)

        return HttpResponseRedirect(reverse('catalog:makey_new_slug', args=[makey.user.username, makey.slug]))

    except Makey.DoesNotExist:
        raise Http404

    except User.DoesNotExist:
        raise Http404


def remove_user_from_makey(request, makey_id, user_id):
    # if not is_admin(request):
    #     raise Http404

    try:
        makey = Makey.objects.get(id=makey_id)
        user = User.objects.get(id=user_id)

        makey.collaborators.remove(user)

        return HttpResponseRedirect(reverse('catalog:makey_new_slug', args=[makey.user.username, makey.slug]))

    except Makey.DoesNotExist:
        raise Http404

    except User.DoesNotExist:
        raise Http404


def collection_wall(request, collection_id):

    collection = Collection.objects.get(id=collection_id)
    insights = []
    for makey in collection.makeys.all():
        insights += get_makey_insights(makey, True)

    insights = sorted(insights, key=lambda x: x.added_time,
                            reverse=True)

    context = {
        'collection' : collection,
        'insights' : insights
    }
    return render(request, 'catalog/collection_wall.html', context)


def collections_mit(request):

    collections = [Collection.objects.get(id=1),
                    Collection.objects.get(id=2),
                    Collection.objects.get(id=3),
                    Collection.objects.get(id=4),
                    Collection.objects.get(id=5),
                    Collection.objects.get(id=6),
                    Collection.objects.get(id=7),
                    Collection.objects.get(id=8),
                    Collection.objects.get(id=9),
                    Collection.objects.get(id=10)
    ]

    for collection in collections:
        insights = []
        for makey in collection.makeys.all():
            insights += get_makey_insights(makey, True)

        insights = sorted(insights, key=lambda x: x.added_time,
                                reverse=True)

        collection.insights = insights

    collections = sorted(collections, key=lambda x: len(x.insights), reverse=True)

    context = {
        'collections' : collections
    }
    return render(request, 'catalog/collection_mit.html', context)


def collections_mit_all(request):

    collections = [Collection.objects.get(id=1),
                    Collection.objects.get(id=2),
                    Collection.objects.get(id=3),
                    Collection.objects.get(id=4),
                    Collection.objects.get(id=5),
                    Collection.objects.get(id=6),
                    Collection.objects.get(id=7),
                    Collection.objects.get(id=8),
                    Collection.objects.get(id=9),
                    Collection.objects.get(id=10)
    ]

    insights_all = []
    for collection in collections:
        insights = []
        for makey in collection.makeys.all():
            insights += get_makey_insights(makey, True)

        for insight in insights:
            insight.collection = collection

        insights_all += insights

    insights_all = sorted(insights_all, key=lambda x: x.added_time,
                                reverse=True)

    context = {
        'insights' : insights_all
    }
    return render(request, 'catalog/collection_mit_all.html', context)


def collections_wehack(request):

    collections = [Collection.objects.get(id=11),
                    Collection.objects.get(id=12),
                    Collection.objects.get(id=13)
    ]

    for collection in collections:
        insights = []
        for makey in collection.makeys.all():
            insights += get_makey_insights(makey, True)

        insights = sorted(insights, key=lambda x: x.added_time,
                                reverse=True)

        collection.insights = insights

    collections = sorted(collections, key=lambda x: len(x.insights), reverse=True)

    context = {
        'collections' : collections
    }
    return render(request, 'catalog/collection_wehack.html', context)


def collections_wehack_all(request):

    collections = [Collection.objects.get(id=11),
                    Collection.objects.get(id=12),
                    Collection.objects.get(id=13)
    ]

    insights_all = []
    for collection in collections:
        insights = []
        for makey in collection.makeys.all():
            insights += get_makey_insights(makey, True)

        for insight in insights:
            insight.collection = collection

        insights_all += insights

    insights_all = sorted(insights_all, key=lambda x: x.added_time,
                                reverse=True)

    context = {
        'insights' : insights_all
    }
    return render(request, 'catalog/collection_wehack_all.html', context)

def collections_snt15(request):

    collections = [Collection.objects.get(id=14),
                    Collection.objects.get(id=15),
                    Collection.objects.get(id=16),
                    Collection.objects.get(id=17)
    ]

    for collection in collections:
        insights = []
        for makey in collection.makeys.all():
            insights += get_makey_insights(makey, True)

        insights = sorted(insights, key=lambda x: x.added_time,
                                reverse=True)

        collection.insights = insights

    collections = sorted(collections, key=lambda x: len(x.insights), reverse=True)

    context = {
        'collections' : collections
    }
    return render(request, 'catalog/collection_snt15.html', context)


def collections_snt15_all(request):

    collections = [Collection.objects.get(id=14),
                    Collection.objects.get(id=15),
                    Collection.objects.get(id=16),
                    Collection.objects.get(id=17)
    ]

    insights_all = []
    for collection in collections:
        insights = []
        for makey in collection.makeys.all():
            insights += get_makey_insights(makey, True)

        for insight in insights:
            insight.collection = collection

        insights_all += insights

    insights_all = sorted(insights_all, key=lambda x: x.added_time,
                                reverse=True)

    context = {
        'insights' : insights_all
    }
    return render(request, 'catalog/collection_snt15_all.html', context)
