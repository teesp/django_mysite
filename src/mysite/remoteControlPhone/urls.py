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
    
    url(r'^push_fromMobile/contacts/$', views.push_forMobile_contacts),
    url(r'^get_fromJS/contacts/$', views.getContacts_fromJS),
    
    url(r'^push_fromMobile/messages/$', views.push_forMobile_messages),
    url(r'^get_fromJS/messages/$', views.getMessages_fromJS),

    url(r'^$', views.deviceList),
    url(r'^device/(\w+)/$', views.device),
    
    url(r'^registerChannel/$', views.registerChannel), 
    url(r'^pushRequest_fromJS/$', views.pushRequest_fromJS), 
)