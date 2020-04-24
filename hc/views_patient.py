from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.contrib import messages
from accounts.models import Patient, Doctor
from .models import Appointment
from .forms_patient import CreateProfileIITForm, takeAppointmentForm


class viewMedicalHistory(TemplateView):
    template_name = "patient/medical_history.html"

    def get_context_data(self, **kwargs):
        context = super(viewMedicalHistory, self).get_context_data(**kwargs)
        patient = get_object_or_404(Patient, user=self.request.user)
        context['patient'] = patient
        context['history'] = patient.prescriptions.all()
        return context


class CreateProfileView(CreateView):
    form_class = CreateProfileIITForm
    template_name = 'patient/create_profile.html'
    success_url = '/'

    def form_valid(self, form):
        user = self.request.user
        user.username = user.email
        user.save()
        userprofile = form.save()
        userprofile.user = user
        userprofile.save()
        messages.success(
            self.request,
            "Profile was successfully created.",
            extra_tags='col-10 col-lg-12 d-flex justify-content-center alert alert-success alert-dismissible fade show')
        return super(CreateProfileView, self).form_valid(form)


def makeAppointment(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    if request.method == "POST":
        form = takeAppointmentForm(request.POST)
        if form.is_valid():
            specialization = form['specialization'].value()
            available_doctors = list(Doctor.objects.all().filter(available=True, specialization=specialization))[0]
            patient = get_object_or_404(Patient, user__email=request.user.email)
            time = form['time'].value()
            date = form['date'].value()
            Appointment.objects.create(patient=patient.user.email, doctor=available_doctors, time=time, date=date)
            messages.success(
                request,
                "Appointment was successfully created.",
                extra_tags='col-10 col-lg-12 d-flex justify-content-center alert alert-success alert-dismissible fade show')
        return HttpResponseRedirect("/")
    else:
        form = takeAppointmentForm()
        return render(request, 'patient/create_appointment.html', {'form': form})
