from __future__ import absolute_import, unicode_literals
from celery import shared_task
from backend import get_info

@shared_task #可以让其他的view视图调用
def add(x, y):
 return x + y


@shared_task
def mul(x, y):
 return x * y


@shared_task
def xsum(numbers):
 return sum(numbers)

@shared_task
def get_something(ip,port,username,password):
    try:
        ret_val=get_info.SSH_CON_Info(ip=ip,port=port,username="root",password=password,)


    except:
        ret_val=0

    return ret_val