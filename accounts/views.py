from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.shortcuts import reverse
from .forms import SignUpOutsiderForm, CreateProfileIITForm
from .models import PatientOutsider, Patient
# from django.views.generic import View


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_redirect_url(self):
        url = super(CustomLoginView, self).get_redirect_url()
        return url or reverse('main:home')


class SignupOutsiderView(CreateView):
    form_class = SignUpOutsiderForm
    template_name = 'accounts/signup_outsider.html'
    success_url = '/accounts/login/'

    def form_valid(self, form):
        data = self.request.POST.copy()
        form = SignUpOutsiderForm(data)
        user = form.save()
        user.username = data['email']
        user.save()
        SignupOutsiderView.create_profile(user, **form.cleaned_data)
        return super(SignupOutsiderView, self).form_valid(form)

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    @staticmethod
    def create_profile(user=None, **kwargs):
        userprofile = PatientOutsider.objects.create(
            user=user,
            gender=kwargs['gender'],
            phone_number=kwargs['phone_number'],
            blood_group=kwargs['blood_group'],
        )
        userprofile.save()


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