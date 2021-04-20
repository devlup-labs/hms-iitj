from django.urls import path, include
from django.conf.urls import url
from .views import IndexView
from main.views import BlogDetailsView, AddBlogView, DevelopersPage, EditBlogView
from hc.views.views_receptionist import IndexViewReceptionist, AppointmentsOfDoctor
from hc.views.views_pharmacist import IndexViewPharmacist
from hc.views.views_doctor import IndexViewDoctor

app_name = 'main'

urlpatterns = [
    path('', IndexView, name='home'),
    path('doctor/', IndexViewDoctor, name='home_doctor'),
    path('receptionist/', IndexViewReceptionist, name='home_receptionist'),
    path('receptionist/appointments/<str:doc_name>', AppointmentsOfDoctor, name='recep_appointments'),
    path('pharmacist/', IndexViewPharmacist, name='home_pharmacist'),
    url(r'^blogs/(?P<slug>[\w-]+)/$', BlogDetailsView.as_view(), name='blog_details'),
    url(r'^blogs/edit/(?P<slug>[\w-]+)/$', EditBlogView, name='edit_blog'),
    path('addblog/', AddBlogView.as_view(), name='AddBlog'),
    path('developers/', DevelopersPage, name='developers'),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),

]
