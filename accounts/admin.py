from django.contrib import admin
from .models import Patient, Doctor


class PatientAdmin(admin.ModelAdmin):
    class Meta:
        model = Patient


class DoctorAdmin(admin.ModelAdmin):
    class Meta:
        model = Doctor


admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)

# admin.site.register(Patient)
