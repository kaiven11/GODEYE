#coding=utf-8

"""
:param
处理用户的请求
"""
import os,sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GODEYE.settings")
base_dir = '/'.join(os.path.abspath(os.path.dirname(__file__)).split("/")[:-1])
sys.path.append(base_dir)
import django
django.setup()
import subprocess
import sys
import paramiko
import multiprocessing
from GOD import models
from backend import  muilti_task



def decrator(func):
        print("decorator")

        def wrapper(*args,**kwargs):

            print("just for test!")


            if type=="file_upload":
                return func(*args)
            if type=="file_donwload":
                pass
            return  wrapper





#将命令处理结果写入到taskdetail中
def  cmd_eva(task_id,bind_hosts_id,cmd_str,port,user,local_file_path,remote_path):
    '''

    :param task_id:
    :param bind_hosts_id:
    :param cmd_str:
    :param port:
    :param user:
    :param local_file_path:
    :param remote_path:
    :return:
    '''
   
    print("---start---")
   
    bind_hosts=models.BindHosts.objects.get(id=bind_hosts_id)
    host_log=models.Taskdetail.objects.get(children_task_id=task_id,bind_host_id=bind_hosts_id,)
    print(bind_hosts,host_log)
    
    password=bind_hosts.host_user.password
    hostname=bind_hosts.host.IPaddr
    print(password,hostname)
    print('heihie')
    SSHClient=paramiko.SSHClient()
    SSHClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
      SSHClient.connect(port=port,password=password,hostname=hostname,timeout=5)
      stdin, stdout, stderr=SSHClient.exec_command(cmd_str)
      result=stdout.read() or stderr.read()
      host_log.result="success"
      host_log.event_log=result.decode()
      host_log.save()
      SSHClient.close()
  
      print('----end----')
    except Exception as e:
      print(e)
      host_log.result="failed"
      host_log.event_log=e
      host_log.save()
      print('----exception---',e)
    #写入数据库taskdetail

#全局的type字段


# @file_type(type_str=muilti_task.type_file)
@decrator
def upload_file(taskid,bindhostid,cmd_str,port,userid,local_file_path,remote_path,):

    host_obj = models.BindHosts.objects.get(id=bindhostid)
    print(host_obj, "主机")
    username = host_obj.host_user.username
    password = host_obj.host_user.password
    port = host_obj.host.port
    ipaddr = host_obj.host.IPaddr

    print(os.path.basename(local_file_path))

    filename = os.path.basename(local_file_path)
    print(local_file_path, os.path.join(remote_path, filename))
    transport = paramiko.Transport((ipaddr, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(local_file_path,remote_path+"%s%s"%(r"/",filename))
    sftp.close()
    print("sendfile_ok!")
    # 写入日志信息
    host_log = models.Taskdetail.objects.get(children_task_id=taskid, bind_host_id=bind_hosts_id,)
    host_log.event_log="%s send to %s completed!"%(filename,ipaddr)









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
   # if len(lack_args)>0:
   #     sys.exit("lack of args"%lack_args)
   
   task_type=sys.argv[sys.argv.index("-tasktype")+1]
   bind_hosts_id=sys.argv[sys.argv.index('-host')+1]
   cmd_str=sys.argv[sys.argv.index('-cmd_str')+1]
   userid=sys.argv[sys.argv.index('-userid')+1]
   taskid=sys.argv[sys.argv.index('-taskid')+1]
   taskid=sys.argv[sys.argv.index('-taskid')+1]

   if task_type=="cmd":

       cmd_exec=cmd_eva
   if task_type=="file_upload":
       cmd_exec=upload_file
       remote_path = sys.argv[sys.argv.index('-remote_path')+1]
       local_file_path=sys.argv[sys.argv.index('-local_file_path')+1]
   for i in bind_hosts_id.split(','):
           print(i)
           p=multiprocessing.Pool(processes=8)
           p.apply_async(cmd_exec,args=(taskid,i,cmd_str,22,userid,local_file_path,remote_path))
           
   
   p.close()
   p.join()
   
      
   










