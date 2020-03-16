from django.contrib import admin
from .models import Patient


class PatientAdmin(admin.ModelAdmin):
    class Meta:
        model = Patient


admin.site.register(Patient, PatientAdmin)
# admin.site.register(Patient)
