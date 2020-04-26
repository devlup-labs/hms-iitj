from django.contrib.auth import views as auth_views
from .views import CustomLoginView
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(template_name="accounts/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='main:home'), name='logout'),
    # path('api/', include('accounts.api.urls'))
]
