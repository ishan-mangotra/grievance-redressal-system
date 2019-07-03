from django.contrib import admin
#Importing the new forms to be used instead of the regular django user forms
from .forms import UserAdminCreationForm, UserAdminChangeForm
#importing the default user model
from .models import User
from django.contrib.auth import get_user_model
#importing user types to set up a custom user model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
#importing to modify the group model
from django.contrib.auth.models import Group
#importing to allow multiple users to be a part of a group
from django.contrib.admin.widgets import FilteredSelectMultiple


User = get_user_model()

# Creating a new form to enter groups
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

# Registering UserAdmin as the default user
admin.site.register(User, UserAdmin)

#Creating a new group model
class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    filter_horizontal = ['permissions']

#Unregistering the default group model
admin.site.unregister(Group)
#Registering GroupAdmin as the default Group model
admin.site.register(Group, GroupAdmin)
