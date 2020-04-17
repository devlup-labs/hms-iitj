from django.urls import path
from .views import treatPatientView

app_name = 'hc'

urlpatterns = [
    path('treatPatient/', treatPatientView.as_view(template_name="hc/treat_patient.html"),
         name='prescription'),
]
