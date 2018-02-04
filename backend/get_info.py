#coding=utf-8

import paramiko

# import paramiko
# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect('10.10.50.30', 22, 'root', '123456')
# stdin, stdout, stderr = ssh.exec_command('ifconfig')
# print stdout.read()

def SSH_CON_Info(ip,port,username,password):
    SSH_Client=paramiko.SSHClient()
    SSH_Client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(ip,username,password)
    SSH_Client.connect(hostname=ip,port=port,username=username,password=password)

    cmd_exe1 = "free -m | awk 'NR==2' |awk '{print ($2-$4-$6)/$2}'"
    cmd_exe="cat /proc/stat |awk 'NR==1' |awk '{var1=($2+$3+$4);print var1/(var1+$5)}'" \
            "&&%s"%cmd_exe1
    print(cmd_exe)
    stdin, stdout, stderr = SSH_Client.exec_command(cmd_exe)



    ret=stdout or stderr
    if ret:
        tackle_data=ret.read().decode()
        cpu=tackle_data.split('\n')[0]
        mem=tackle_data.split('\n')[1]
        zai={'cpu':float(cpu),'mem':float(mem)}

    return zai

# #
# a=SSH_CON_Info(ip="192.168.31.162",port=22,username='root',password="admin")
# print(a)



