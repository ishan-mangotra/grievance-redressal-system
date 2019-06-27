from django import forms
from .models import Complaint
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserChangeForm
from users.forms import RegistrationForm,changedetails
from django.contrib.auth import get_user_model



d1="Revenue"
d2="Food And Civil Supplies"
d3="GHMC"
d4="Commercial Taxes"
d5="SPDCL"
d6="NPDCL"
d7="Others"
dept_choice = ((d1,"Revenue"),(d2,"Food And Civil Supplies"),(d3,"GHMC"),(d4,"Commercial Taxes"),(d5,"SPDCL"),(d6,"NPDCL"),(d7,"Others"))

c1="MeeSeva"
c2="T-App Folio"
c3="T-Wallet"
channel_choice = ((c1,"MeeSeva"),(c2,"T-App Folio"),(c3,"T-Wallet"))

s1="unresolved"
s2="resolved"
s3="spam"
status_choice = ((s1,"unresolved"),(s2,"resolved"),(s3,"spam"))

f1="Applications Issues"
f2="Payment Issues"
f3="Data Fields"
f4="Server Slowness"
f5="Others"
stream_choice = ((f1,"Application Issues"),(f2,"Payment Issues"),(f3,"Data Fields"),(f4,"Server Slowness"),(f5,"Others"))
User=get_user_model()
class ComplaintForm(forms.Form):
    channel = forms.CharField(label='Channel', widget=forms.Select(choices=channel_choice))
    dept = forms.CharField(label='Department', widget=forms.Select(choices=dept_choice))
    stream = forms.CharField(label='Stream', widget=forms.Select(choices=stream_choice))
    complaint = forms.CharField(max_length=1000, required=True)
    image = forms.ImageField(required=False)
    file = forms.FileField(required=False)
    #file = forms.FileField()
#    image = forms.ImageField(upload_to='media/', null=True, blank=True)
#	file = forms.ImageField(upload_to='images/', null=True, blank=True)

class complaintredressal(forms.Form):

    resolution = forms.CharField(max_length=1000)
    status = forms.CharField(label='Status', widget=forms.Select(choices=status_choice))

class dashboardform(forms.Form):

    dept = forms.CharField(label='Department', widget=forms.Select(choices=dept_choice))

class managerform(forms.Form):
    username = forms.ModelChoiceField(queryset=User.objects.all(),required = False)


class editprofileform(changedetails):
    """phone = forms.CharField(max_length=10)
    housenumber = forms.CharField(max_length=255)
    locality = forms.CharField(max_length=255)
    village = forms.CharField(max_length=255)
    mandal = forms.CharField(max_length=255)
    district = forms.CharField(max_length=255)
    pincode = forms.CharField(max_length=6)"""
