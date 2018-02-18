from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from backend import muilti_task
from django_celery_beat import  models as celery_models
from backend import runtask
from django.dispatch import receiver
from django.core import signals
from channels import Group


from GOD import froms

from backend import get_info
import io
import json
import os
from GOD import models
from backend import generate_code
from django.core.cache import cache
from GODEYE import settings
import random
import string
from backend import dynamic_form
import paramiko
from GOD.tasks import get_something
# Create your views here.


def index(request):
    # print(settings.RANDOM_DIR)
    # img.save(os.path.join(settings.RANDOM_DIR,"%s.gif"%(random_file_name)))

    # cache.set(random_file_name,random_code,1)
    if request.method=="POST":
        # verify_key=request.POST.get('file_key')
        verifi_code=request.POST.get('verify_code')
        username=request.POST.get('email')
        pwd=request.POST.get('pwd')

        print(username,pwd)
        print(request.session.items())
        # print(cache.get(request.user.id),"have the  key")
        if verifi_code.upper()==request.session["CheckCode"].upper():
            print("yess")
            user=authenticate(request=request,username=username,password=pwd)
            if user is not None:
                print("user is not nonew")
                print(request.user)
                login(request,user)#写入session
                return redirect("/OverView")
            else:
                return redirect('/account/login')
        else:
            return  redirect('/account/login')

    if request.method=="GET":
        if request.user.is_authenticated():
            return redirect("/OverView")
        return render(request, "index.html")




def check_code(request):
    """
    获取验证码
    :param request:
    :return:
    """
    stream = io.BytesIO()
    # 创建随机字符 code
    # 创建一张图片格式的字符串，将随机字符串写到图片上
    img, code = generate_code.create_validate_code()
    img.save(stream, "PNG")
    # 将字符串形式的验证码放在Session中

    #将用户ID和验证码放入到缓存中
    #如果缓存中有数据，就删除，保证缓存中只有一个
    # if cache.get(request.user.id):
    #     cache.delete(request.user.id)
    # cache.set(request.user.id, code)会出现问题，多用户登录时会将前面用户顶掉
    request.session["CheckCode"] = code

    request.session["oo"]="test"

    # print(request.session['CheckCode'])
    return HttpResponse(stream.getvalue())

@login_required
#用户概览
def OverView(request):
    return render(request,'base.html')

@login_required
# @receiver(signals.request_finished)
def log_out(request):
    logout(request)
    return redirect('/account/login')


@login_required
#主机显示

def mange_host(request):
    host_list=models.BindHosts.objects.all()
    return  render(request,"hosts_manage.html",{'host_list':host_list})
@login_required

@login_required
#显示主机具体信息
def host_info(request,host_id):
    host_obj=models.Host.objects.get(id=host_id)
    if request.method=="GET":
        myform = dynamic_form.Create_Dynamic_Form(models.Host)
        form_obj=myform(instance=host_obj)



    return render(request,'host_detail.html',{'host_detail':form_obj,'host_obj':host_obj})



#h获取CPU信息
def get_cpu(request):
    print('yes')
    if request.is_ajax():
        if request.method=="GET":
            host_ip=request.GET.get("host_ip")
            host_port=request.GET.get("host_port")

            # models.BindHosts.objects.get(host__IPaddr=host_ip,host__bindhosts__host_user='root')
            user_obj=models.HostUser.objects.filter(bindhosts__host__IPaddr=host_ip,username="root")
            print(user_obj[0])

            haha=get_something.delay(ip=host_ip,port=host_port,username="root",password=user_obj[0].password,)

            #get host info
            # try:
            #     ret_val=get_info.SSH_CON_Info(ip=host_ip,port=host_port,username="root",password=user_obj[0].password,)
            #     print(ret_val)
            # except:
            #     ret_val=0




    return HttpResponse(json.dumps(haha.get()))



