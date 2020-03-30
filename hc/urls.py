from django.conf.urls import url
# from django.contrib.auth import views as auth_views
from .views import createAppointment

app_name = 'hc'

urlpatterns = [
    url(r'appointment$', createAppointment, name='take_appointment'),
]
