import logging

from django.contrib import auth, messages
from django.http import HttpResponseRedirect

logger = logging.getLogger(__name__)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def login_cancelled(request):
    messages.error(request, 'Login Failed! Please try again.')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
