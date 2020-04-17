from accounts.models import Doctor, Patient
from .forms import treatPatientForm
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView
import datetime as dt
from.models import Appointment


def makeAppointment(form, patient):
    if form.is_valid():
        specialization = form['specialization'].value()
        available_doctors = list(Doctor.objects.all().filter(available=True, specialization=specialization))[0]
        patient = get_object_or_404(Patient, user__email=patient)
        time = form['time'].value()
        date = form['date'].value()
        Appointment.objects.create(patient=patient, doctor=available_doctors, time=time, date=date)


class treatPatientView(CreateView):
    form_class = treatPatientForm
    template_name = 'hc/treat_patient.html'
    success_url = '/'
    super_context = {}

    def get_context_data(self, *args, **kwargs):
        context = super(treatPatientView, self).get_context_data(*args, **kwargs)
        min_dt = dt.datetime.now()-dt.timedelta(minutes=30)

        for appointment in Appointment.objects.filter().order_by('date', 'time'):    # first sorted by date and then time
            if(appointment.date < min_dt.date()):
                appointment.delete()
            elif(appointment.date == min_dt.date() and appointment.time < min_dt.time()):
                appointment.delete()
            else:
                break
        email = self.request.POST.get('email', False)
        if email:
            try:
                appointment = Appointment.objects.filter(patient=email).order_by('date', 'time')[0]
            except IndexError:
                context['appointment'] = None
                return context

        else:
            appointment = Appointment.objects.filter().order_by('date', 'time')[0]
        patient = get_object_or_404(Patient, user__email=appointment.patient)
        context['appointment'] = appointment
        context['patient'] = patient
        self.super_context['email'] = appointment.patient
        return context

    def form_valid(self, form, **kwargs):
        context = self.super_context
        email = context['email']
        appointment = Appointment.objects.filter(patient=email).order_by('date', 'time')[0]
        prescription = form.save()
        prescription.doctor = appointment.doctor
        patient = get_object_or_404(Patient, user__email=appointment.patient)
        patient.prescriptions.add(prescription)
        appointment.delete()
        return super(treatPatientView, self).form_valid(form)
