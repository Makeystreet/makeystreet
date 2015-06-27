# from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse


# Create your views here.
def refill_emails():
    users = User.objects.all()
    for u in users:
        if u.email == "":
            a = u.socialaccount_set.first()
            try:
                u.email = a.extra_data['email']
                u.save()
            except:
                pass


def uptime_check(request):
    return HttpResponse('Success, OK!')
