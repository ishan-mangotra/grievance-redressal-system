from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils import six

#Function to check if a user is part of a group
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

#to display index page
def index(request):
    return render(request, 'index.html')

#To display faqs page
def faqs(request):
    return render(request, 'faqs.html')

#To display register page
def register(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        #if form data is valid, clearing django form validations
        #Form details are saved to user model
        form.save()

        #We extract the first name to redirect to login page and display a personalized success message
        first_name = form.cleaned_data.get('first_name')
        messages.success(request, f'Congratulations on registration {first_name}! Login to proceed')
        return redirect('login')
    #In case form hasn't been submitted or has validation errors,
    # the form is returned on the registration page itself
    else:
        return render(request, 'register.html', {"form" : form })
