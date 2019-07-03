from django.contrib import admin
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.admin.widgets import FilteredSelectMultiple

User = get_user_model()

class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = []

    # Add the users field.
    users = forms.ModelMultipleChoiceField(
         queryset=User.objects.all(),
         required=False,
         # Use the pretty 'filter_horizontal widget'.
         widget=FilteredSelectMultiple('users', False)
    )

    def __init__(self, *args, **kwargs):
        # Do the normal form initialisation.
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        # If it is an existing group (saved objects have a pk).
        if self.instance.pk:
            # Populate the users field with the current Group users.
            self.fields['users'].initial = self.instance.user_set.all()

    def save_m2m(self):
        # Add the users to the Group.
        self.instance.user_set.set(self.cleaned_data['users'])

    def save(self, *args, **kwargs):
        # Default save
        instance = super(GroupAdminForm, self).save()
        # Save many-to-many data
        self.save_m2m()
        return instance


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('username', 'email','first_name','last_name','phone')
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('email','username', 'password')}),
        ('Personal info', {'fields': ('first_name','last_name', 'phone','housenumber','locality','village','mandal','district','pincode')}),

    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
        ),
    )
    search_fields = ('username','email','first_name','last_name','phone')
    ordering = ('username','email','phone')
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)

class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    filter_horizontal = ['permissions']

admin.site.register(Group, GroupAdmin)
