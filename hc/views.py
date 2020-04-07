from accounts.models import Doctor, Patient
from .forms import takeAppointmentForm, treatPatientForm
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import CreateView
# from .forms import treatPatient
from.models import Appointment


def takeAppointmentView(request):
    if request.method == 'POST':
        form = takeAppointmentForm(request.POST)
        if form.is_valid():
            specialization = form['specialization'].value()
            available_doctors = list(Doctor.objects.all().filter(available=True, specialization=specialization))[0]
            patient = get_object_or_404(Patient, user=request.user)
            time = form['time'].value()
            Appointment.objects.create(patient=patient, doctor=available_doctors, time=time)
            return redirect('main:home')
    else:
        form = takeAppointmentForm()

    return render(request, 'hc/create_appointment.html', {'form': form})


class treatPatientView(CreateView):
    form_class = treatPatientForm
    template_name = 'hc/treat_patient.html'
    success_url = '/hc/treatPatient/'

    def form_valid(self, form):
        appointment = Appointment.objects.filter().order_by('time')[0]
        prescription = form.save({'appointment': appointment})
        prescription.doctor = appointment.doctor
        appointment.patient.prescriptions.add(prescription)
        appointment.delete()
        return super(treatPatientView, self).form_valid(form)
