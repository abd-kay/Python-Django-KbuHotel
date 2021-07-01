from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from hotel.models import Room, Category
from reservation.models import Booking, BookingForm


def index(request):
    return HttpResponse("reservation page")


@login_required(login_url='/login')
def addtobooking(request,id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information

    checkroom = Booking.objects.filter(room_id=id)
    if checkroom:
        control = 1
    else:
        control = 0

    if request.method == 'POST':  # if there is a post
        form = BookingForm(request.POST)
        if form.is_valid():
            if control == 1:
                data = Booking.objects.get(room_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()  # save data
            else:
                data = Booking()
                data.user_id = current_user.id
                data.room_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, "Room successfully booked ")
        return HttpResponseRedirect(url)

    else:  # if there is no post
        if control == 1:  # Update  booking
            data = Booking.objects.get(room_id=id)
            data.quantity += 1
            data.save()  #
        else:  # Inser to booking
            data = Booking()
            data.user_id = current_user.id
            data.room_id = id
            data.quantity = 1
            data.save()  #
        messages.success(request, "Room successfully booked")
        return HttpResponseRedirect(url)


def booking(request):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    booking = Booking.objects.filter(user_id=current_user.id)
    total=0
    for rs in booking:
        total += rs.room.price * rs.quantity
    #return HttpResponse(str(total))
    context={'booking': booking,
             'category':category,
             'total': total,
             }
    return render(request,'booking_rooms.html',context)



@login_required(login_url='/login') # Check login
def deletefrombooking(request,id):
    Booking.objects.filter(id=id).delete()
    messages.success(request, "Your Room deleted form Booking.")
    return HttpResponseRedirect("/booking")