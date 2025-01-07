from django.contrib import admin
from .models import Service, Appointment

admin.site.register(Service)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'service', 'date', 'time', 'status')
    list_filter = ('service', 'status')
    search_fields = ('name', 'email', 'phone_number')

