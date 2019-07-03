#importing template to set up a python filter block in html
from django import template
#importing group as the filters will be based on groups
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='group')
def group(user, group_name):
    # returns true if the user belongs to a group. Else, false.
    return user.groups.filter(name=group_name).exists()
