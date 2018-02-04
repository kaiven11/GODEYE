#coding=utf-8

from django.contrib.auth import authenticate
import getpass
import os
import subprocess

#验证堡垒机用户
'''
用django自带的验证方法
'''
#linux执行此程序
#记录日志


def authen():
    #验证用户
    user=None
    while True:
        username=input("input your email：").strip()
        if len(username)==0:continue
        passwd=getpass.getpass("input your password:")
        if len(passwd)==0:continue
        user=authenticate(username=username,password=passwd)
        if user:
            print("验证成功！")
            break

    #显示用户可用的主机组或者主机
    exit_flag=True
    back_flag=True
    while exit_flag:

    # 1.主机组
        selected_all=user.group_host.all()
        print(selected_all)
        for index,group_name in enumerate(selected_all):
            print("%s %s"%(index,group_name))

        print("%s Undefined Group" %(index+1))


        group_num=input("select your group number:").strip()
        if len(group_num)==0:continue
        group_num = int(group_num)
        #判断输入的数字等于用户绑定的组，表明他选择的是未分组的主机
        if group_num==selected_all.count():
            selected_all=user.bind_host.all()
            for loop,bd_host in enumerate(selected_all):
                print("%s %s"%(loop,bd_host))
            selected_all = user.group_host.all()

        else:

            try:
                selected_group_list=selected_all[group_num].bind_hosts.all()
            except:
                continue
            for index,host_name in enumerate(selected_group_list):
                print("%s %s"%(index,host_name))

        
        #开始选取主机
        host_num=input("select host :").strip()
        if len(host_num)==0:continue
        host_num=int(host_num)
        if group_num==selected_all.count():

            host_obj=user.bind_host.all()[host_num]
        else:
            host_obj=selected_group_list[host_num]
        host_ip=host_obj.host_user.username+'@'+host_obj.host.IPaddr
        print("the host_obj is %s" %host_ip)
        #启动一个进程来监测用户登陆后的ID，并进行记录



        import time
        import hashlib
        md5_str=hashlib.md5(str(time.time()).encode()).hexdigest()
        log_cmd="./backend/session_tracker.sh %s %s" %(md5_str,settings.WORKDIR)
        #out_pipe=subprocess.Popen("%s %s" %("./backend/session_tracker.sh",md5_str),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=settings.BASE_DIR)       

        out_pipe=subprocess.Popen(log_cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=settings.BASE_DIR)       
        if  not out_pipe.stderr.read():
            models.UserLog.objects.create(name=md5_str,user=user,bindhost=host_obj)
        #print(out_pipe.stdout.read(),out_pipe.stderr.read())         
        #md5_str=hashlib.md5(str(time.time()).encode()).hexdigest()
        #正式进行linux环境 
        subprocess.run("sshpass -p admin /usr/local/openssh/bin/ssh -Z %s  %s  -o StrictHostKeyChecking=no" %(md5_str,host_ip),shell=True)
        print(out_pipe.stdout.read(),out_pipe.stderr.read())         
        print('------------logout----------------')






    



















    #显示用户可以用的主机组或者主机

















if __name__=="__main__":
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GODEYE.settings")
    # import django
    # django.setup()

    '''
    下面几句需要提前引入django环境
    '''
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GODEYE.settings")
    import django
    django.setup()
    from django.conf import settings
    from GOD import models




    authen()

    #just for test
