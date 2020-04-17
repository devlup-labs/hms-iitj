from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import CreateView
from .models import blog
from accounts.models import Doctor, Patient
from hc.models import Appointment
from .forms import AddBlogForm
from hc.forms import takeAppointmentForm, SearchPatientForm
from hc.views import makeAppointment


def IndexView(request):
    blogs = blog.objects.all()

    if request.user.is_authenticated:
        if hasattr(request.user, 'doctor'):
            number = Appointment.objects.all().count()
            form = SearchPatientForm
            return render(request, 'main/doctors_home_page.html', {'number': number, 'form': form})
        # add pharmacist, receptionist fields here
        if not hasattr(request.user, 'patient'):
            return redirect('accounts:createProfile')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        form = takeAppointmentForm(request.POST)
        makeAppointment(form, request.user.email)
        return render(request, 'main/index.html', {'form': form, 'blogs': blogs})
    else:
        form = takeAppointmentForm()
        return render(request, 'main/index.html', {'form': form, 'blogs': blogs})


def blogDetails(request, pk):
    blogs = blog.objects.get(pk=pk)
    template_name = 'main/blogDetails.html'
    return render(request, template_name, {'blog': blogs})


class AddBlogView(CreateView):
    template_name = 'main/addBlog.html'
    form_class = AddBlogForm
    success_url = '/'
