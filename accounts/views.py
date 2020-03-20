from django.views.generic import CreateView
from .forms import SignupFormforIIT
from .models import Patient


class SignupView(CreateView):
    form_class = SignupFormforIIT
    template_name = 'accounts/signup.html'
    success_url = 'accounts/login/'

    def form_valid(self, form):
        data = self.request.POST.copy()
        form = SignupFormforIIT(data)
        user = form.save()
        user.username = data['email']
        user.save()
        SignupView.create_profile(user, **form.cleaned_data)
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
            roll_no=kwargs['roll_no'],
            phone_number=kwargs['phone_number'],
            emergency_phone=kwargs['emergency_phone'],
            blood_group=kwargs['blood_group'],
            height=kwargs['height'],
            weight=kwargs['weight'],
            birthday=kwargs['birthday'],
            past_diseases=kwargs['past_diseases'],
            other_diseases=kwargs['other_diseases'],
            allergies=kwargs['allergies'],
            
        )
        userprofile.save()

# class CustomLoginView(LoginView):
#     template_name = 'accounts/login.html'
#     redirect_authenticated_user = True
