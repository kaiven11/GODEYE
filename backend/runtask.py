#coding=utf-8
import os,sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GODEYE.settings")
base_dir = '/'.join(os.path.abspath(os.path.dirname(__file__)).split("/")[:-1])
sys.path.append(base_dir)
import django
django.setup()
from GOD import models
from backend import exec_tasks

class exec_task():
    plan_dict = {} #类变量
    zhong_dic={}
    def __init__(self, plan_id):
        self.plan_id = plan_id
        self.stage=None
        self.job=None

    def wrapper(func):
        def decrator(self):
            print("Current_process is %s" %(self.job))
            return func(self)
        return decrator

    @wrapper
    def run(self):
        self.ordered_stage(planid=self.plan_id)

        self.zhong_dic.update({self.plan_id:self.plan_dict})
        for k,v in self.zhong_dic.items():
            for j,z in v.items():
                self.stage = j
                if z:
                    for m in z:
                        self.job = m
                        print('this is m',m)
                        self.GetType(m)


    @classmethod
    def GetType(cls,args):
       print(args['task_type'])
       if args.get("task_type")==0:
	       exec_tasks.exec_ssh(args)
       elif args.get("task_type")==2:
		    
               print('haha')
               exec_tasks.exec_git(args)
    @classmethod
    def ordered_stage(cls, planid):
        '''

        :return:{stage1:{job1,job2},stage2:{job1,job2}}
        In [22]: list(a.taskstage_set.order_by('id').values())
Out[22]:
stage:
[{'id': 1, 'stagename': 'stage1', 'taskplan_id': 1},
 {'id': 5, 'stagename': 'stage2', 'taskplan_id': 1},
 {'id': 6, 'stagename': 'stage3', 'taskplan_id': 1},
 {'id': 7, 'stagename': 'stage4', 'taskplan_id': 1}]

job:
[{'id': 1, 'task_type': 0, 'taskstage_id': 1},
 {'id': 2, 'task_type': 2, 'taskstage_id': 1},
 {'id': 3, 'task_type': 1, 'taskstage_id': 1}]

{planid:{stage1:[job1,job2,job3]},{stage2:[job1,job2,job3]}}最终生成的数据结构

或者这里可以用链表来操作。

        '''

        _plan=models.TaskPlan.objects.get(id=planid)
        _stages=_plan.taskstage_set.select_related().order_by("id")
        print(_stages)
        for item in _stages:
            cls.order_jobs(item)
        return cls.plan_dict

    @classmethod
    def order_jobs(cls,stage):
        print(stage.id,'sdfasdfads')

        _jobs = list(stage.taskjob_set.all().values())

        return cls.plan_dict.update({stage.id:_jobs})





    @property
    def current_process(self):
        return  "%s:%s" %(self.stage,self.job)
