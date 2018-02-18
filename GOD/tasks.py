from __future__ import absolute_import, unicode_literals
from celery import shared_task
from backend import get_info
from django.core.mail import send_mail
from GODEYE import settings
import json
import paramiko
from GOD import models
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


@shared_task

def gittask(job_id):
	gittask=models.TaskJob.objects.get(id=job_id).gittask
	git_bindhosts=list(gittask.bindhost.all().values())
	ssh=paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	for i in git_bindhosts:
		host_obj=models.BindHosts.objects.get(id=i['id'])
		host_ipaddr=host_obj.host.IPaddr
		host_username=host_obj.host_user.username
		host_password=host_obj.host_user.password
		print(host_obj,host_ipaddr)
		cmd_str=gittask.git_url
		print(cmd_str)
		
		
		try:
		  ssh.connect(hostname=host_ipaddr,username=host_username,password=host_password)
		  stdin,stdout,stderr=ssh.exec_command("git clone  %s"%cmd_str)
		  result=stdout.read() or stderr.read()
		  print(result.decode())
		except Exception as e:
			print(e)



