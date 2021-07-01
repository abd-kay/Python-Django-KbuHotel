from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.crypto import get_random_string

from hotel.models import Room, Category
from reservation.models import Booking, BookingForm, ReservationForm, ReservationRoom, Reservation
from user.models import UserProfile


def index(request):
    return HttpResponse("reservation page")

def reservationroom(request):
    category = Category.objects.all()
    current_user = request.user
    booking = Booking.objects.filter(user_id=current_user.id)
    total = 0
    for rs in booking:
        total += rs.room.price * rs.quantity

    if request.method == 'POST':  # if there is a post
        form = ReservationForm(request.POST)
        # return HttpResponse(request.POST.items())
        if form.is_valid():
            # Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
            # ..............

            data = Reservation()
            data.first_name = form.cleaned_data['first_name']  # get room quantity from form
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            roomcode = get_random_string(5).upper()  # random cod
            data.code = roomcode
            data.save()  #

            booking = Booking.objects.filter(user_id=current_user.id)
            for rs in booking:
                detail = ReservationRoom()
                detail.reservation_id = data.id
                detail.room_id = rs.room_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                detail.price = rs.room.price
                detail.amount = rs.amount
                detail.save()

                room = Room.objects.get(id=rs.room_id)
                room.amount -= rs.quantity
                room.save()

            Booking.objects.filter(user_id=current_user.id).delete()  # Clear & Delete
            request.session['booking_items'] = 0
            messages.success(request, "Your Reservation has been completed. Thank you ")
            return render(request, 'reservation_complated.html', {'roomcode': roomcode, 'category': category})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/reservation/reservationroom")

    form = ReservationForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'booking': booking,
               'category': category,
               'total': total,
               'form': form,
               'profile': profile,
               }
    return render(request, 'reservation_form.html', context)

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


