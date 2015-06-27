from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from woot.apps.catalog.models.core import Makey, Space
from woot.apps.catalog.models.like import LikeMakey


@cache_page(60 * 15)
def makey_page(request, makey_id):
    makey = Makey.objects.get(pk=makey_id)
    likes = LikeMakey.objects.filter(makey=makey)

    if makey:
        if makey.cover_pic:
            cover_pic = makey.cover_pic
        else:
            cover_pic = makey.images.all()[0]

        makey.parts_count = len(makey.partsused.all()) +\
            len(makey.new_parts.all())
        makey.likes_count = len(likes)

        return render(request, 'catalog/embed/makey.html', {
            'makey': makey,
            'cover_pic': cover_pic,
        })
    else:
        return HttpResponse('404 Error - This Makey does not exist')


@cache_page(60 * 15)
def space_page(request, space_id):
    space = Space.objects.get(pk=space_id)

    if space:
        return render(request, 'catalog/embed/space.html', {
            'space': space,
        })
    else:
        return HttpResponse('404 Error - This Makey does not exist')
        # space.no_admins = space.admins.count()
        # space.no_members = space.members.count()
        # space.no_makeys = space.makeys_made_in.count()


# @cache_page(60 * 15)
def makey_hierarchy(request, makey_id):
    makey = Makey.objects.get(pk=makey_id)
    likes = LikeMakey.objects.filter(makey=makey)

    if makey:
        if makey.cover_pic:
            cover_pic = makey.cover_pic
        else:
            cover_pic = makey.images.all()[0]

        makey.parts_count = len(makey.partsused.all()) +\
            len(makey.new_parts.all())
        makey.likes_count = len(likes)

        return render(request, 'catalog/embed/makey_hierarchy.html', {
            'makey': makey,
            'cover_pic': cover_pic,
        })
    else:
        return HttpResponse('404 Error - This Makey does not exist')
