from django.urls import path
from .views_doctor import treatPatientView, patientHistoryView
from .views_patient import makeAppointment, viewMedicalHistory, CreateProfileView


app_name = 'hc'

urlpatterns = [
    path('treatPatient/', treatPatientView.as_view(template_name="doctor/treat_patient.html"),
         name='prescription'),
    path('makeAppointment/', makeAppointment, name='makeAppointment'),
    path('create_profile/', CreateProfileView.as_view(), name='createProfile'),
    path('history/', viewMedicalHistory.as_view(), name='history'),
    path('<str:ldap>/history', patientHistoryView.as_view(), name='patient'),

]
