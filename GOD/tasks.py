from __future__ import absolute_import, unicode_literals
from celery import shared_task
from backend import get_info
from django.core.mail import send_mail
from GODEYE import settings
import json

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

@shared_task
def sendemail(*args,**kwargs):
    '''
    subject, message, from_email, recipient_list,
              fail_silently=False, auth_user=None, auth_password=None,
              connection=None, html_message=None
    "email_content": "fewfadfadf",
    "email_subject": "dfwefwe", "email_to": "1064187559@qq.com"
    '''

    # kwargs=json.loads(kwargs)
    send_mail(kwargs['email_subject'],
              kwargs["email_content"],
              settings.DEFAULT_FROM_EMAIL,
              kwargs["email_to"].split(),
              fail_silently=False,
              )


