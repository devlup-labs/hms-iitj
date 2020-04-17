from django.urls import path
from .views import treatPatientView, makeAppointment

app_name = 'hc'

urlpatterns = [
    path('treatPatient/', treatPatientView.as_view(template_name="hc/treat_patient.html"),
         name='prescription'),
    path('makeAppointment/', makeAppointment, name='makeAppointment'),
]
