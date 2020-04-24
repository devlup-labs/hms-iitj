from django.urls import path
from .views_doctor import treatPatientView
from .views_patient import makeAppointment

app_name = 'hc'

urlpatterns = [
    path('treatPatient/', treatPatientView.as_view(template_name="doctor/treat_patient.html"),
         name='prescription'),
    path('makeAppointment/', makeAppointment, name='makeAppointment'),
]
