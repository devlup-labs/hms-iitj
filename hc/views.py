from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView
# from .forms import writePrescription
from accounts.models import Appointment, Doctor, Patient
from .forms import takeAppointment


class takeAppointmentView(CreateView):
    form_class = takeAppointment
    template_name = 'hc/create_appointment.html'
    success_url = '/'

    def form_valid(self, form):
        specialization = form['specialization'].value()
        available_doctors = list(Doctor.objects.all().filter(available=True, specialization=specialization))
        print(available_doctors)
        patient  = get_object_or_404(Patient, user=self.request.user)
        appointment = Appointment.objects.create(patient=patient, doctor=available_doctors[0])
        appointment.save()
        return super(takeAppointmentView, self).form_valid(form)




# def createAppointment(request):
#     appointment_form = takeAppointment(request.POST)
#     if request.method == 'POST':
#         user = request.user
#         specialization=appointment_form['specialization']
#         available_doctors = Doctor.objects.filter(available=True, specialization=specialization)
#         # appointment =
#         Appointment.objects.create(patient=user, doctor=available_doctors[0])
#         return redirect('hc:take_appointment')
#     return render(request, 'hc/create_appointment.html')
