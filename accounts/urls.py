from django.contrib.auth import views as auth_views
from .views import CustomLoginView, CreateProfileView
from django.urls import path, include
# from

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(template_name="accounts/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='main:home'), name='logout'),
    path('create_profile/', CreateProfileView.as_view(), name='createProfile'),
    path('api/', include('accounts.api.urls'))
]
