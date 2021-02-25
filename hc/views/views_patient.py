from django.views.generic import TemplateView, CreateView
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import Patient, Doctor
from hc.models import Appointment
from hc.forms.forms_patient import CreateProfileForm, takeAppointmentForm, AddFamilyMemberForm
from hc.event import create_event
from django.contrib.auth.models import User
import subprocess
import datetime as dt
from django.utils.timezone import make_aware


class viewMedicalHistory(TemplateView):
    template_name = "patient/medical_history.html"

    def get_context_data(self, **kwargs):
        context = super(viewMedicalHistory, self).get_context_data(**kwargs)
        patients = Patient.objects.all().filter(user__email=self.request.user.email)

        patientData = []

        for i in range(len(patients)):
            readablePres = []
            for prescription in patients[i].prescriptions.all():
                prescription.remarks = prescription.ENCRYPTER.decrypt(prescription.remarks.encode('utf-8')).decode('utf-8')
                readablePres.append(prescription)
            patientData.append([patients[i], readablePres])

        context['patientData'] = patientData
        context['staff'] = Patient.objects.get(user=self.request.user).staff

        return context


class CreateProfileView(LoginRequiredMixin, CreateView):
    login_url = '/auth/google/login'
    redirect_field_name = 'hc:createProfile'
    form_class = CreateProfileForm
    template_name = 'patient/create_profile.html'
    success_url = '/'

    def form_valid(self, form):
        result = 0
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
            doctor = form['doctor'].value()
            try:
                available_doctor = Doctor.objects.filter(available=True, id=doctor)[0]
                patient = get_object_or_404(Patient, user__username=request.user.username)
                time = form['time'].value()
                date = form['date'].value()

                # checking for the conflicts in appn time
                appn_dt_str = date + " " + time
                appn_dt_obj = dt.datetime.strptime(appn_dt_str, "%Y-%m-%d %H:%M")
                block_time_start = appn_dt_obj - dt.timedelta(minutes=19)
                block_time_end = appn_dt_obj + dt.timedelta(minutes=20)

                conflict = Appointment.objects.filter(time__range=(block_time_start, block_time_end))

                if conflict:
                    messages.error(
                        request,
                        "Time slot is not available.",
                        extra_tags='d-flex justify-content-center alert alert-danger alert-dismissible fade show')
                else:
                    appn_dt_obj = make_aware(appn_dt_obj)  # to convert naive date time to aware datetime
                    Appointment.objects.create(patient=patient.user.username, doctor=available_doctor, time=appn_dt_obj)
                    create_event(patient.user.email, date, time, available_doctor)
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
        if form.is_valid():
            messages.success(
                    request,
                    "Profile was successfully updated.",
                    extra_tags='d-flex justify-content-center alert\
                                 alert-success alert-dismissible fade show')
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

            dependant = form.save(user=user)
            dependant.num = get_object_or_404(Patient, user__username=request.user).num
            dependant.save()
            messages.success(
                request,
                "Dependant was successfully added.",
                extra_tags='d-flex justify-content-center alert alert-success alert-dismissible fade show')
            return redirect('main:home')
    else:
        form = AddFamilyMemberForm()

    return render(request, 'patient/add_member.html', {'form': form})
