from django.urls import path
from django.conf.urls import url
from .views import IndexView
from hc.views_patient import BlogDetails
from hc.views_doctor import AddBlogView

app_name = 'main'

urlpatterns = [
    path('', IndexView, name='home'),
    url(r'^(?P<pk>\d+)/$', BlogDetails, name='BlogDetails'),
    path('addblog/', AddBlogView.as_view(), name='AddBlog'),
]
