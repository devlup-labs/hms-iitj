from django.contrib import admin
from .models import Prescription, Appointment


class PrescriptionAdmin(admin.ModelAdmin):
    class Meta:
        model = Prescription


class AppointmentAdmin(admin.ModelAdmin):
    class Meta:
        model = Appointment


admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Prescription, PrescriptionAdmin)