#针对用户提交的主机和命令批量执行
@login_required
@csrf_exempt
def muilt_cmd(request):
    #未分组主机

    ugroup_host=request.user.bind_host.all()
    print(ugroup_host,request.user)
    # if request.method=="GET":
    #     pass
    if request.is_ajax():

        if request.method=="POST":
            # selected_host=request.POST.getlist('selected_host')
            # cmd=request.POST.get("cmd")

            print("here")
            ret=muilti_task.Muiltiple_task("cmd",request)
            a=ret.run()
            print("ret---",a)
            
            return  HttpResponse(a)
        if request.method=="GET":
            task_id=request.GET.get('task_id')
            task_detal_queryset=models.TaskLog.objects.get(id=task_id).taskdetail_set.values('result')
            print(task_detal_queryset)

    return render(request,"host_task.html",{'ugroup_host':ugroup_host})

@login_required
@csrf_exempt
def file_upload(request):
    if request.is_ajax():
        if request.method == "POST":

            for k,v in request.FILES.items():
                #print(type(str(request.FILES['file'])))
                with open(os.path.join(settings.UPLOAD_DIRS,v.name),'wb') as e:
                    for chunk in v.chunks():
                        e.write(chunk)
            file_up=muilti_task.Muiltiple_task("file_upload",request)
            p=file_up.run()


            return HttpResponse("aaa")
    if request.method=="GET":
        ugroup_host = request.user.bind_host.all()
        return  render(request,'fileupload.html',{'ugroup_host':ugroup_host})


@login_required
@csrf_exempt

def prio_task(request):
    if request.method=="GET":
        a=celery_models.PeriodicTask.objects.all()
        print("task_prio",a)
        ret=froms.PeriodicTaskForm()
    if request.method=="POST":
        obj=froms.PeriodicTaskForm(instance=request.POST)
        if obj.is_valid():
            obj.save()


    return  render(request,"peri_task.html",{'ret':a})

@login_required
@csrf_exempt
def prio_task_add(request):
    if request.method=="GET":
        ret = froms.PeriodicTaskForm()

    if request.method=="POST":
        ret=froms.PeriodicTaskForm(request.POST)
        if ret.is_valid():
            #处理前台处理传过来的数据
            # print(ret.cleaned_data)
            email_dict={}
            # email_subject=ret.cleaned_data.get("email_subject")
            # email_from=ret.cleaned_data.get("email_from")
            # email_to=ret.cleaned_data.get("email_to")
            # email_content=ret.cleaned_data.get("email_content")
            for k,v in ret.cleaned_data.items():
                if k.startswith("email"):
                    if k=="email_to":
                        print(type(ret.cleaned_data[k]),ret.cleaned_data[k])
                        email_dict[k]=v.split()
                    email_dict[k]=v


            print(email_dict)

            ret.instance.kwargs=json.dumps(email_dict)
            print(ret.cleaned_data)





            ret.save(commit=True)
    return render(request, "peri_task_add.html", {'ret': ret})


#定时任务修改

@login_required
@csrf_exempt

def peri_task_edit(request,pid):
    peri_obj = celery_models.PeriodicTask.objects.get(id=pid)
    if request.method=="GET":

        ret=froms.PeriodicTaskForm(instance=peri_obj,initial={"email_subject":eval(peri_obj.kwargs).get("email_subject"),
                                                              "email_content":eval(peri_obj.kwargs).get("email_content"),
                                                              "email_to":eval(peri_obj.kwargs).get("email_to"),
                                                              "regtask":peri_obj.task


                                                              })
    elif request.method=="POST":
         ret=froms.PeriodicTaskForm(request.POST,instance=peri_obj)
         if ret.is_valid():
             ret.save()




    return  render(request,"peri_task_edit.html",{"ret":ret,"kwarg":ret.instance.kwargs})



@login_required
@csrf_exempt

def tackle_task_plan(reqeust):
    if reqeust.is_ajax():
        if reqeust.method=="POST":
            taskplan=reqeust.POST.get("taskplan")
            obj=models.TaskPlan.objects.create(planname=taskplan)
            
            Group('info').send({
        'text': json.dumps({
            'taskplan_name': obj.planname,
            'taskplan_id':str(obj.id),
            
        })
    })

            return  HttpResponse("ok")


