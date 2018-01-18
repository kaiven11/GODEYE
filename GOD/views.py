from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from backend import muilti_task


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
    # if request.method=="GET":
    #     pass
    if request.is_ajax():

        if request.method=="POST":
            # selected_host=request.POST.getlist('selected_host')
            # cmd=request.POST.get("cmd")

            print("here")
            ret=muilti_task.Muiltiple_task("cmd",request)
            a=ret.run()
            print(a)
            return  HttpResponse(ret)


    return render(request,"host_task.html",{'ugroup_host':ugroup_host})










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