#coding=utf-8


import os,sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GODEYE.settings")
base_dir = '/'.join(os.path.abspath(os.path.dirname(__file__)).split("/")[:-1])
sys.path.append(base_dir)
import django
django.setup()
import paramiko
from GOD import models
from GOD.tasks import gittask

def exec_ssh(args):
	print("yes,it is hrere")
	job_id=args['id']
	job_obj=models.TaskJob.objects.get(id=job_id)
	print(job_obj)
	sshtask=job_obj.sshtask
	print(sshtask)
	hostnames=list(sshtask.bindhosts.all().values())
	cmd_str=sshtask.exec_cmd
	print(cmd_str)
	ssh=paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	for i in hostnames:
		hostname=models.Host.objects.get(id=i['host_id']).IPaddr
		host_pass_obj=models.HostUser.objects.get(id=i['host_user_id'])
		host_username=host_pass_obj.username
		host_userpass=host_pass_obj.password
		print(hostname,host_userpass,host_username)
		try:

		  ssh.connect(hostname=hostname,password=host_userpass,username=host_username)

		  stdin,stdout,stderr=ssh.exec_command(cmd_str)
		  result=stdout.read() or stderr.read()
		  print(result.decode())
		  ssh.close()
		except Exception as e:
			print(e)
			continue



def exec_scp(args):
	pass


def exec_git(args):
	print('exec_gittask')
	job_id=args['id']
	gittask.delay(job_id)
	






def exec_pip(args):
	pass

