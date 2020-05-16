from django.views.generic import TemplateView, CreateView
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import Patient, Doctor
from hc.models import Appointment
from hc.forms.forms_patient import CreateProfileForm, takeAppointmentForm


class viewMedicalHistory(TemplateView):
    template_name = "patient/medical_history.html"

    def get_context_data(self, **kwargs):
        context = super(viewMedicalHistory, self).get_context_data(**kwargs)
        patient = get_object_or_404(Patient, user=self.request.user)
        context['patient'] = patient
        context['history'] = patient.prescriptions.all()
        return context


class CreateProfileView(LoginRequiredMixin, CreateView):
    login_url = '/auth/google/login'
    redirect_field_name = 'hc:createProfile'
    form_class = CreateProfileForm
    template_name = 'patient/create_profile.html'
    success_url = '/'

    def form_valid(self, form):
        user = self.request.user
        user.username = user.email.split("@")[0]
        group = Group.objects.get(name="patient")
        user.groups.add(group)
        user.save()
        userprofile = form.save()
        userprofile.user = user
        userprofile.save()
        messages.success(
            self.request,
            "Profile was successfully created.",
            extra_tags='d-flex justify-content-center alert alert-success alert-dismissible fade show')
        return super(CreateProfileView, self).form_valid(form)


@login_required(login_url="/auth/google/login/")
@user_passes_test(lambda u: u.groups.filter(name='patient').exists())  # give access to this view to receptionist too
def makeAppointment(request):

    if request.method == "POST":
        form = takeAppointmentForm(request.POST)
        if form.is_valid():
            specialization = form['specialization'].value()
            try:
                available_doctors = list(Doctor.objects.all().filter(available=True, specialization=specialization))[0]
                patient = get_object_or_404(Patient, user__email=request.user.email)
                time = form['time'].value()
                date = form['date'].value()
                Appointment.objects.create(patient=patient.user.email, doctor=available_doctors, time=time, date=date)
                messages.success(
                    request,
                    "Appointment was successfully created.",
                    extra_tags='col-10 col-lg-12 d-flex justify-content-center alert\
                                 alert-success alert-dismissible fade show')
            except:
                messages.error(
                    request,
                    "No Doctors Available.",
                    extra_tags='d-flex justify-content-center alert alert-danger alert-dismissible fade show')
        return HttpResponseRedirect("/")
    else:
        form = takeAppointmentForm()
        return render(request, 'patient/create_appointment.html', {'form': form})


def updateProfileView(request):
    patient = get_object_or_404(Patient, user__username=request.user.username)
    form = CreateProfileForm(instance=patient)
    if(request.method == "POST"):
        form = CreateProfileForm(request.POST, instance=patient)
        form.save()
        return redirect("main:home")
    return render(request, "patient/update_profile.html", {'form': form})
