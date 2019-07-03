from django.shortcuts import render,redirect, get_object_or_404, reverse
from django.utils import timezone, six
from urllib.parse import urlencode
from django.http import HttpResponse, HttpResponseRedirect
from .models import Complaint
from users.models import User_manager
from .forms import ComplaintForm,editprofileform, complaintredressal, dashboardform,managerform
from django.contrib.auth.models import User,Permission,Group
from django.contrib.auth import get_user_model,update_session_auth_hash
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.core.mail import send_mail
from django.conf import settings
# Create your s here.


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

@login_required
def home(request):

    if request.method == "POST":
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            context = Complaint()
            context.author = request.user
            context.complaint = form.cleaned_data['complaint']
            context.channel = form.cleaned_data['channel']
            context.stream = form.cleaned_data['stream']
            context.dept = form.cleaned_data['dept']
            context.image = form.cleaned_data['image']
            context.file = form.cleaned_data['file']
            context.save()
            return redirect('done/')

    form = ComplaintForm()
    context = {'form':form}
    return render(request, 'complaint-register.html', context)
# @login_required
def done(request):
    return render(request, 'complaint-registered.html')

#Staff Dashboard to view all the assigned complaints
@group_required('staff')
def staffdashboard(request):
    dat = timezone.now()
    complaints_unre = Complaint.objects.filter(assigned_to=request.user)
    complaints_re = Complaint.objects.filter(assigned_to=request.user,status = "resolved")
    context = {'complaints_unre' : complaints_unre,'complaints_re':complaints_re,"dat":dat}
    return render(request, 'staff-dashboard.html', context)

#Complaint dashboard to assign all complaints
@login_required
def dashboard(request):
    form = dashboardform()
    dat = timezone.now()
    query=User.objects.filter(groups__name='staff')
    dep=request.GET.get("d")
    cha=request.GET.get("c")
    name=request.GET.get("n")
    cm=request.GET.get("c")
    complaints_unre = Complaint.objects.filter(dept="department0",status = "unresolved")
    complaints_re = Complaint.objects.filter(dept="department0",status ="resolved")
    complaints_spam = Complaint.objects.filter(dept="department0",status ="spam")
    complaints_assgn = Complaint.objects.filter(dept="department0",status ="reassign")

    compl=Complaint.objects.filter(dept="department0",status ="resolved")


    if dep and cha:

        complaints_unre = Complaint.objects.filter(dept=dep,channel=cha,status = "unresolved")
        complaints_re = Complaint.objects.filter(dept=dep,channel=cha,status ="resolved")
        complaints_spam = Complaint.objects.filter(dept=dep, channel=cha,status ="spam")
        complaints_assgn = Complaint.objects.filter(dept=dep,channel=cha,status ="reassign")
    if dep == "All" and cha !="All":
        complaints_unre = Complaint.objects.filter(channel=cha,status = "unresolved")
        complaints_re = Complaint.objects.filter(channel=cha,status ="resolved")
        complaints_spam = Complaint.objects.filter(channel=cha,status ="spam")
        complaints_assgn = Complaint.objects.filter(channel=cha,status ="reassign")
    if cha == "All"and dep != "All":
        complaints_unre = Complaint.objects.filter(dept=dep,status = "unresolved")
        complaints_re = Complaint.objects.filter(dept=dep,status ="resolved")
        complaints_spam = Complaint.objects.filter(dept=dep,status ="spam")
        complaints_assgn = Complaint.objects.filter(dept=dep,status ="reassign")
    if dep == "All" and cha =="All":
        complaints_unre = Complaint.objects.filter(status = "unresolved")
        complaints_re = Complaint.objects.filter(status ="resolved")
        complaints_spam = Complaint.objects.filter(status ="spam")
        complaints_assgn = Complaint.objects.filter(status ="reassign")

    if name and cm:
        Complaint.objects.filter(id=cm).update(assigned_to=name)



    context = {'form':form,'complaints_unre' : complaints_unre,'complaints_re':complaints_re,'complaints_spam':complaints_spam,'complaints_assgn':complaints_assgn,'dat':dat,'query':query,'name':name,'compl':compl}
    return render(request, 'complaint-dashboard.html', context)

#edit profile view
@login_required
def edit(request):

    #person = get_user_model()
    if request.method == "POST":
        form = editprofileform(request.POST,instance = request.user,initial={'email':request.user.email,'phone':request.user.phone})
        form.actual_user = request.user
        #if form.is_valid():
        form.save()
        return redirect('/mycomplaints')
    else:
        form = editprofileform(initial={'email':request.user.email,
            'phone':request.user.phone,
            'housenumber':request.user.housenumber,
            'locality':request.user.locality,
            'village':request.user.village,
            'mandal':request.user.mandal,
            'district':request.user.district,
            'pincode':request.user.pincode})
        args = {'form':form}
        return render(request, 'edit.html', args)

