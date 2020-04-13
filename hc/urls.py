from django.conf.urls import url
from django.urls import path
# from django.contrib.auth import views as auth_views
from .views import takeAppointmentView, treatPatientView, SearchPatientView

app_name = 'hc'

urlpatterns = [
    url(r'appointment$', takeAppointmentView, name='take_appointment'),
    path('treatPatient/', treatPatientView.as_view(template_name="hc/treat_patient.html"),
         name='prescription'),
    path('search_patient/', SearchPatientView.as_view(), name='search_patient')
]
