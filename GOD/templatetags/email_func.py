#coding=utf-8
from django.utils.safestring import  mark_safe
from django import template

register=template.Library()

@register.simple_tag
def email_tackle(arg):

    arg=dict(eval(arg))
    if len(arg)==0:
        return mark_safe("<td>None</td><td>None</td>")
    html_head=""
    for k,v in arg.items():

        html_head+="<td>"+arg.get(k,None)+"</td>"


    print(html_head)
    return mark_safe(html_head)

#处理添加定时任务和修改的数具
@register.simple_tag

def format_value(arg):
    print(arg.name)

    return mark_safe("dfd")

#tackle the m2m data
#@register.simple_tag

#def tackle_m2m(form_obj):
 #       print(form_obj,'this is a filed in form!')
	#model_name=form_obj.Meta.model._meta.many_to_many
	#for item in model_name:
	#	m2m_data=item.rel.to.objects.all()
	#for z in form_obj:














