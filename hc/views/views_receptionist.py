from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from hc.forms.forms_receptionist import ViewAppointmentForm
from hc.forms.forms_doctor import SearchPatientForm
from hc.models import Appointment


@login_required(login_url="/accounts/login/")
@user_passes_test(lambda u: u.groups.filter(name='receptionist').exists())
def IndexViewReceptionist(request):
    form = SearchPatientForm()
    if request.method == "POST":
        username = request.POST.get('username', False)
        return redirect('hc:appointment', username=username)
    else:
        return render(request, 'receptionist/index.html', {'form': form})


@login_required(login_url="/accounts/login/")
@user_passes_test(lambda u: u.groups.filter(name='receptionist').exists())
def SearchAppointmentView(request, username):
    if Appointment.objects.filter(patient=username).exists():
        appn = Appointment.objects.filter(patient=username).order_by('time')[0]
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
            form = ViewAppointmentForm(initial={'patient': username})
            appn = None
            return render(request, 'receptionist/view_appointment.html', {'form': form, 'appointment': appn})
 