# Create your views here.
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
import json as jason
from gcm import GCM
import pdb; 

from django.contrib.auth.models import User
from remoteControlPhone.models import Device
from remoteControlPhone.models import UserDevice
from remoteControlPhone.models import Contacts
from remoteControlPhone.models import CallLogs
from remoteControlPhone.models import PushRegistration
from django.contrib import auth
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.template import Context, loader
from django.contrib.auth import authenticate, login

import urllib2
from django.utils import timezone

import datetime
import time
import json

SERVER_KEY = "AIzaSyCtc9HzCbao7tQiEt7Ms_yau4KITHTycBo"


#{
#"username":"testAccount",
#"password1":"mac8.6",
#"password2":"mac8.6",
#"uniqueID":"1234567890"
#}
def register_forMobile(request):
    if request.method == 'POST':
        try:
            dataStr = request.body
            dataObj = jason.loads(dataStr)
            
            username = dataObj['username']
            password1 = dataObj['password1']
            password2 = dataObj['password2']
            uniqueID = dataObj['uniqueID']
            type = dataObj['type']
            model = dataObj['model']
            
            if not username or not password1 or not password2 or not uniqueID or not password1 == password2:
                return ReturnParamError()
            num_results = User.objects.filter(username = username).count()
            if num_results is not 0:
                return ReturnRegisterMobileUserExisted()
            
    #       register user
            user = User.objects.create_user(username, 'test@mail.com', password1)
    #       register device
            addDevice(username, uniqueID, type, model)
            return ReturnOK()
        except:
            return ReturnRegisterMobileException()
    return ReturnRegisterMobileError()

def getCurrentUnixTimeStamp():
    return time.time()

def addDevice(username, guid, type, model):
    devices = Device.objects.filter(uniqueID=guid)
    if devices:
        devices.delete()
        
    _Device = Device(uniqueID=guid, type=type, model=model, date_created=getCurrentUnixTimeStamp())
    _Device.save()
        
    userDevices = UserDevice.objects.filter(device__uniqueID=guid)
    if userDevices:
        userDevices.delete()
        
    _UserDevice = UserDevice(user=User.objects.get(username=username), device=Device.objects.get(uniqueID=guid), date_created=getCurrentUnixTimeStamp())
    _UserDevice.save()

def login_forMobile(request):
#    pdb.set_trace()
    if request.method == 'POST':
        try:
            dataStr = request.body
            dataObj = jason.loads(dataStr)
            
            username = dataObj['username']
            password = dataObj['password']
            uniqueID = dataObj['uniqueID']
            type = dataObj['type']
            model = dataObj['model']
            
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                # Correct password                                    
                addDevice(username, uniqueID, type, model)
                return ReturnOK()
            else:
                return ReturnLogInMobileWrongAccount()
        except:
            return ReturnLogInMobileException()
    else:
        return ReturnLogInMobileError()
    
def hello(request):
    return HttpResponse("Hello world")
    
