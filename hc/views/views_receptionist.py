from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from hc.forms.forms_receptionist import ViewAppointmentForm
from hc.models import Appointment


@login_required(login_url="/accounts/login/")
@user_passes_test(lambda u: u.groups.filter(name='receptionist').exists())
def IndexViewReceptionist(request):
    if request.method == "POST":
        email = request.POST.get('email', False)
        ldap = email[:-len('@iitj.ac.in')]
        return redirect('hc:appointment', ldap=ldap)
    else:
        return render(request, 'receptionist/index.html')


@login_required(login_url="/accounts/login/")
@user_passes_test(lambda u: u.groups.filter(name='receptionist').exists())
def SearchAppointmentView(request, ldap):
    email = ldap + '@iitj.ac.in'
    if Appointment.objects.filter(patient=email).exists():
        appn = Appointment.objects.filter(patient=email).order_by('date', 'time')[0]
        if request.method == "POST":
            form = ViewAppointmentForm(request.POST, instance=appn)
            form.save()
            return redirect("main:home")
        else:
            form = ViewAppointmentForm(instance=appn)
            return render(request, 'receptionist/view_appointment.html', {'form': form, 'appointment': appn})
    else:
        if request.method == "POST":
            form = ViewAppointmentForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('main:home')
        else:
            form = ViewAppointmentForm(initial={'patient': email})
            appn = None
            return render(request, 'receptionist/view_appointment.html', {'form': form, 'appointment': appn})
