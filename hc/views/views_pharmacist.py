from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.models import Patient
from hc.forms.forms_pharmacist import ViewPrescriptionForm


@login_required(login_url="/accounts/login/")
@user_passes_test(lambda u: u.groups.filter(name='pharmacist').exists())
def IndexViewPharmacist(request):
    if request.method == "POST":
        email = request.POST.get('email', False)
        ldap = email[:-len('@iitj.ac.in')]
        return redirect('hc:prescription', ldap=ldap)
    else:
        return render(request, 'pharmacist/index.html')


@login_required(login_url="/accounts/login/")
@user_passes_test(lambda u: u.groups.filter(name='pharmacist').exists())
def ViewPrescription(request, ldap):
    email = ldap + '@iitj.ac.in'
    patient = Patient.objects.filter(user__email=email)[0]
    pres = patient.prescriptions.filter(utilised=False).latest('created_at')
    if request.method == "POST":
        form = ViewPrescriptionForm(request.POST, instance=pres)
        form.save()
        return redirect('main:home')
    form = ViewPrescriptionForm(instance=pres)
    return render(request, 'pharmacist/prescription.html', {'form': form})
