from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from hc.forms.forms_receptionist import ViewAppointmentForm, Doctor_Select
from hc.forms.forms_doctor import SearchPatientForm
from hc.models import Appointment


@login_required(login_url="/accounts/login/")
@user_passes_test(lambda u: u.groups.filter(name='receptionist').exists())
def IndexViewReceptionist(request):
    form = SearchPatientForm()
    doc_form = Doctor_Select()
    if request.method == "POST":
        username = request.POST.get('username', False)
        doc_form = Doctor_Select(request.POST)
        if doc_form.is_valid():
            data = doc_form.cleaned_data
            field = data['doctor']
            args = {'field': field}
            args['appointments'] = Appointment.objects.all().filter(doctor=field).order_by('time')
            global val

            def val():
                return data
            return redirect('main:recep_appointments')

        return redirect('hc:appointment', username=username)
    else:
        args = {}
        args['appointments'] = Appointment.objects.all().order_by('time')[:5]
        args['form'] = form
        args['doc_form'] = doc_form
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


def Recep_Appointments(request):
    data = val()
    field = data['doctor']
    args = {'field': field}
    args['appointments'] = Appointment.objects.all().filter(doctor=field).order_by('time')
    return render(request, 'receptionist/testform_result.html', args)
