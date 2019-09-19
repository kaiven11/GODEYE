"""GODEYE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from GOD import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^check_code/$', views.check_code),
    url(r'^account/login/$', views.index),
    url(r'^account/logout/$', views.logout),
    url(r'^OverView', views.OverView,name="overview"),
    url(r'^mange_host', views.mange_host,name="mange_host"),
    url(r'^change_pass', views.change_pass,name="change_pass"),
    url(r'^logout', views.log_out,name="log_out"),
    url(r'^host_info/(\d+)', views.host_info,name="host_info"),
    url(r'^get_cpu', views.get_cpu,name="get_cpu"),
    url(r'^muilt_cmd/$', views.muilt_cmd,name="muilt_cmd"),
    url(r'^file_upload/$', views.file_upload,name="file_upload"),
    url(r'^prio_task/$', views.prio_task,name="prio_task"),
    url(r'^prio_task/add$', views.prio_task_add,name="prio_task_add"),
    url(r'^prio_task/edit-(?P<pid>(\d+))$', views.peri_task_edit,name="peri_task_edit"),
    url(r'^autorun$', views.autorun,name="autorun"),
    url(r'^taskplan$', views.tackle_task_plan,name="taskplan"),
    url(r'^taskpstage$', views.tackle_taskpstage,name="taskpstage"),
    url(r'^taskjob$', views.tackle_taskjob,name="tackle_job"),
    url(r'^run_task$', views.run_task,name="run_task"),
    
]
