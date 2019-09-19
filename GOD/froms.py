#coding=utf-8
from __future__ import absolute_import, unicode_literals

from django import forms
from django.conf import settings
from django.contrib import admin
from django.forms.widgets import Select
from django.template.defaultfilters import pluralize
from django.utils.translation import ugettext_lazy as _
from GOD import models
from django.forms import fields as celery_fileds
# from django.forms import forms


from celery import current_app
from celery.utils import cached_property
from kombu.utils.json import loads

from django_celery_beat.models import (
    PeriodicTask, PeriodicTasks,
    IntervalSchedule, CrontabSchedule,
    SolarSchedule
)
from django_celery_beat.utils import is_database_scheduler

class TaskSelectWidget(Select):
    """Widget that lets you choose between task names."""

    celery_app = current_app
    _choices = None

    def tasks_as_choices(self):
        _ = self._modules  # noqa
        tasks = list(sorted(name for name in self.celery_app.tasks
                            if not name.startswith('celery.')))
        return (('', ''), ) + tuple(zip(tasks, tasks))

    @property
    def choices(self):
        if self._choices is None:
            self._choices = self.tasks_as_choices()
        return self._choices

    @choices.setter
    def choices(self, _):
        # ChoiceField.__init__ sets ``self.choices = choices``
        # which would override ours.
        pass

    @cached_property
    def _modules(self):
        self.celery_app.loader.import_default_modules()
class TaskChoiceField(forms.ChoiceField):
    """Field that lets you choose between task names."""

    widget = TaskSelectWidget

    def valid_value(self, value):
        return True
class PeriodicTaskForm(forms.ModelForm):
    email_subject=celery_fileds.CharField()
    email_to=celery_fileds.EmailField()
    # email_from=celery_fileds.EmailField()
    email_content=celery_fileds.CharField()
    """Form that lets you create and modify periodic tasks."""
    def __new__(cls, *args, **kwargs):
        for field_name,field_obj in cls.base_fields.items():

            #判断是否字段在 只读字段中
            field_obj.widget.attrs['class'] = 'form-control'


        return  forms.ModelForm.__new__(cls)
    # def __init__(self,*args,**kwargs):
    #     super(PeriodicTaskForm,self).__init__(*args,**kwargs)

        # self.fields["regtask"].choices=TaskSelectWidget.choices
    regtask = TaskChoiceField(
        label=_('Task (registered)'),
        required=False,
    )

    task = forms.CharField(
        label=_('Task (custom)'),
        required=False,
        max_length=200,
    )

    class Meta:
        """Form metadata."""

        model = PeriodicTask
        exclude = ("interval","solar","kwargs","queue",
                   "exchange",
                    "routing_key",
                   "total_run_count",
                   "args",



                   )

    def clean(self):
        data = super(PeriodicTaskForm, self).clean()
        regtask = data.get('regtask')
        if regtask:
            data['task'] = regtask
        if not data['task']:
            exc = forms.ValidationError(_('Need name of task'))
            self._errors['task'] = self.error_class(exc.messages)
            raise exc
        return data

    def _clean_json(self, field):
        value = self.cleaned_data[field]
        try:
            loads(value)
        except ValueError as exc:
            raise forms.ValidationError(
                _('Unable to parse JSON: %s') % exc,
            )
        return value

    def clean_args(self):
        return self._clean_json('args')

    def clean_kwargs(self):
        return self._clean_json('kwargs')




    #上为celerymodelform

    #------------------------------------------------------

class TaskPlanForm(forms.ModelForm):
    class Meta:
        model=models.TaskPlan
        fields="__all__"
   
         


class TaskStageForm(forms.ModelForm):
    class Meta:
        model=models.TaskStage
        fields="__all__"

        def __init__(self, *args, **kwargs):
            super(TaskStageForm, self).__init__(*args, **kwargs)
            print(self.fields)
            self.fields['taskplan_id'].choices = models.TaskPlan.objects.values_list("name")
        # labels={
        #     "name":"计划名称",
        # }

class SCPTaskForm(forms.ModelForm):
	class Meta:
           model=models.SCPTASK
           fields="__all__"
           exclude=('taskjob',)
class TaskJobForm(forms.ModelForm):
    class Meta:
        model=models.TaskJob
        fields="__all__"

class SSHTASKForm(forms.ModelForm):
    class Meta:
        model=models.SSHTASK
        fields="__all__"
        exclude=('taskjob',)

class PIPtaskForm(forms.ModelForm):
    class Meta:
        model=models.PIPtask
        fields="__all__"
        exclude=('taskjob',)

class GITTASKForm(forms.ModelForm):
    class Meta:
        model=models.GITTASK
        fields="__all__"
        exclude=('taskjob',)
