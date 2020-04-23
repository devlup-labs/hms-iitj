from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
import datetime as dt
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from accounts.models import Patient
from .forms_doctor import treatPatientForm, AddBlogForm
from .models import Appointment


class treatPatientView(CreateView):
    form_class = treatPatientForm
    template_name = 'hc/treat_patient.html'
    success_url = '/'
    super_context = {}

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


class AddBlogView(SuccessMessageMixin, CreateView):
    template_name = 'main/add_blog.html'
    form_class = AddBlogForm
    success_url = '/'
    success_message = 'Blog was successfully created.'
    extra_tags = 'd-flex justify-content-center alert alert-success alert-dismissible fade show'

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message, extra_tags=self.extra_tags)
        return response
