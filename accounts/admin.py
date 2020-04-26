from django.contrib import admin
from .models import Patient, Doctor, Receptionist


class PatientAdmin(admin.ModelAdmin):
    class Meta:
        model = Patient


class DoctorAdmin(admin.ModelAdmin):
    class Meta:
        model = Doctor


class ReceptionistAdmin(admin.ModelAdmin):
    class Meta:
        model = Receptionist


admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Receptionist, ReceptionistAdmin)
