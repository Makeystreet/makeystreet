# Custom Admin Site
from django.contrib import admin
from django.conf import settings
from adminplus.sites import AdminSitePlus

from django.conf.urls import patterns, include, url

# This is the stuff for sitemap
from django.contrib.sitemaps import GenericSitemap
from apps.catalog.models.core import Product, Makey, Space, User
from django.db.models import Count

from woot.apps.catalog.views import auth
import apps.core.views

users = User.objects.all()

# See: https://docs.djangoproject.com/en/dev/ref/
# contrib/admin/#hooking-adminsite-instances-into-your-urlconf
admin.site = AdminSitePlus()
admin.autodiscover()

# this was created for the sitemap
info_dict = {
    'queryset': Product.objects.all(),
    'date_field': 'pub_date',
}
makey_dict = {
    'queryset': Makey.objects.filter(is_enabled=True).filter(is_private=False),
    'date_field': 'pub_date',
}
space_dict = {
    'queryset': Space.objects.all().annotate(members_count=Count('members')).filter(members__in=users).order_by('-members_count'),
    'date_field': 'pub_date',
}

sitemaps = {
    # 'flatpages': FlatPageSitemap,
    'product': GenericSitemap(info_dict, priority=0.6),
    # 'makey': GenericSitemap(makey_dict, priority=0.6),
}
sitemap_makey = {
    # 'flatpages': FlatPageSitemap,
    # 'product': GenericSitemap(info_dict, priority=0.6),
    'makey': GenericSitemap(makey_dict, priority=0.6),
}

sitemap_space = {
    'space': GenericSitemap(space_dict, priority=0.6),
}

# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns(
    '',

    # Uptime
    url(r'^uptime/', apps.core.views.uptime_check),
    url(r'^hijack/', include('hijack.urls')),

    # #askbot
    # url(r'%s' % settings.ASKBOT_URL, include('askbot.urls')),

    # Admin panel and documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/social/login/cancelled/$', auth.login_cancelled),
    url(r'^accounts/social/login/error/$', auth.login_cancelled),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^', include('apps.catalog.urls', namespace='catalog')),
    url(r'^api/', include('apps.catalog.api_urls')),

    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}),
    url(r'^sitemap_makey\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemap_makey}),
    url(r'^sitemap_space\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemap_space}),
)
