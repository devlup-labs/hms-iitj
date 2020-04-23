from django.contrib.auth.views import LoginView
from django.shortcuts import reverse


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_redirect_url(self):
        url = super(CustomLoginView, self).get_redirect_url()
        return url or reverse('main:home')
