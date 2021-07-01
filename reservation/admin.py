from django.contrib import admin

# Register your models here.
from reservation.models import Booking


class BookingAdmin(admin.ModelAdmin):
    list_display = ['room','user','quantity','price','amount' ]
    list_filter = ['user']



admin.site.register(Booking,BookingAdmin)
