from django.contrib import admin
from .models import FlightInformation

# Register your models here.

@admin.register(FlightInformation)
class FlightInformationModel(admin.ModelAdmin):
    list_filter = ('ride_type', 'flight_time', 'flight_date', 'dropoff_point', 'airline')
    list_display = ('ride_type', 'flight_time', 'flight_date', 'dropoff_point', 'airline')