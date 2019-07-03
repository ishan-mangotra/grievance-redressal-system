from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
#from users.models import User as get_user_model
from datetime import timedelta


class Complaint(models.Model):
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
    s4="reassign"
    status_choice = ((s1,"unresolved"),(s2,"resolved"),(s3,"spam"),(s4,"reassign"))

    f1="Applications Issues"
    f2="Payment Issues"
    f3="Data Fields"
    f4="Server Slowness"
    f5="Others"
    stream_choices = ((f1,"Application Issues"),(f2,"Payment Issues"),(f3,"Data Fields"),(f4,"Server Slowness"),(f5,"Others"))

    def two_days():
        now = timezone.now()
        return now + timedelta(days=2)

    date = models.DateTimeField(default=timezone.now)
    channel = models.CharField(max_length = 25, choices = channel_choice, default = c1)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    dept = models.CharField(max_length = 25, choices = dept_choice, default = d1)
    complaint = models.CharField(max_length=1000)
    status = models.CharField(max_length = 15, choices = status_choice, default = s1)
    resolution = models.CharField(max_length=1000)
    resolved_by = models.CharField(max_length = 32, default=None, blank=True, null=True)
    assigned_to = models.CharField(max_length = 32, default=None, blank=True, null=True)
    sle_date = models.DateTimeField(default = two_days)
    stream = models.CharField(max_length = 25, choices = stream_choices, default = f1)
    image = models.ImageField(upload_to = 'images/', blank=True, null=True)
    file = models.FileField(upload_to = 'documents/', blank=True, null=True)

    def token(self):
        self.token = 'CMPLNOO'+str(self.id)
        return self.token
