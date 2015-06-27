from django.core.cache import cache
from django.http import HttpResponseRedirect


def login_required(cur_view):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect("/launching_soon")
        else:
            return cur_view(request, *args, **kwargs)

    return _wrapped_view


def cache_per_user(ttl=None, prefix=None, cache_post=False):
    '''Decorator that makes the view cache per User
    * ttl - Lifetime of cache, not sending this parameter means that the
      cache will last until the server reboots or decides to remove it
    * prefix - Prefix to be used to store the response in the cache. If not
      set, 'view_cache _' + function .__ name__ will be used
    * cache_post - Whether POST request can be cached
    * The cache for anonymous users is shared with all
    * The key cache is one of the possible options:
        '% s_% s'% (prefix, user.id)
        's_anonymous%'% (prefix)
        'view_cache_% s_% s'% (function .__ name__, user.id)
        'view_cache_ s_anonymous%'% (function .__ name__)

    Author: eu@rafaelsdm.com
    '''
    def decorator(function):
        def apply_cache(request, *args, **kwargs):
            # Generates the part of the User remaining in the cache key
            if request.user.is_anonymous():
                user = 'anonymous'
            else:
                user = request.user.id

            # Generates the cache key
            if prefix:
                CACHE_KEY = '%s_%s' % (prefix, user)
            else:
                CACHE_KEY = 'view_cache_%s_%s' % (function.__name__, user)

            # Verifies that you can cache the request
            if not cache_post and request.method == 'POST':
                can_cache = False
            else:
                can_cache = True

            if can_cache:
                response = cache.get(CACHE_KEY, None)
            else:
                response = None

            if not response:
                response = function(request, *args, **kwargs)
                if can_cache:
                    cache.set(CACHE_KEY, response, ttl)
            return response
        return apply_cache
    return decorator
