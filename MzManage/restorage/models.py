from django.db import models
from django.contrib.auth.hashers import (check_password,
                                        make_password)

# Create your models here.

class UserType(models.Model):
    caption = models.CharField(max_length=32,db_index=True,unique=True)
    code = models.CharField(max_length=32,db_index=True,unique=True)

    def __str__(self):
        return self.caption

    class Meta:
        verbose_name_plural = "用户类型"

class Permission:
    CMDB = 1
    FORTRESS = 2
    ADMINISTER = 16

class Role(models.Model):
    name = models.CharField(max_length=32,unique=True)
    default  = models.BooleanField(default=False,db_index=True)
    permissions = models.IntegerField()
    @staticmethod
    def insert_roles():
        roles={
            'User':[Permission.FORTRESS],
            'Ops':[Permission.CMDB,
                  Permission.FORTRESS],
            'Admin':[Permission.ADMINISTER]
        }
        default_role = 'User'
        for r in roles:
            try:
                role = Role.objects.filter(name=r).first()
                if role is None:
                    role = Role(name=r)
                    role.reset_permissions()
                    for perm in roles[r]:
                        role.add_permission(perm)
                    role.default = (role.name == default_role)
                    role.save()
            except Exception as e:
                print("error",e)
    def has_permission(self,perm):
        return self.permissions & perm == perm

    def add_permission(self,perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self,perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "用户角色"

class Department(models.Model):
    name = models.CharField(max_length=32,unique=True,db_index=True)
    moment = models.CharField(max_length=128,null=True,blank=True)
    #定义部门字段连接用户表
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "部门"
class User(models.Model):
    email = models.EmailField(max_length=32,unique=True,db_index=True)
    uesername = models.CharField(max_length=32,unique=True)
    password_hash = models.CharField(max_length=128,blank=True)
    authed =   models.BooleanField(default=False)
    role = models.ForeignKey(Role,blank=True,on_delete=models.CASCADE)
    dept = models.ForeignKey(Department,blank=True,on_delete=models.CASCADE)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = make_password(password)

    def verify_password(self,password):
        return check_password(password,self.password_hash)

    def can(self,permissions):
        return self.role is not None and \
                (self.role.permissions & permissions) ==permissions
    def is_admin(self):
        return self.can(Permission.ADMINISTER)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "用户表"
