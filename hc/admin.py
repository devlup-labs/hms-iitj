from django.contrib import admin
from .models import Prescription


class PrescriptionAdmin(admin.ModelAdmin):
    class Meta:
        model = Prescription


admin.site.register(Prescription, PrescriptionAdmin)
