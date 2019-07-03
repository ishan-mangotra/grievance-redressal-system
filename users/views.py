from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils import six

def group_required(group, login_url=None, raise_exception=False):
    def check_perms(user):
        if isinstance(group, six.string_types):
            groups =(group, )
        else:
            groups = group
        if user.groups.filter(name__in=groups).exists():
            return True
        if raise_exception:
            raise PermissionDenied
        return False
    return user_passes_test(check_perms, login_url=login_url)

def index(request):
    return render(request, 'index.html')

def faqs(request):
    return render(request, 'faqs.html')

def register(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        form.save()
        first_name = form.cleaned_data.get('first_name')
        messages.success(request, f'Congratulations on registration {first_name}! Login to proceed')
        return redirect('login')
    else:
        return render(request, 'register.html', {"form" : form })
