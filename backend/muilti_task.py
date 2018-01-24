#coding=utf-8
"""
:param -tasktype
此类用来让判断用户的task
分发器模式
"""
from . import global_settings
#from backend import tackle_task
# from django.conf import settings
from GODEYE import settings
import  os
import subprocess
from GOD import models

class Muiltiple_task():
    def __init__(self,tasktype,request_info):
        self.tasktype=tasktype
        self.request=request_info
        # self.parase_type(self.tasktype)

    def parase_type(self,type):
        type_obj=None
        if self.tasktype=="cmd":
            print("cmdtask")
            type_obj=getattr(self,"run_cmd")

        elif self.tasktype=="file_upload":
            type_obj=getattr(self,"file_upload")
        else:
            type_obj=getattr(self,"file_donwload")
        return type_obj

    def run(self):
        a=self.parase_type(self.tasktype)
        return a()



    def run_cmd(self):
        #获取相关的参数，调用具体的任务执行
        '''
         :param cmd,hostlist,去重工作，后台验证数据是否正确工作

        :return:
        '''
        print("there")
        cmd=self.request.POST.get('cmd')
        print(cmd)
        #assert cmd
        # hostgroup=self.request.POST.get("group")
        hostselected=self.request.POST.getlist("selected_host")#这里暂时处理前端提交的未分组的机器
        print(hostselected,type(hostselected))
        #hostselected_str=[",".join(i) for i in hostselected]
        #print(hostselected_str)
        # if hostgroup:
        #     models.get(group).valuelist()
        # if hostselected:
        #     modles.get(hostselected)
        #
        # 去重
        # 调用 subprocess.run(script,cmd,hostselected)
        #
        # 得到pid，用于处理结束时的任务
        #约定参数  -tasktype,host,
        #创建任务日志

        task_obj=models.TaskLog.objects.create(tag_name="a",user=self.request.user,task_type=self.tasktype,cmd_str=cmd)
        if task_obj:
           print("sucess")
           task_obj.host_list.add(*hostselected)
           print(task_obj.host_list.all())
        
        p=subprocess.Popen(["python",settings.TACKLE_SCRIPTS,"-tasktype",self.tasktype,
                          "-host",','.join(hostselected),
                          "-userid",str(self.request.user.id),
                          "-cmd_str",cmd,
                          "-taskid",str(task_obj.id),
                          ],)#设置一个进程组，方便后期结束整个任务

        pid=p.pid
        task_obj.task_pid=pid
        print(task_obj.id)
        task_obj.save()
        
        #write the "taskdetail" log 
        for i in hostselected:
           

            models.Taskdetail.objects.create(children_task_id=task_obj.id,result="unknow",event_log='',bind_host_id=i)
       	
        return task_obj.id










    def file_upload(self):
        print(self.request.POST.get("remote_value"))
        remote_path=self.request.POST.get("remote_value")
        local_file_name=str(self.request.FILES['file'])
        local_file_path=os.path.join(settings.UPLOAD_DIRS,local_file_name)
        print(remote_path,local_file_path)
        hostselected=self.request.POST.get('selected_host')
        hostselected=hostselected.split(',')
        print(hostselected)
        #创建日志
        task_obj=models.TaskLog.objects.create(
                                      tag_name=self.tasktype,
                                      user=self.request.user,
                                      task_type="file_send",
                                      remote_path=remote_path,

                                      )

        p = subprocess.Popen(["python", settings.TACKLE_SCRIPTS, "-tasktype", self.tasktype,
                              "-host", ','.join(hostselected),
                              "-userid", str(self.request.user.id),
                              "-taskid", str(task_obj.id),
                              "-cmd_str","",
                              "-remote_path",remote_path,
                              "-local_file_path",local_file_path
                              ])  # 设置一个进程组，方便后期结束整个任务

        pid = p.pid
        task_obj.task_pid = pid
        task_obj.save()

        return None
    def file_donwload(self):
        pass



# a.run("df")
# a=Muiltiple_task("cmd",request_info="a")
