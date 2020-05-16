from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
import datetime as dt
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from accounts.models import Patient
from hc.forms.forms_doctor import treatPatientForm
from hc.models import Appointment


class patientHistoryView(UserPassesTestMixin, TemplateView):
    template_name = 'doctor/patient_history.html'

    def test_func(self):
        return self.request.user.groups.filter(name='doctor').exists()

    def get_context_data(self, *args, **kwargs):
        context = super(patientHistoryView, self).get_context_data(*args, **kwargs)
        patient = get_object_or_404(Patient, user__username=kwargs['ldap'])
        context['patient'] = patient
        return context


class treatPatientView(UserPassesTestMixin, CreateView):
    form_class = treatPatientForm
    template_name = 'doctor/treat_patient.html'
    success_url = '/'
    super_context = {}

    def test_func(self):
        return self.request.user.groups.filter(name='doctor').exists()

    def get(self, request, *args, **kwargs):
        min_dt = dt.datetime.now()-dt.timedelta(minutes=30)
        for appointment in Appointment.objects.filter().order_by('date', 'time'):    # first sorted by date and then time
            if(appointment.date < min_dt.date()):
                appointment.delete()
            elif(appointment.date == min_dt.date() and appointment.time < min_dt.time()):
                appointment.delete()
            else:
                break
        if Appointment.objects.exists():
            return super().get(request, *args, **kwargs)
        else:
            messages.error(
                self.request,
                "No Appointments.",
                extra_tags='d-flex justify-content-center alert alert-danger alert-dismissible fade show')
            return HttpResponseRedirect('/')

    def get_context_data(self, *args, **kwargs):
        context = super(treatPatientView, self).get_context_data(*args, **kwargs)
        email = self.request.POST.get('email', False)
        if email:
            try:
                appointment = Appointment.objects.filter(patient=email).order_by('date', 'time')[0]
            except IndexError:
                messages.error(
                    self.request,
                    "Patient has not taken appointment.",
                    extra_tags='d-flex justify-content-center alert alert-danger alert-dismissible fade show')
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
