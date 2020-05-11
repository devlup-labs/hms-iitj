from django.urls import path
from django.conf.urls import url
from .views import IndexView
from main.views import BlogDetails, AddBlogView, DevelopersPage
from hc.views_receptionist import IndexViewReceptionist
from hc.views_pharmacist import IndexViewPharmacist

app_name = 'main'

urlpatterns = [
    path('', IndexView, name='home'),
    path('receptionist/', IndexViewReceptionist, name='home_receptionist'),
    path('pharmacist/', IndexViewPharmacist, name='home_pharmacist'),
    url(r'^(?P<pk>\d+)/$', BlogDetails, name='BlogDetails'),
    path('addblog/', AddBlogView.as_view(), name='AddBlog'),
    path('developers/', DevelopersPage, name='developers'),

]
