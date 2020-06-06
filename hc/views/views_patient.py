from django.views.generic import TemplateView, CreateView
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import Patient, Doctor
from hc.models import Appointment
from hc.forms.forms_patient import CreateProfileForm, takeAppointmentForm, AddFamilyMemberForm
import subprocess
from hc.event import create_event
from django.contrib.auth.models import User


class viewMedicalHistory(TemplateView):
    template_name = "patient/medical_history.html"

    def get_context_data(self, **kwargs):
        context = super(viewMedicalHistory, self).get_context_data(**kwargs)
        patients = Patient.objects.all().filter(user__email=self.request.user.email)
        context['patients'] = patients
        return context


class CreateProfileView(LoginRequiredMixin, CreateView):
    login_url = '/auth/google/login'
    redirect_field_name = 'hc:createProfile'
    form_class = CreateProfileForm
    template_name = 'patient/create_profile.html'
    success_url = '/'

    def form_valid(self, form):
        user = self.request.user
        userprofile = form.save()
        userprofile.user = user

        result = subprocess.check_output(['java', 'LDAP_API.java', user.username])
        result = result.decode('utf-8')
        if(result == "0"):
            return HttpResponse("User {} does not exists.".format(user))
        elif(result == "faculty" or result == "staff" or result == "project"):
            userprofile.staff = True

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
                patient = get_object_or_404(Patient, user__username=request.user.username)
                time = form['time'].value()
                date = form['date'].value()
                Appointment.objects.create(patient=patient.user.username, doctor=available_doctors, time=time, date=date)

                create_event(patient.user.email, date, time, available_doctors)

                messages.success(
                    request,
                    "Appointment was successfully created.",
                    extra_tags='d-flex justify-content-center alert\
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


@login_required(login_url="/auth/google/login/")
@user_passes_test(lambda u: Patient.objects.get(user__username=u.username).staff)
def AddFamilyMemberView(request):
    if request.method == "POST":
        form = AddFamilyMemberForm(request.POST)
        if form.is_valid():
            email = request.user.email
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = first_name.lower() + "__" + email
            user = User.objects.create_user(username=username, email=username, first_name=first_name, last_name=last_name)
            user.email = email
            user.save()

            form.save(user=user)
            messages.success(
                request,
                "Dependant was successfully added.",
                extra_tags='d-flex justify-content-center alert alert-success alert-dismissible fade show')
            return redirect('main:home')
    else:
        form = AddFamilyMemberForm()

    return render(request, 'patient/add_member.html', {'form': form})
