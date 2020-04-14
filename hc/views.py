from accounts.models import Doctor, Patient
from .forms import takeAppointmentForm, treatPatientForm, SearchPatientForm
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import CreateView
from django.views.generic.base import View
# from .forms import treatPatient
import datetime as dt
from.models import Appointment


def takeAppointmentView(request):
    if request.method == 'POST':
        form = takeAppointmentForm(request.POST)
        if form.is_valid():
            specialization = form['specialization'].value()
            available_doctors = list(Doctor.objects.all().filter(available=True, specialization=specialization))[0]
            patient = get_object_or_404(Patient, user=request.user)
            time = form['time'].value()
            date = form['date'].value()
            Appointment.objects.create(patient=patient, doctor=available_doctors, time=time, date=date)
            return redirect('main:home')
    else:
        form = takeAppointmentForm()

    return render(request, 'hc/create_appointment.html', {'form': form})


class treatPatientView(CreateView):
    form_class = treatPatientForm
    template_name = 'hc/treat_patient.html'
    success_url = '/'
    super_context = {}

    def get_context_data(self, *args, **kwargs):
        context = super(treatPatientView, self).get_context_data(*args, **kwargs)
        for appointment in Appointment.objects.filter().order_by('date', 'time'):    # first sorted by date and then time
            if(appointment.date < dt.date.today()):
                appointment.delete()
            elif(appointment.date == dt.date.today()
                 and appointment.time < (dt.datetime.now()-dt.timedelta(minutes=30)).time()
                 and (dt.datetime.now()-dt.timedelta(minutes=30)).date() >= appointment.date):
                appointment.delete()
            else:
                break
        email = self.request.POST.get('email', False)
        if email:
            context['email'] = email
            self.super_context['email'] = email
            try:
                appointment = Appointment.objects.filter(patient__user__username=email).order_by('date', 'time')[0]
            except IndexError:
                appointment = None
        else:
            appointment = Appointment.objects.filter().order_by('date', 'time')[0]
        context['appointment'] = appointment
        self.super_context['appointment'] = appointment
        return context

    def form_valid(self, form, **kwargs):
        context = self.super_context
        if context['email']:
            email = context['email']
            try:
                appointment = Appointment.objects.filter(patient__user__username=email).order_by('date', 'time')[0]
            except IndexError:
                appointment = None
        else:
            appointment = Appointment.objects.filter().order_by('date', 'time')[0]
        prescription = form.save()
        prescription.doctor = appointment.doctor
        appointment.patient.prescriptions.add(prescription)
        appointment.delete()
        return super(treatPatientView, self).form_valid(form)


class SearchPatientView(View):
    form_class = SearchPatientForm()
    template_name = 'hc/treat_patient.html'
    success_url = 'treatPatient/'

    def post(self, request, *args, **kwargs):
        form = SearchPatientForm(request.POST)
        if form.is_valid():
            email = form['email'].value()
            appointment = get_object_or_404(Appointment, patient__user__username=email)
            prescription = form.save()
            prescription.doctor = appointment.doctor
            appointment.patient.prescriptions.add(prescription)
            appointment.delete()
            return super(SearchPatientView, self).form_valid(form)
