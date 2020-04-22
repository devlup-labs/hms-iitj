from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView
from django.shortcuts import reverse, get_object_or_404
from django.contrib import messages
from .forms import CreateProfileIITForm
from .models import Patient
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
        messages.success(
            self.request,
            "Profile was successfully created.",
            extra_tags='col-10 col-lg-12 d-flex justify-content-center alert alert-success alert-dismissible fade show')
        return super(CreateProfileView, self).form_valid(form)


class viewMedicalHistory(TemplateView):
    template_name = "accounts/medical_history.html"

    def get_context_data(self, **kwargs):
        context = super(viewMedicalHistory, self).get_context_data(**kwargs)
        patient = get_object_or_404(Patient, user=self.request.user)
        context['patient'] = patient
        context['history'] = patient.prescriptions.all()
        return context
