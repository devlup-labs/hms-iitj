from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from .models import Blog
from hc.models import Appointment
from .forms import AddBlogForm
from hc.forms import takeAppointmentForm, SearchPatientForm
from hc.views import makeAppointment


def IndexView(request):
    blogs = Blog.objects.all()
    appn = Appointment.objects.all()

    if request.user.is_authenticated:
        if hasattr(request.user, 'doctor'):
            number = appn.count()
            form = SearchPatientForm
            return render(request, 'main/doctors_home_page.html', {'number': number, 'form': form})
        elif hasattr(request.user, 'receptionist'):
            return render(request, 'main/receptionists_home.html')
        # add pharmacist fields here
        appn = appn.filter(patient=request.user.email).order_by('date', 'time')
        if not hasattr(request.user, 'patient'):
            return redirect('accounts:createProfile')

    if request.method == 'POST':
        makeAppointment(request)
        return HttpResponseRedirect("/")

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
    success_message = "Blog was successfully created."
