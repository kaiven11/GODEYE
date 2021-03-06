from django.contrib import admin
from django import forms
from GOD import models


from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
# Register your models here.
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = models.UserProfile
        fields = ('email', 'name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = models.UserProfile
        fields = ('email', 'password', 'name', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserProfileAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name', "is_active","is_staff",'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_admin',"is_active",'is_superuser',"user_permissions","groups","group_host","bind_host")}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ("user_permissions","groups","group_host","bind_host")


class UserLogAdmin(admin.ModelAdmin):
    list_display = ('name','user','bindhost','logtime')

class TaskLogAdmin(admin.ModelAdmin):
    list_display = ('id','tag_name','user','task_pid','task_time','task_type')

class TaskdetailAdmin(admin.ModelAdmin):
    list_display = ('children_task','result','date','bind_host','event_log')

admin.site.register(models.HostGroups)
admin.site.register(models.Host)
admin.site.register(models.BindHosts)
admin.site.register(models.UserProfile,UserProfileAdmin)
admin.site.register(models.HostUser)
admin.site.register(models.TaskLog,TaskLogAdmin)
admin.site.register(models.Taskdetail,TaskdetailAdmin)
admin.site.register(models.IDC)
admin.site.register(models.UserLog,UserLogAdmin)
admin.site.register(models.TaskPlan)
admin.site.register(models.TaskStage)
admin.site.register(models.TaskJob)
admin.site.register(models.SSHTASK)
admin.site.register(models.SCPTASK)
admin.site.register(models.GITTASK)
admin.site.register(models.PIPtask)
