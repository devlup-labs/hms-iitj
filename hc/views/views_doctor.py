from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
import datetime as dt
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.models import Patient
from hc.forms.forms_doctor import treatPatientForm, SearchPatientForm
from hc.models import Appointment
from main.models import Blog
from django.utils.timezone import make_aware


@login_required(login_url="/accounts/login/")
@user_passes_test(lambda u: u.groups.filter(name='doctor').exists())
def IndexViewDoctor(request):
    form = SearchPatientForm()
    blogs = Blog.objects.filter(author__user__email=request.user.email)
    return render(request, 'doctor/index.html', {'form': form, 'blogs': blogs})


class patientHistoryView(UserPassesTestMixin, TemplateView):
    template_name = 'doctor/patient_history.html'

    def test_func(self):
        return self.request.user.groups.filter(name='doctor').exists()

    def get_context_data(self, *args, **kwargs):
        context = super(patientHistoryView, self).get_context_data(*args, **kwargs)
        patient = get_object_or_404(Patient, user__username=kwargs['username'])
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
        min_dt = make_aware(min_dt)  # to convert naive date time to aware datetime
        for appointment in Appointment.objects.filter().order_by('time'):    # sorted by time
            if(appointment.time < min_dt):
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
        username = self.request.POST.get('username', False)
        if username:
            try:
                appointment = Appointment.objects.filter(patient=username).order_by('time')[0]
            except IndexError:
                messages.error(
                    self.request,
                    "Patient has not taken appointment.",
                    extra_tags='d-flex justify-content-center alert alert-danger alert-dismissible fade show')
                context['appointment'] = None
                return context

        else:
            appointment = Appointment.objects.filter().order_by('time')[0]
        patient = get_object_or_404(Patient, user__username=appointment.patient)
        context['appointment'] = appointment
        context['patient'] = patient
        self.super_context['username'] = appointment.patient
        return context

    def form_valid(self, form, **kwargs):
        context = self.super_context
        username = context['username']
        appointment = Appointment.objects.filter(patient=username).order_by('time')[0]
        prescription = form.save()
        prescription.doctor = appointment.doctor
        patient = get_object_or_404(Patient, user__username=appointment.patient)
        patient.prescriptions.add(prescription)
        appointment.delete()
        return super(treatPatientView, self).form_valid(form)


def load_users(request):
    user_email = request.GET.get('user_email')
    users = Patient.objects.filter(user__email=user_email).order_by('user__username')
    return render(request, 'doctor/user_dropdown_options.html', {'users': users})
