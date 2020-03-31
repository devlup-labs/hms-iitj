from django.conf.urls import url
# from django.contrib.auth import views as auth_views
from .views import takeAppointmentView

app_name = 'hc'

urlpatterns = [
    url(r'appointment$', takeAppointmentView, name='take_appointment'),
]
