from django.urls import path, re_path
from hc.views.views_doctor import treatPatientView, patientHistoryView, load_users
from hc.views.views_patient import (
    makeAppointment, viewMedicalHistory, CreateProfileView, updateProfileView, AddFamilyMemberView, cancelAppointment
)
from hc.views.views_receptionist import SearchAppointmentView
from hc.views.views_pharmacist import ViewPrescription
app_name = 'hc'

urlpatterns = [
    path('treatPatient/', treatPatientView.as_view(template_name="doctor/treat_patient.html"),
         name='prescription'),
    path('makeAppointment/', makeAppointment, name='makeAppointment'),
    re_path(r'^cancelAppointment/(?P<pk>[0-9]+)/$', cancelAppointment, name='cancelAppointment'),
    path('create_profile/', CreateProfileView.as_view(), name='createProfile'),
    path('update_profile/', updateProfileView, name='updateProfile'),
    path('add_member/', AddFamilyMemberView, name='add_member'),
    path('history/', viewMedicalHistory.as_view(), name='history'),
    path('<str:username>/history/', patientHistoryView.as_view(), name='patient'),
    path('<str:username>/appointment/', SearchAppointmentView, name='appointment'),  # receptionist
    path('<str:username>/prescription/', ViewPrescription, name='view_prescription'),  # pharmacist
    path('ajax/load_users/', load_users, name='ajax_load_users'),  # ajax load users(family members) from email id of ward

]
