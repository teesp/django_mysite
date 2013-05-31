from django.conf.urls import patterns, url

from foo import views

urlpatterns = patterns('',
    url(r'^hello/$', views.hello),
    url('^time/$', views.current_datetime),
    url(r'^time/plus/(\d{1,2})/$', views.hours_ahead),
    url(r'^display_meta/$', views.display_meta),
    url(r'^search/$', views.search),
    url(r'^contact/thanks/$', views.contact_thanks),
    url(r'^contact/$', views.contact),
    url(r'^$', views.index),
)