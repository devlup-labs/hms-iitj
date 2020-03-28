from django.urls import path
from django.conf.urls import url
from .views import IndexPage, blogDetails

app_name = 'main'

urlpatterns = [
    path('', IndexPage, name='home'),
    url(r'^(?P<pk>\d+)/$', blogDetails, name='blogDetails'),
]
