from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin
)

from django.utils.safestring import mark_safe
# Create your models here.


# class hostUser(models.Model):
#     '''主机系统用户，共用一套'''
#     username=models.CharField(max_length=64)
#     password=models.CharField(max_length=64)
#     def __str__(self):
#         return self.username
#     class Meta:
#         unique_together=('username','password')

class HostUser(models.Model):
    """主机登录账户"""
    auth_type_choices = ((0,'ssh-password'),(1,'ssh-key'))
    auth_type = models.SmallIntegerField(choices=auth_type_choices,default=0)
    username = models.CharField(max_length=64,verbose_name="主机用户名")
    password = models.CharField(max_length=128,blank=True,null=True)
    def __str__(self):
        return "%s:%s" %(self.username,self.password)
    class Meta:
        unique_together = ('auth_type','username','password')
        verbose_name="主机账户表"
        verbose_name_plural="主机账户表"

class Host(models.Model):
    '''主机'''
    IPaddr=models.GenericIPAddressField(unique=True,null=False,blank=False)
    Hostname=models.CharField(max_length=64)
    port = models.PositiveIntegerField(default=22)
    idc = models.ForeignKey("IDC",on_delete=models.DO_NOTHING)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return "%s(%s)" % (self.Hostname, self.IPaddr)

    class Meta:
        verbose_name="主机表"
        verbose_name_plural="主机表"



class IDC(models.Model):
        """机房信息"""
        name = models.CharField(max_length=64, unique=True)

        def __str__(self):
            return self.name

        class Meta:
            verbose_name = "机房表"
            verbose_name_plural = "机房表"


class BindHosts(models.Model):
    '''形成最小的权限'''
    host_user=models.ForeignKey('HostUser',null=False,on_delete=models.DO_NOTHING)
    host=models.ForeignKey('Host',on_delete=models.DO_NOTHING)


    def __str__(self):
        return "%s@%s"%(self.host_user,self.host)
    class Meta:
        unique_together=('host_user','host')
        verbose_name="主机和用户表"
        verbose_name_plural="主机和用户表"



class HostGroups(models.Model):
    '''主机组'''
    Group_name=models.CharField(max_length=64,unique=True)
    bind_hosts=models.ManyToManyField('BindHosts',null=True,blank=True)

    def __str__(self):
        return self.Group_name
    class Meta:
        verbose_name="主机组表"
        verbose_name_plural="主机组表"

class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        self.is_active = True

        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        self.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser,PermissionsMixin):
    '''堡垒机用户'''
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    password = models.CharField(('password'), max_length=128,help_text=mark_safe('''<a href="password/">重置密码</a>'''))# 重写继承类的pasword
    name = models.CharField(max_length=32)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()

    # group_host=models.ManyToManyField('HostGroups')
    # bind_host=models.ManyToManyField('BindHosts')
    group_host=models.ManyToManyField('HostGroups',blank=True)
    bind_host=models.ManyToManyField('BindHosts',blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    def __str__(self):
         return self.name
    class Meta:
        verbose_name="用户表"
        verbose_name_plural="用户表"

#堡垒机用户从后台登录后得到的日志信息
class UserLog(models.Model):
    name=models.CharField(max_length=128)
    user=models.ForeignKey('UserProfile',on_delete=models.DO_NOTHING)
    bindhost=models.ForeignKey('BindHosts',on_delete=models.DO_NOTHING)
    logtime=models.DateTimeField(auto_now_add=True)


#定义一个tasklog,前台用户记录相关的日志 信息

class TaskLog(models.Model):
    tag_name=models.CharField(max_length=128,blank=True,null=True)
    user=models.ForeignKey("UserProfile",on_delete=models.DO_NOTHING)
    cmd_str=models.CharField(max_length=1024)
    task_pid=models.IntegerField(default=0)
    task_time=models.DateTimeField(auto_now_add=True)
    task_type_choices = (('cmd', "CMD"), ('file_send', "批量发送文件"), ('file_get', "批量下载文件"))
    task_type = models.CharField(choices=task_type_choices, max_length=50)
    host_list = models.ManyToManyField('BindHosts')

    def __str__(self):
        return "%s:%s" %(self.id,self.tag_name)
    class Meta:
        verbose_name_plural="任务日志"
        verbose_name="任务日志"


class Taskdetail(models.Model):
    children_task=models.ForeignKey("TaskLog")
    result_choices= (('success','Success'),('failed','Failed'),('unknown','Unknown'))
    result = models.CharField(choices=result_choices,max_length=30,default='unknown')
    date=models.DateTimeField(auto_now_add=True)
    event_log=models.TextField()
    bind_host=models.ForeignKey('BindHosts',on_delete=models.DO_NOTHING)
    def __str__(self):
       return "child of:%s result:%s" %(self.children_task.id, self.result)


    class Meta:
        verbose_name_plural = "任务详细"
        verbose_name = "任务详细"


