from django.contrib.auth import views as auth_views
from .views import CustomLoginView
from hc.views_patient import viewMedicalHistory, CreateProfileView
from django.urls import path, include

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(template_name="accounts/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='main:home'), name='logout'),
    path('create_profile/', CreateProfileView.as_view(), name='createProfile'),
    path('history/', viewMedicalHistory.as_view(), name='history'),
    path('api/', include('accounts.api.urls'))
]
