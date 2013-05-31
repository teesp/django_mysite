from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout

from remoteControlPhone import views

urlpatterns = patterns('',
    url(r'^hello/$', views.hello),
    
    url(r'^accounts/login/$',  login),
    url(r'^accounts/logout/$', logout),
    
    url(r'^accounts/register_forMobile/$', views.register_forMobile),
    url(r'^accounts/login_forMobile/$', views.login_forMobile),
    
    url(r'^push_fromMobile/calllogs/$', views.push_forMobile_calllogs),
    url(r'^get_fromJS/calllogs/$', views.getCallLogs_fromJS),
    

    url(r'^$', views.deviceList),
    url(r'^device/(\w+)/$', views.device),
)