from django.urls import path
from django.conf.urls import url
from .views import IndexView, blogDetails, AddBlogView

app_name = 'main'

urlpatterns = [
    path('', IndexView, name='home'),
    url(r'^(?P<pk>\d+)/$', blogDetails, name='blogDetails'),
    path('addblog/', AddBlogView.as_view(), name='addBlog'),
    # path('doctor/', DoctorsView.as_view(), name='doctor')
]
