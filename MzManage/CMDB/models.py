from django.db import models
import datetime

# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=64)
    memo = models.TextField(u'备注',null=True,blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "状态"

class DeviceType(models.Model):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=64)
    memo = models.CharField(max_length=256,null=True,blank=True)
    #是否为虚拟设备（虚拟机/云主机）
    virdev = models.BooleanField(default=False)
    create_at = models.DateTimeField(blank=True,auto_now_add=True)
    update_at = models.DateTimeField(blank=True,auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "设备类型"

class IDC(models.Model):
    name = models.CharField(max_length=128)
    region = models.CharField(u'区域',max_length=64)
    floor = models.IntegerField(u'楼层',default=1)

class Asset(models.Model):
    #deviceType = models.ForeignKey("DeviceType")
    #deviceStatus = models.ForeignKey("Status")
    pass

