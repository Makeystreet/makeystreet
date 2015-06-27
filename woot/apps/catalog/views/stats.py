from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from .helper import get_user_details_json
import datetime

import reversion
from apps.catalog.models.core import Makey


def backend_stats(request):
    login = request.user.is_authenticated()
    user_details = get_user_details_json(request)
    users = User.objects.all().order_by('-date_joined')

    context = {
        'static_blob': settings.STATIC_BLOB,
        'login': login,
        'user_details': user_details,
        'users': users,
    }

    return render(request, 'catalog/stats.html', context)


def backend_stats_old(request):
    login = request.user.is_authenticated()
    user_details = get_user_details_json(request)
    users = User.objects.all().order_by('-date_joined')

    context = {
        'static_blob': settings.STATIC_BLOB,
        'login': login,
        'user_details': user_details,
        'users': users,
    }

    return render(request, 'catalog/stats_old.html', context)


def backend_stats_temp(request):
    login = request.user.is_authenticated()
    user_details = get_user_details_json(request)
    # week=[]
    # week.append("hello")
    weeks = []
    week = {}
    week["end_users"] = User.objects.all().count()
    # print "\n"
    # print users
    week["end_time"] = datetime.date.today

    for i in range(0, 12):
        # print "-------------------"
        # print i
        week["id"] = i
        week["start_time"] = datetime.date.today() -\
            datetime.timedelta(datetime.date.today().weekday()) -\
            datetime.timedelta(days=7*i)
        # print week["end_time"]
        # print week["start_time"]
        week["start_users"] = User.objects.filter(date_joined__lte=
                                                  week["start_time"]).count()
        # print week["end_users"]
        # print week["start_users"]
        week["new_users"] = week["end_users"] - week["start_users"]
        # print "new_users: ",week["new_users"]
        week["growth"] = float(week["new_users"]*100)/week["start_users"]
        # print "growth %: ", week["growth"]
        weeks.append(week.copy())

        week["end_users"] = week["start_users"]
        week["end_time"] = week["start_time"]

    target_cent = 7
    target = float(weeks[0]["start_users"]*7)/100

    context = {
        'static_blob': settings.STATIC_BLOB,
        'login': login,
        'user_details': user_details,
        # 'users': users,
        'weeks': weeks,
        'target': target,
        'target_cent': target_cent,
    }

    return render(request, 'catalog/stats_temp.html', context)


class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)

    def added(self):
        return self.set_current - self.intersect

    def removed(self):
        return self.set_past - self.intersect

    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])

    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])


def makey_diff(request, makey_id):
    makey = get_object_or_404(Makey, id=makey_id)
    versions = reversion.get_for_object(makey)
    # from reversion.models import Version
    # versions = Version.objects.order_by('revision__date_created')[:20]

    v = []
    if(len(versions) > 1):
        for i in range(len(versions) - 1):
            temp = {}
            temp['version'] = versions[i]

            new_version = versions[i]
            old_version = versions[i+1]

            diff_ = DictDiffer(new_version.field_dict, old_version.field_dict)
            diff = list(diff_.changed())

            changes = {}
            for field in diff:
                changes[field + '::new'] = new_version.field_dict[field]
                changes[field + '::old'] = old_version.field_dict[field]
            temp['changes'] = changes
            v.append(temp)
    v.append({'version': versions[len(versions) - 1], 'changes': {}})

    context = {
        'makey': makey,
        'versions': v
    }

    return render(request, 'catalog/makey_diff.html', context)