#Change passsword
@login_required
def passwordchange(request):

    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/mycomplaints')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form':form}
        return render(request, 'edit-password.html', args)

#Page to view all the complaints registered by user
@login_required
def mycomplaints(request):
    context = {
        'complaints' : Complaint.objects.filter(author= request.user)


    }

    return render(request, 'complaint-view.html', context)



@login_required
def redressal(request, cmp_id):
    comp = get_object_or_404(Complaint,pk=cmp_id)
    if request.method == "POST":
        form =complaintredressal(request.POST, request.FILES)
        if form.is_valid():
            comp.status = form.cleaned_data['status']
            comp.resolution = form.cleaned_data['resolution']
            comp.resolved_by = request.user.username
            comp.save()

            return redirect('/dashboard')

    form = complaintredressal()

    return render(request, 'complaint-redressal.html',{'comp':comp,'form':form})

@login_required
def myprofile(request):
    context = {
        'details': request.user
    }
    return render(request, 'profile.html', context)

#Manager has their own dashboard
User=get_user_model()
@group_required('manager')
def manager(request):
    form = managerform()
    dat = timezone.now()
    query=User.objects.all()
    dep=request.GET.get("d")
    cha=request.GET.get("c")
    date1=request.GET.get("date1")
    date2=request.GET.get("date2")

    name=request.GET.get("n")
    if name=="All":
        name=0
    complaints_unre = Complaint.objects.filter(dept="department0",status = "unresolved")
    complaints_re = Complaint.objects.filter(dept="department0",status ="resolved")

    c1 = len(Complaint.objects.filter(status ="unresolved"))
    c2 = len(Complaint.objects.filter(status ="resolved"))
    c5 = len(Complaint.objects.filter(status ="spam"))
    x = Complaint.objects.filter(status ="unresolved")

    c3=0

    for i in x:
        if i.sle_date<dat:
            c3+=1

    total = len(Complaint.objects.all())
    c4 = total -c3

    if dep and cha and not name:
        if date1 and date2:
            complaints_unre = Complaint.objects.filter(dept=dep,channel=cha,status = "unresolved",date__range=[date1, date2])
            complaints_re = Complaint.objects.filter(dept=dep,channel=cha,status ="resolved",date__range=[date1, date2])
            complaints_spam = Complaint.objects.filter(dept=dep, channel=cha, status='spam', date__range=[date1,date2])
        elif not (date1 and date2):
            complaints_unre = Complaint.objects.filter(dept=dep,channel=cha,status = "unresolved")
            complaints_re = Complaint.objects.filter(dept=dep,channel=cha,status ="resolved")
            complaints_spam = Complaint.objects.filter(dept=dep, channel=cha, status='spam')

        c1=len(complaints_unre)
        c2=len(complaints_re)
        c5=len(complaints_spam)

    if dep == "All" and cha !="All" and not name:
        if date1 and date2:
            complaints_unre = Complaint.objects.filter(channel=cha,status = "unresolved",date__range=[date1, date2])
            complaints_re = Complaint.objects.filter(channel=cha,status ="resolved",date__range=[date1, date2])
        elif not (date1 and date2):
            complaints_unre = Complaint.objects.filter(channel=cha,status = "unresolved")
            complaints_re = Complaint.objects.filter(channel=cha,status ="resolved")
        c1=len(complaints_unre)
        c2=len(complaints_re)
    if cha == "All"and dep != "All" and not name:
        if date1 and date2:
            complaints_unre = Complaint.objects.filter(dept=dep,status = "unresolved",date__range=[date1, date2])
            complaints_re = Complaint.objects.filter(dept=dep,status ="resolved",date__range=[date1, date2])
        elif not (date1 and date2):
            complaints_unre = Complaint.objects.filter(dept=dep,status = "unresolved")
            complaints_re = Complaint.objects.filter(dept=dep,status ="resolved")
        c1=len(complaints_unre)
        c2=len(complaints_re)
    if dep == "All" and cha =="All" and not name:
        if date1 and date2:
            complaints_unre = Complaint.objects.filter(status = "unresolved",date__range=[date1, date2])
            complaints_re = Complaint.objects.filter(status ="resolved",date__range=[date1, date2])
        elif not (date1 and date2):
            complaints_unre = Complaint.objects.filter(status = "unresolved")
            complaints_re = Complaint.objects.filter(status ="resolved")
        c1=len(complaints_unre)
        c2=len(complaints_re)

    ##################################################################################################

    if dep and cha and name:
        if date1 and date2:
            complaints_unre = Complaint.objects.filter(dept=dep,channel=cha,status = "unresolved",date__range=[date1, date2],resolved_by=name)
            complaints_re = Complaint.objects.filter(dept=dep,channel=cha,status ="resolved",date__range=[date1, date2],resolved_by=name)
        elif not (date1 and date2):
            complaints_unre = Complaint.objects.filter(dept=dep,channel=cha,status = "unresolved",resolved_by=name)
            complaints_re = Complaint.objects.filter(dept=dep,channel=cha,status ="resolved",resolved_by=name)
        c1=len(complaints_unre)
        c2=len(complaints_re)

    if dep == "All" and cha !="All" and name :
        if date1 and date2:
            complaints_unre = Complaint.objects.filter(channel=cha,status = "unresolved",date__range=[date1, date2],resolved_by=name)
            complaints_re = Complaint.objects.filter(channel=cha,status ="resolved",date__range=[date1, date2],resolved_by=name)
        elif not (date1 and date2):
            complaints_unre = Complaint.objects.filter(channel=cha,status = "unresolved",resolved_by=name)
            complaints_re = Complaint.objects.filter(channel=cha,status ="resolved",resolved_by=name)
        c1=len(complaints_unre)
        c2=len(complaints_re)
    if cha == "All"and dep != "All" and name:
        if date1 and date2:
            complaints_unre = Complaint.objects.filter(dept=dep,status = "unresolved",date__range=[date1, date2],resolved_by=name)
            complaints_re = Complaint.objects.filter(dept=dep,status ="resolved",date__range=[date1, date2],resolved_by=name)
        elif not (date1 and date2):
            complaints_unre = Complaint.objects.filter(dept=dep,status = "unresolved",resolved_by=name)
            complaints_re = Complaint.objects.filter(dept=dep,status ="resolved",resolved_by=name)
        c1=len(complaints_unre)
        c2=len(complaints_re)
    if dep == "All" and cha =="All" and name:
        if date1 and date2:
            complaints_unre = Complaint.objects.filter(status = "unresolved",date__range=[date1, date2],resolved_by=name)
            complaints_re = Complaint.objects.filter(status ="resolved",date__range=[date1, date2],resolved_by=name)
        elif not (date1 and date2):
            complaints_unre = Complaint.objects.filter(status = "unresolved",resolved_by=name)
            complaints_re = Complaint.objects.filter(status ="resolved",resolved_by=name)
        c1=len(complaints_unre)
        c2=len(complaints_re)


    context = {'form':form,'complaints_unre' : complaints_unre,'complaints_re':complaints_re,
                'dat':dat,'c1':c1,'c2':c2,'c3':c3,'c4':c4,'c5':c5,'query':query,'total':total}
    return render(request, 'manager-dashboard.html', context)


