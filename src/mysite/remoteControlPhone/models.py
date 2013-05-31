from django.db import models
from django.contrib.auth.models import User

class Device(models.Model):
    uniqueID = models.CharField(max_length=1000)
    type = models.CharField(max_length=1000)
    model = models.CharField(max_length=1000)
    date_created = models.CharField(max_length=1000)

    def __unicode__(self):
        return "uniqueID:" + self.uniqueID + ", date_created:" + str(self.date_created)

class UserDevice(models.Model):
    user = models.ForeignKey(User)
    device = models.ForeignKey(Device)
    date_created = models.CharField(max_length=1000)

    def __unicode__(self):
        return "user:" + self.user.username  + ";" + "device:" + self.device.uniqueID + ";" + ", date_created:" + str(self.date_created)

class Contacts(models.Model):
    device = models.ForeignKey(Device)
    name = models.CharField(max_length=1000)
    phone_No = models.CharField(max_length=1000)
    date_created = models.CharField(max_length=1000)
    
    def __unicode__(self):
        return "device:" + self.device.uniqueID  + ";" + "Name:" + self.name + ";" + "Phone_No:" + self.phone_No + ", date_created:" + str(self.date_created)

class CallLogs(models.Model):
    device = models.ForeignKey(Device)
    type = models.CharField(max_length=1000)
    date = models.CharField(max_length=1000)
    duration = models.CharField(max_length=1000)
    number = models.CharField(max_length=1000)
    date_created = models.CharField(max_length=1000)
    
    def __unicode__(self):
        return "device:" + self.device.uniqueID  + ";" + "type:" + self.type + ";" + "date:" + self.date  + ";" + "duration:" + self.duration + ";" + "number:" + self.number + ", date_created:" + str(self.date_created)
    
class PushRegistration(models.Model):
    device = models.ForeignKey(Device)
    regId = models.CharField(max_length=1000)
    date_created = models.CharField(max_length=1000)

    def __unicode__(self):
        return "device:" + self.device.uniqueID + ";" + "regId:" + self.regId + ", date_created:" + str(self.date_created)