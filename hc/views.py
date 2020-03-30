from django.shortcuts import redirect, render
# from django.views.generic import CreateView
# from .forms import writePrescription
from accounts.models import Appointment, Doctor


def createAppointment(request):
    if request.method == 'POST':
        user = request.user
        specialization = request.POST.get('specialization')
        available_doctors = Doctor.objects.filter(available=True, specialization=specialization)
        # appointment =
        Appointment.objects.create(patient=user, doctor=available_doctors[0])
        return redirect('hc:take_appointment')
    return render(request, 'hc/create_appointment.html')
