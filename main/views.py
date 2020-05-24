from django.views.generic import CreateView, DetailView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse
from main.models import Blog
from accounts.models import Doctor
from hc.models import Appointment
from hc.forms.forms_patient import takeAppointmentForm
from hc.forms.forms_doctor import SearchPatientForm
from main.forms import AddBlogForm
from hc.views.views_patient import makeAppointment


def IndexView(request):
    blogs = Blog.objects.all()
    appn = None

    if request.user.is_authenticated:
        if hasattr(request.user, 'doctor'):
            form = SearchPatientForm()
            return render(request, 'doctor/index.html', {'form': form})
        elif hasattr(request.user, 'receptionist'):
            return redirect('main:home_receptionist')
        elif hasattr(request.user, 'pharmacist'):
            return redirect('main:home_pharmacist')
        appn = Appointment.objects.all().filter(patient=request.user.email).order_by('date', 'time')
        if not hasattr(request.user, 'patient'):
            return redirect('hc:createProfile')

    if request.method == 'POST':
        return makeAppointment(request)

    form = takeAppointmentForm()
    return render(request, 'main/index.html', {'form': form, 'blogs': blogs, 'user': request.user, 'appointments': appn})


class BlogDetailsView(DetailView):
    model = Blog
    template_name = 'main/blog_details.html'
    context_object_name = 'blog'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super(BlogDetailsView, self).get_context_data(**kwargs)
        return context

    def get_absolute_url(self):
        return reverse('main:blog_details', kwargs={'slug': self.slug})


class AddBlogView(SuccessMessageMixin, UserPassesTestMixin, CreateView):
    template_name = 'main/add_blog.html'
    form_class = AddBlogForm
    success_url = '/'
    extra_tags = 'd-flex justify-content-center alert alert-success alert-dismissible fade show'

    def test_func(self):
        return self.request.user.groups.filter(name='doctor').exists()

    def form_valid(self, form):
        form = form.save(commit=False)
        form.author = Doctor.objects.get(user=self.request.user)
        form.save()
        success_message = "Blog was successfully created."
        if success_message:
            messages.success(self.request, success_message, extra_tags=self.extra_tags)
        return redirect('main:home')


def DevelopersPage(request):
    return render(request, 'main/developers.html')
