from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from hc.forms.forms_receptionist import ViewAppointmentForm, SelectDoctor
from hc.forms.forms_doctor import SearchPatientForm
from hc.models import Appointment
from accounts.models import Doctor
from django.contrib.auth.models import User


@login_required(login_url="/accounts/login/")
@user_passes_test(lambda u: u.groups.filter(name='receptionist').exists())
def IndexViewReceptionist(request):
    form = SearchPatientForm()
    appn_doc_form = SelectDoctor()
    if request.method == "POST":
        username = request.POST.get('username', False)
        appn_doc_form = SelectDoctor(request.POST)
        if appn_doc_form.is_valid():
            data = appn_doc_form.cleaned_data
            doc_name = data['doctor']
            return redirect('main:recep_appointments', doc_name)

        return redirect('hc:appointment', username=username)
    else:
        args = {}
        args['appointments'] = Appointment.objects.all().order_by('time')[:5]
        args['form'] = form
        args['appn_doc_form'] = appn_doc_form
        return render(request, 'receptionist/index.html', args)


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


def AppointmentsOfDoctor(request, doc_name):
    doc_user = get_object_or_404(User, username=doc_name)
    doctor_username = get_object_or_404(Doctor, user=doc_user)
    args = {'appointments': Appointment.objects.all().filter(doctor=doctor_username).order_by('time')}
    return render(request, 'receptionist/testform_result.html', args)
