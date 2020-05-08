from django.urls import path
from django.conf.urls import url
from .views import IndexView
from main.views import BlogDetails, AddBlogView
from hc.views_receptionist import IndexViewReceptionist

app_name = 'main'

urlpatterns = [
    path('', IndexView, name='home'),
    path('receptionist/', IndexViewReceptionist, name='home_receptionist'),
    url(r'^(?P<pk>\d+)/$', BlogDetails, name='BlogDetails'),
    path('addblog/', AddBlogView.as_view(), name='AddBlog'),
]
