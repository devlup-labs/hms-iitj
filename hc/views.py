from django.shortcuts import get_object_or_404  # , redirect, render
from django.views.generic import CreateView
# from .forms import writePrescription
from accounts.models import Appointment, Doctor, Patient
from .forms import takeAppointment


class takeAppointmentView(CreateView):
    form_class = takeAppointment
    template_name = 'hc/create_appointment.html'
    success_url = '/'

    def form_valid(self, form):
        specialization = form['specialization'].value()
        available_doctors = list(Doctor.objects.all().filter(available=True, specialization=specialization))[0]
        patient = get_object_or_404(Patient, user=self.request.user)
        # appointment =
        Appointment.objects.create(patient=patient, doctor=available_doctors)
        return super(takeAppointmentView, self).form_valid(form)
