from accounts.models import Doctor, Patient
from .forms import takeAppointmentForm, treatPatientForm
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import CreateView
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
    success_url = '/hc/treatPatient/'

    def get_context_data(self, *args, **kwargs):
        context = super(treatPatientView, self).get_context_data(*args, **kwargs)
        for appointment in Appointment.objects.filter().order_by('time'):
            if(appointment.date < dt.date.today()):
                appointment.delete()
            elif(appointment.date == dt.date.today()
                 and appointment.time < (dt.datetime.now()-dt.timedelta(minutes=30)).time()):
                appointment.delete()
            else:
                break
        appointment = Appointment.objects.filter().order_by('time')[0]
        context['appointment'] = appointment
        return context

    def form_valid(self, form):
        appointment = Appointment.objects.filter().order_by('time')[0]
        prescription = form.save()
        prescription.doctor = appointment.doctor
        appointment.patient.prescriptions.add(prescription)
        appointment.delete()
        return super(treatPatientView, self).form_valid(form)
