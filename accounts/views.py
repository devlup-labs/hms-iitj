from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.shortcuts import reverse
from .forms import CreateProfileIITForm
# from django.views.generic import View


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_redirect_url(self):
        url = super(CustomLoginView, self).get_redirect_url()
        return url or reverse('main:home')


class CreateProfileView(CreateView):
    form_class = CreateProfileIITForm
    template_name = 'accounts/create_profile.html'
    success_url = '/'

    def form_valid(self, form):
        user = self.request.user
        user.username = user.email
        user.save()
        userprofile = form.save()
        userprofile.user = user
        userprofile.save()
        return super(CreateProfileView, self).form_valid(form)
