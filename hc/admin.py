from django.contrib import admin
from .models import Prescription, Appointment, DoctorSpecialization


class PrescriptionAdmin(admin.ModelAdmin):
    class Meta:
        model = Prescription


class AppointmentAdmin(admin.ModelAdmin):
    class Meta:
        model = Appointment


class DoctorSpecializationAdmin(admin.ModelAdmin):
    class Meta:
        model = DoctorSpecialization


admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Prescription, PrescriptionAdmin)
admin.site.register(DoctorSpecialization, DoctorSpecializationAdmin)
