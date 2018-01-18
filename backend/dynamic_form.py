#coding=utf-8
from django.forms import ModelForm
def Create_Dynamic_Form(model_class):
    '''
    __init__是当实例对象创建完成后被调用的，然后设置对象属性的一些初始值。
    __new__是在实例创建之前被调用的，因为它的任务就是创建实例然后返回该实例，是个静态方法。
    也就是，__new__在__init__之前被调用，__new__的返回值（实例）将传递给__init__方法的第一个参数，然后__init__给这个实例设置一些参数。
    :param admins:
    :return:

    '''

    # def __new__(cls,*args,**kwargs):
    #     for field_name,field_obj in cls.base_fields.items():
    #         field_obj.widget.attrs['class']='form-control'
    #     return ModelForm.__new__(cls)



    class Meta:
        model=model_class
        fields="__all__"
    attr={'Meta':Meta}
    myform=type("dynamic_form",(ModelForm,),attr)

    return  myform