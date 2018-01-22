#coding=utf-8

"""
:param
处理用户的请求
"""
import os,sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CrazyEye.settings")
base_dir = '/'.join(os.path.abspath(os.path.dirname(__file__)).split("/")[:-1])
sys.path.append(base_dir)
import django
django.setup()
import subprocess
import sys
import paramiko
import multiprocessing
from GOD import models

#将命令处理结果写入到taskdetail中
def  cmd_eva(task_id,bind_hosts_id,cmd_str,port,user):
   
   
    print("---start---")
   
    bind_hosts=models.BindHosts.objects.get(id=bind_hosts_id)
    host_log=models.Taskdetail.objects.get(children_task_id=task_id,bind_host_id=bind_hosts_id)
    print(bind_hosts,host_log)
    
    password=bind_hosts.host_user.password
    hostname=bind_hosts.host.IPaddr
    print(password,hostname)
    print('heihie')
    SSHClient=paramiko.SSHClient()
    SSHClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
      SSHClient.connect(port=port,password=password,hostname=hostname)
      stdin, stdout, stderr=SSHClient.exec_command(cmd_str)
      result=stdout.read() or stderr.read()
      host_log.result="success"
      host_log.event_log=result.decode()
      host_log.save()
      SSHClient.close()
  
      print('----end----')
    except Exception as msg:
      print(msg)
      host_log.result="failed"
      host_log.event_log=msg
      host_log.save()
      print('----exception---',e)
    #写入数据库taskdetail
      
  


def upload_file(remote_path):
    pass

def download_file(remote_path):
    pass


#判断用户的输入的命令是否正确
if __name__=="__main__":
   print(sys.argv)

   """
	['/home/blyh/GODEYE/backend/tackle_task.py', '-tasktype', 'cmd', '-host', "['3', '4']", '-userid', '6', '-cmd_str', 'sss', '-taskid', '42']
   """

   #define the user input args
   require_args=['-tasktype','-host','-userid','-cmd_str','-taskid']
   print(sys.argv[1:])
   lack_args = [arg for arg in require_args if arg not in sys.argv[1:]]
   print(lack_args)
   if len(lack_args)>0:
       sys.exit("lack of args"%lack_args)
   
   task_type=sys.argv[sys.argv.index("-tasktype")+1]
   bind_hosts_id=sys.argv[sys.argv.index('-host')+1]
   cmd_str=sys.argv[sys.argv.index('-cmd_str')+1]
   userid=sys.argv[sys.argv.index('-userid')+1]
   taskid=sys.argv[sys.argv.index('-taskid')+1]
   task_list=[]
   if task_type=="cmd":
          cmd_exec=cmd_eva
   
   for i in bind_hosts_id.split(','):
           print(type(i))
           p=multiprocessing.Pool(processes=8)
           p.apply_async(cmd_exec,args=(taskid,i,cmd_str,22,userid,))
           
   
   p.close()
   p.join()
   
      
   










