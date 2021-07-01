from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm

from hotel.models import Room


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.room.title

    @property
    def price(self):
        return (self.room.price)

    @property
    def amount(self):
        return (self.quantity * self.room.price)


class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['quantity']


