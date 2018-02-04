#coding=utf-8
from django.core.signals import request_started,request_finished

def callback(sender,**kwargs):
    print("我来了")


request_started.connect(callback)

def logout(sender,**kwargs):
    print("我走了")


request_finished.connect(logout)
