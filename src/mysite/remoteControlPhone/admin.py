from remoteControlPhone.models import Device
from remoteControlPhone.models import UserDevice
from remoteControlPhone.models import Contacts
from remoteControlPhone.models import CallLogs
from remoteControlPhone.models import PushRegistration
from remoteControlPhone.models import Messages


from django.contrib import admin
from django.contrib.auth.models import User

admin.site.register(Device)
admin.site.register(UserDevice)
admin.site.register(Contacts)
admin.site.register(CallLogs)
admin.site.register(PushRegistration)
admin.site.register(Messages)

if User.objects.count() == 0:
    admin = User.objects.create_user('dollar_zhang', 'leinakesi@gmail.com', 'mac8.6')
    admin.is_superuser = True
    admin.is_staff = True
    admin.save()