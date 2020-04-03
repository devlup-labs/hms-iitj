from django.conf.urls import url
from django.urls import path
# from django.contrib.auth import views as auth_views
from .views import takeAppointmentView, writePrescriptionView

app_name = 'hc'

urlpatterns = [
    url(r'appointment$', takeAppointmentView, name='take_appointment'),
    path('writePrescription/', writePrescriptionView.as_view(template_name="hc/write_prescription.html"),
         name='prescription'),
]
