from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from apps.myapp import views

urlpatterns = patterns('',
	url(r'^$', views.land, name='land'),
    #url(r'^tangle/$', views.tangle, name='tangle'),
	url(r'^land/$', views.land, name='land'),
	
	#url(r'^newdesign/$', views.newdesign, name='newdesign')
	)

urlpatterns += staticfiles_urlpatterns()
