from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import CreateView
from .models import blog
from accounts.models import Doctor, Patient
from hc.models import Appointment
from .forms import AddBlogForm
from hc.forms import takeAppointmentForm


def IndexView(request):
    blogs = blog.objects.all()
    if hasattr(request.user, 'doctor'):
        return render(request, 'main/doctors_home_page.html')
    else:
        if request.method == 'POST':
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            form = takeAppointmentForm(request.POST)
            if form.is_valid():
                specialization = form['specialization'].value()
                available_doctors = list(Doctor.objects.all().filter(available=True, specialization=specialization))[0]
                patient = get_object_or_404(Patient, user=request.user)
                time = form['time'].value()
                date = form['date'].value()
                Appointment.objects.create(patient=patient, doctor=available_doctors, time=time, date=date)
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