@login_required
@permission_required('complaint.change_complaint')
def redressal(request, cmp_id):
    comp = get_object_or_404(Complaint,pk=cmp_id)
    if request.method == "POST":
        form =complaintredressal(request.POST, request.FILES)
        if form.is_valid():
            comp.status = form.cleaned_data['status']
            comp.resolution = form.cleaned_data['resolution']
            comp.resolved_by = request.user.username
            mail=comp.author.email
            send_mail(
            'Grievance',
            'Your Grievance is resolved!',
            'esdgrievance@gmail.com',
            [mail],
            fail_silently=False,
            )

           # sendmail(request,mail)

            comp.save()

            return redirect('/dashboard')

    form = complaintredressal()

    return render(request, 'complaint-redressal.html',{'comp':comp,'form':form})


def sendmail(request):
    mail='esdgrievance@gmail.com'
    m=mail
    send_mail(
        'Grievance',
        'Your Grievance is resolved!',
        'esdgrievance@gmail.com',
        [m],
        fail_silently=False,
    )
    return redirect('/dashboard')
    form = complaintredressal()
    return render(request, 'complaint-redressal.html',{'comp':comp,'form':form})



# @permission_required('complaint.change_complaint')
def details(request, cmp_id):
    comp = get_object_or_404(Complaint,pk=cmp_id)
    context = {'comp':comp}
    return render(request, 'complaint-details.html',context)




    # comp = get_object_or_404(Complaint,pk=cmp_id)
    # if request.method == "POST":
    #     form =complaintredressal(request.POST, request.FILES)
    #     if form.is_valid():
    #         comp.status = form.cleaned_data['status']
    #         comp.resolution = form.cleaned_data['resolution']
    #         comp.resolved_by = request.user.username
    #         mail=comp.author.email
    #         comp.save()
    #
    #         return redirect('/dashboard')
    #
    # form = complaintredressal()
    #
    # return render(request, 'complaint-redressal.html',{'comp':comp,'form':form})
