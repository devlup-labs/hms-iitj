#app/urls.py

from django.conf.urls import url
from app import views
app_name="app"
urlpatterns=[
    url(r'^register/$', views.register, name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
]