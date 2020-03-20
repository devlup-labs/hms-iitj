from django.views.generic import CreateView
from .forms import SignupFormforIIT
from .models import Patient


class SignupView(CreateView):
    form_class = SignupFormforIIT
    template_name = 'accounts/signup.html'
    success_url = '/login/'

    def form_valid(self, form):
        data = self.request.POST.copy()
        data['username'] = data['email']
        form = SignupFormforIIT(data)
        user = form.save()
        SignupView.create_profile(user, **form.cleaned_data)
        # messages.success(self.request, 'Hi %s,' % user.get_full_name())
        print("hi")
        return super(SignupView, self).form_valid(form)

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    @staticmethod
    def create_profile(user=None, **kwargs):
        userprofile = Patient.objects.create(
            user=user,
            gender=kwargs['gender'],
            phone_number=kwargs['phone_number'],
            bloodgroup=kwargs['bloodgroup'],
            birthdate=kwargs['birthdate']
        )
        userprofile.save()

# class CustomLoginView(LoginView):
#     template_name = 'accounts/login.html'
#     redirect_authenticated_user = True
