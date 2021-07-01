from django.contrib import admin

# Register your models here.
from reservation.models import Booking, ReservationRoom, Reservation


class ReservationRoomline(admin.TabularInline):
    model = ReservationRoom
    readonly_fields = ('user', 'room','price','quantity','amount')
    can_delete = False
    extra = 0


class ReservationAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name','phone','city','total','status']
    list_filter = ['status']
    readonly_fields = ('user','address','city','country','phone','first_name','ip', 'last_name','phone','city','total')
    can_delete = False
    inlines = [ReservationRoomline]

class ReservationRoomAdmin(admin.ModelAdmin):
    list_display = ['user', 'room','price','quantity','amount']
    list_filter = ['user']

class BookingAdmin(admin.ModelAdmin):
    list_display = ['room','user','quantity','price','amount' ]
    list_filter = ['user']


admin.site.register(Reservation,ReservationAdmin)
admin.site.register(ReservationRoom,ReservationRoomAdmin)
admin.site.register(Booking,BookingAdmin)
