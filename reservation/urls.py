from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addtobooking/<int:id>', views.addtobooking, name='addtobooking'),
    path('reservationroom', views.reservationroom, name='reservationroom'),
    path('deletefrombooking/<int:id>', views.deletefrombooking, name='deletefrombooking'),

]
