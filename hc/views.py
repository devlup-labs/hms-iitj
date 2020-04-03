from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import CreateView
# from .forms import writePrescription
from accounts.models import Doctor, Patient, Appointment
from .models import Prescription
from .forms import takeAppointmentForm, writePrescriptionForm


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

class writePrescriptionView(CreateView):
    form_class = writePrescriptionForm
    template_name = 'hc/write_prescription.html'
    success_url = '/hc/treatPatient/'

    def form_valid(self, form):
        appointment = Appointment.objects.filter().order_by('time')[0]
        prescription = form.save()
        appointment.prescription = prescription
        appointment.patient.prescriptions.add(prescription)
        