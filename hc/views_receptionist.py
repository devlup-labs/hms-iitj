from django.shortcuts import render, get_object_or_404, redirect
from .forms_receptionsist import ViewAppointmentForm
from .models import Appointment


def IndexViewReceptionist(request):
    if request.method == "POST":
        email = request.POST.get('email', False)
        ldap = email[:-len('@iitj.ac.in')]
        return redirect('hc:appointment', ldap=ldap)
    else:
        return render(request, 'receptionist/index.html')


def SearchAppointmentView(request, ldap):
    email = ldap + '@iitj.ac.in'
    if Appointment.objects.filter(patient=email).exists():
        appn = get_object_or_404(Appointment, patient=email)
        if request.method == "POST":
            form = ViewAppointmentForm(request.POST, instance=appn)
            form.save()
            return redirect("main:home")
        else:
            form = ViewAppointmentForm(instance=appn)
    else:
        form = ViewAppointmentForm()
    return render(request, 'receptionist/view_appointment.html', {'form': form, 'appointment': appn})