def deviceList(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/remoteControlPhone/accounts/login')
    
    userDevices = UserDevice.objects.filter(user=User.objects.get(username=request.user.username))
#    calllogs_list = []
#    for userDevice in userDevices:
#        calllogs = CallLogs.objects.filter(device=Device.objects.get(uniqueID=userDevice.device.uniqueID))
#        calllogs_list.append(calllogs)
        
    if len(userDevices) == 0:
        return HttpResponse("No device")
    else:
        return render_to_response('remoteControlPhone/deviceList.html', {'user' : request.user, 'userDevices': userDevices})

def device(request, uniqueID):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/remoteControlPhone/accounts/login')
    
    try:
        userDevices = UserDevice.objects.filter(user=User.objects.get(username=request.user.username), device=Device.objects.get(uniqueID=uniqueID))
    except:
        return ReturnDeviceNotMatchYou()
    
    if len(userDevices) == 0:
        return ReturnDeviceNotMatchYou()

    calllogs = CallLogs.objects.filter(device=Device.objects.get(uniqueID=uniqueID))
    
    response = render_to_response('remoteControlPhone/device.html', {'user' : request.user, 'userDevice': userDevices[0], 'calllogs': calllogs})
    response.set_cookie('username', request.user.username)
    response.set_cookie('uniqueID', userDevices[0].device.uniqueID) 
    return response

def getCallLogs_fromJS(request):
    uniqueID = request.COOKIES.get('uniqueID')
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/remoteControlPhone/accounts/login')
    
    try:
        userDevices = UserDevice.objects.filter(user=User.objects.get(username=request.user.username), device=Device.objects.get(uniqueID=uniqueID))
    except:
        return ReturnDeviceNotMatchYou()
    
    if len(userDevices) == 0:
        return ReturnDeviceNotMatchYou()
    
    calllogs = CallLogs.objects.filter(device=Device.objects.get(uniqueID=uniqueID))
    strList = []
    for item in calllogs:
        strObj = {}
        strObj["date_created"] = item.date_created;
        strObj["type"] = item.type;
        strObj["date"] = item.date;
        strObj["duration"] = item.duration;
        strObj["number"] = item.number;
        strList.append(strObj)
    return HttpResponse(jason.dumps(strList))

def push_forMobile_calllogs(request):
#    pdb.set_trace()
    if request.method == 'POST':
        try:
            dataStr = request.body
            dataObj = jason.loads(dataStr)
            
#            check whether this device exists in current database
            guid = dataObj['uniqueID']
            
            _device = Device.objects.filter(uniqueID=guid)
            if not _device:
                return ReturnPushFromMobileCallLogsDontHaveThisDevice()
                
            previousCallLogs = CallLogs.objects.filter(device__uniqueID=guid)
            if previousCallLogs:
                previousCallLogs.delete()
            
            for callLog in dataObj['callLogs']:
                type = callLog['type']
                date = callLog['date']
                duration = callLog['duration']
                number = callLog['number']
                
                _callLog = CallLogs(device=Device.objects.get(uniqueID=guid), type=type, date=date, duration=duration, number=number, date_created=getCurrentUnixTimeStamp())
                _callLog.save()
                       
            return ReturnOK()
        except:
            return ReturnPushFromMobileCallLogsException()
    else:
        return ReturnPushFromMobileCallLogsException()
       
#    return content
def ReturnOK():
    return HttpResponse(jason.dumps({'ReturnCode': "200", 'Desc': "OK"}))

def ReturnCommonError():
    return HttpResponse(jason.dumps({'ReturnCode': "90000000", 'Desc': "CommonError"}))

def ReturnParamError():
    return HttpResponse(jason.dumps({'ReturnCode': "90000001", 'Desc': "ParamError"}))

def ReturnAccountError():
    return HttpResponse(jason.dumps({'ReturnCode': "90000002", 'Desc': "AccountError"}))

def ReturnLogInMobileError():
    return HttpResponse(jason.dumps({'ReturnCode': "90010000", 'Desc': "LogInMobileError"}))

def ReturnLogInMobileWrongAccount():
    return HttpResponse(jason.dumps({'ReturnCode': "90010001", 'Desc': "LogInMobileWrongAccount"}))

def ReturnLogInMobileException():
    return HttpResponse(jason.dumps({'ReturnCode': "90010002", 'Desc': "LogInMobileException"}))

def ReturnRegisterMobileError():
    return HttpResponse(jason.dumps({'ReturnCode': "90020000", 'Desc': "RegisterMobileError"}))

def ReturnRegisterMobileUserExisted():
    return HttpResponse(jason.dumps({'ReturnCode': "90020001", 'Desc': "RegisterMobileUserExisted"}))

def ReturnRegisterMobileException():
    return HttpResponse(jason.dumps({'ReturnCode': "90020002", 'Desc': "RegisterMobileUserException"}))

def ReturnDeviceNotMatchYou():
    return HttpResponse(jason.dumps({'ReturnCode': "90030002", 'Desc': "DeviceNotMatchYou"}))

def ReturnPushFromMobileCallLogsException():
    return HttpResponse(jason.dumps({'ReturnCode': "90040000", 'Desc': "ReturnPushFromMobileCallLogsException"}))

def ReturnPushFromMobileCallLogsDontHaveThisDevice():
    return HttpResponse(jason.dumps({'ReturnCode': "90040001", 'Desc': "ReturnPushFromMobileCallLogsDontHaveThisDevice"}))