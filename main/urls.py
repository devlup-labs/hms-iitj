from django.urls import path
from django.conf.urls import url
from .views import IndexView
from main.views import BlogDetailsView, AddBlogView, DevelopersPage
from hc.views.views_receptionist import IndexViewReceptionist
from hc.views.views_pharmacist import IndexViewPharmacist

app_name = 'main'

urlpatterns = [
    path('', IndexView, name='home'),
    path('receptionist/', IndexViewReceptionist, name='home_receptionist'),
    path('pharmacist/', IndexViewPharmacist, name='home_pharmacist'),
    url(r'^blogs/(?P<slug>[\w-]+)/$', BlogDetailsView.as_view(), name='blog_details'),
    path('addblog/', AddBlogView.as_view(), name='AddBlog'),
    path('developers/', DevelopersPage, name='developers'),

]
