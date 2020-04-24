from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .models import Blog
from hc.models import Appointment
from hc.forms_patient import takeAppointmentForm
from hc.forms_doctor import SearchPatientForm
from main.forms import AddBlogForm
from hc.views_patient import makeAppointment


def IndexView(request):
    blogs = Blog.objects.all()
    appn = Appointment.objects.all()

    if request.user.is_authenticated:
        if hasattr(request.user, 'doctor'):
            form = SearchPatientForm
            return render(request, 'doctor/index_doctor.html', {'form': form})
        elif hasattr(request.user, 'receptionist'):
            return render(request, 'receptionist/index_receptionist.html')
        # add pharmacist and admin fields here
        appn = appn.filter(patient=request.user.email).order_by('date', 'time')
        if not hasattr(request.user, 'patient'):
            return redirect('accounts:createProfile')

    if request.method == 'POST':
        return makeAppointment(request)

    form = takeAppointmentForm()
    return render(request, 'main/index.html', {'form': form, 'blogs': blogs, 'user': request.user, 'appointments': appn})


def BlogDetails(request, pk):
    blogs = Blog.objects.get(pk=pk)
    template_name = 'main/blog_details.html'
    return render(request, template_name, {'blog': blogs})


class AddBlogView(SuccessMessageMixin, CreateView):
    template_name = 'main/add_blog.html'
    form_class = AddBlogForm
    success_url = '/'
    success_message = 'Blog was successfully created.'
    extra_tags = 'd-flex justify-content-center alert alert-success alert-dismissible fade show'

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message, extra_tags=self.extra_tags)
        return response
