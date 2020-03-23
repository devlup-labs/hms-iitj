from django.urls import path
from .views import IndexView, AddBlog

app_name = 'main'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('addBlog/', AddBlog.as_view(), name='addBlog')
]
