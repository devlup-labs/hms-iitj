from django.shortcuts import render, redirect
from .models import Blog
from hc.models import Appointment
from hc.forms_patient import takeAppointmentForm
from hc.forms_doctor import SearchPatientForm
from hc.views_patient import makeAppointment


def IndexView(request):
    blogs = Blog.objects.all()
    appn = Appointment.objects.all()

    if request.user.is_authenticated:
        if hasattr(request.user, 'doctor'):
            form = SearchPatientForm
            return render(request, 'main/doctors_home_page.html', {'form': form})
        elif hasattr(request.user, 'receptionist'):
            return render(request, 'main/receptionists_home.html')
        # add pharmacist and admin fields here
        appn = appn.filter(patient=request.user.email).order_by('date', 'time')
        if not hasattr(request.user, 'patient'):
            return redirect('accounts:createProfile')

    if request.method == 'POST':
        return makeAppointment(request)

    form = takeAppointmentForm()
    return render(request, 'main/index.html', {'form': form, 'blogs': blogs, 'user': request.user, 'appointments': appn})
