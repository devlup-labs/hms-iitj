from django.contrib.auth import views as auth_views
from .views import SignupView, CustomLoginView
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignupView.as_view(template_name="accounts/signup.html"), name='signup'),
    path('login/', CustomLoginView.as_view(template_name="accounts/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='accounts:login'), name='logout'),
]
