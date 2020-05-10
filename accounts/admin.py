from django.contrib import admin
from .models import Patient, Doctor, Receptionist, Pharmacist


class PatientAdmin(admin.ModelAdmin):
    class Meta:
        model = Patient


class DoctorAdmin(admin.ModelAdmin):
    class Meta:
        model = Doctor


class ReceptionistAdmin(admin.ModelAdmin):
    class Meta:
        model = Receptionist


class PharmacistAdmin(admin.ModelAdmin):
    class Meta:
        model = Pharmacist


admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Receptionist, ReceptionistAdmin)
admin.site.register(Pharmacist, PharmacistAdmin)
