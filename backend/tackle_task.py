#coding=utf-8

"""
:param
处理用户的请求
"""
import sys
import paramiko
import multiprocessing
from GOD import models
#将命令处理结果写入到taskdetail中
def  cmd_eva(bind_hosts,cmd_str,passwd,port):
    SSHClient=paramiko.SSHClient()
    SSHClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    SSHClient.connect(port=port,password=passwd,hostname=bind_hosts)
    stdin, stdout, stderr=SSHClient.exec_command(cmd_str)
    result=stdout.read() or stderr.read()
    #写入数据库taskdetail
    return result.decode()


def upload_file(remote_path):
    pass

def download_file(remote_path):
    pass


#判断用户的输入的命令是否正确
if __name__=="__main__":
   p=multiprocessing.Pool()

