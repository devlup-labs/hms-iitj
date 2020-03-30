from django.contrib import admin
from .models import Patient, Doctor, Appointment


class PatientAdmin(admin.ModelAdmin):
    class Meta:
        model = Patient


class DoctorAdmin(admin.ModelAdmin):
    class Meta:
        model = Doctor


class AppointmentAdmin(admin.ModelAdmin):
    class Meta:
        model = Appointment


admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Appointment, AppointmentAdmin)
# admin.site.register(Patient)
