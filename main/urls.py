from django.urls import path
from django.conf.urls import url
from .views import IndexView, BlogDetails, AddBlogView

app_name = 'main'

urlpatterns = [
    path('', IndexView, name='home'),
    url(r'^(?P<pk>\d+)/$', BlogDetails, name='BlogDetails'),
    path('addblog/', AddBlogView.as_view(), name='AddBlog'),
    # path('doctor/', DoctorsView.as_view(), name='doctor')
]
