from django.urls import path
from hc.views.views_doctor import treatPatientView, patientHistoryView
from hc.views.views_patient import makeAppointment, viewMedicalHistory, CreateProfileView, updateProfileView
from hc.views.views_receptionist import SearchAppointmentView
from hc.views.views_pharmacist import ViewPrescription


app_name = 'hc'

urlpatterns = [
    path('treatPatient/', treatPatientView.as_view(template_name="doctor/treat_patient.html"),
         name='prescription'),
    path('makeAppointment/', makeAppointment, name='makeAppointment'),
    path('create_profile/', CreateProfileView.as_view(), name='createProfile'),
    path('update_profile/', updateProfileView, name='updateProfile'),
    path('history/', viewMedicalHistory.as_view(), name='history'),
    path('<str:ldap>/history/', patientHistoryView.as_view(), name='patient'),
    path('<str:ldap>/appointment/', SearchAppointmentView, name='appointment'),
    path('<str:ldap>/prescription/', ViewPrescription, name='prescription'),

]