@login_required
@csrf_exempt
def tackle_taskpstage(request):
    
    if request.is_ajax():
         
        if request.method=="POST":
            taskstage_obj=froms.TaskStageForm(request.POST)
            if taskstage_obj.is_valid():
                 taskstage_obj.save()
                 print("taskstage_obj",taskstage_obj.instance)
            
            Group('info').send({
        'text': json.dumps({
            'taskstage_name': taskstage_obj.instance.stagename,
            'taskstage_id':str(taskstage_obj.instance.id),
            
        })
    })

            return  HttpResponse("ok")



froms.GITTASKForm() 





@login_required
@csrf_exempt

def autorun(request):
    taskplan=froms.TaskPlanForm()
    taskstage=froms.TaskStageForm()
    taskjob=froms.TaskJobForm()
    sshtask=froms.SSHTASKForm()
    piptask=froms.PIPtaskForm()
    gittask=froms.GITTASKForm()
    scptask=froms.SCPTaskForm()
    if request.method=="POST":
        print(request.POST)
    elif request.method=="GET":

	    return render(request,"aoturun.html",{'taskplan':taskplan,"taskstage":taskstage,'taskjob':taskjob,'sshtask':sshtask,'scptask':scptask,'gittask':gittask,'piptask':piptask})



@login_required
@csrf_exempt

def tackle_taskjob(request):
	if request.is_ajax():
		if request.method=="POST":
			print(request.POST)
			#post the data to the sql
			taskjob=froms.TaskJobForm(request.POST)
			if taskjob.is_valid():
				print('hi,it is hrere!!!')
				taskjob.save(commit=True)
				plugin=taskjob.instance.get_task_type_display()
				if plugin=="sshtask":
					sshtask=froms.SSHTASKForm(request.POST)
					if sshtask.is_valid():
						obj=sshtask.save(commit=False)
						obj.taskjob=taskjob.instance
						obj.save()
						
						obj.bindhosts.add(*sshtask.cleaned_data['bindhosts'])
						
						print(type(obj))
						#sshtask.cleaned_data['taskjob']=taskjob.instance
						#a=sshtask.cleaned_data.pop('bindhosts')
						print('new_cleaned_data',sshtask.cleaned_data)
						#b=models.SSHTASK.objects.create(**sshtask.cleaned_data)
						#b.bindhosts.add(*a)
						#print('this is job',sshtask.instance.bindhosts)
			
				if plugin=="gittask":
					gittask=froms.GITTASKForm(request.POST)
					if gittask.is_valid():
						obj=gittask.save(commit=False)
						obj.taskjob=taskjob.instance
						obj.save()
						obj.bindhosts.add(*gittask.cleaned_data['bindhosts'])


				if plugin=="scptask":
					scptask=froms.SCPTaskForm(request.POST)
					print(scptask)
					if scptask.is_valid():
						obj=scptask.save(commit=False)
						obj.taskjob=taskjob.instance
						obj.save()
						obj.bindhost.add(*scptask.cleaned_data['bindhost'])
			
			return HttpResponse('ok')







@login_required
@csrf_exempt

def run_task(request):
	if request.is_ajax():
		if request.method=="POST":
			print(request.POST)
			a=runtask.exec_task(request.POST.get("plan_id"))
			a.run()
			return HttpResponse('ok')








@login_required
#用户修改密码
def change_pass(request):

    if request.method=="POST":
        old_ass=request.POST.get('old_pass')
        new_pass=request.POST.get('new_pass')
        print(old_ass,new_pass)
        # user=models.UserProfile.objects.get(email=request.user)
        ret=request.user.check_password(old_ass)
        if ret:
            request.user.set_password(new_pass)
            request.user.save()
            return  HttpResponse('修改成功！')
    return  render(request,'change_pass.html')
