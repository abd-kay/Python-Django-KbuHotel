from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.utils.crypto import get_random_string
from reservation.models import ReservationCart, ReservationCartForm, ReservationForm, Reservation, ReservationRoom
from hotel.models import Category, Hotel, Room
from user.models import UserProfile


def index(request):
    return HttpResponse("reservation App")


@login_required(login_url='/login')  # Check Login
def addtocart(request, rid, pid):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    checkroom = ReservationCart.objects.filter(room_id = rid)  #Query if the product is in the cart
    if checkroom:
        control = 1  # The hotel is in the cart
    else:
        control = 0  # The hotel is not in the cart

    if request.method == 'POST':  # If the form is posted, on the hotel detail page
        form = ReservationCartForm(request.POST)
        if form.is_valid():
            if control==1:  # update the hotel
                data = ReservationCart.objects.get(room_id=rid)
                data.quantity += form.cleaned_data['quantity']
                data.save()  # save to database
            else :
                data = ReservationCart()  # model ile bağlantı kur
                data.user_id = current_user.id
                data.room_id = rid
                data.hotel_id = pid
                data.quantity = form.cleaned_data['quantity']
                data.date_start = form.cleaned_data['date_start']
                data.date_end = form.cleaned_data['date_end']
                data.save()
            request.session['cart_items'] = ReservationCart.objects.filter(user_id=current_user.id).count()
            messages.success(request, "The hotel room has been successfully added. We thank you ")
            return HttpResponseRedirect(url)
    else:  # If the hotel is pressed directly on the add to cart button
        if control ==1:
            data = ReservationCart.objects.get(room_id=rid)
            data.quantity += 1
            data.save()  # save to database
        else:
            data = ReservationCart()   # connect with model
            data.user_id = current_user.id
            data.room_id = rid
            data.quantity = 1
            data.save()     # save to database
            request.session['cart_items'] = ReservationCart.objects.filter(user_id=current_user.id).count()
        messages.success(request, "The hotel room has been successfully added to the cart. We thank you ")
        return HttpResponseRedirect(url)

    messages.success(request, "There was an error adding the hotel room to the cart! Please check ")
    return HttpResponseRedirect(url)

@login_required(login_url='/login')     # Check login
def reservationcart(request):
    category = Category.objects.all()
    current_user = request.user
    reservationcart = ReservationCart.objects.filter(user_id=current_user.id)
    request.session['cart_items'] = ReservationCart.objects.filter(user_id=current_user.id).count()
    total=0
    for rs in reservationcart:
        total += rs.room.price * rs.quantity

    context = {'reservationcart': reservationcart,
               'category': category,
               'total': total,
               }
    return render(request, 'reservationcart_rooms.html', context)


@login_required(login_url='/login')    # Check login
def deletefromcart(request, id):
    ReservationCart.objects.filter(id=id).delete()
    current_user = request.user
    request.session['cart_items'] = ReservationCart.objects.filter(user_id=current_user.id).count()
    messages.success(request, "The hotel has been deleted from the cart.")
    return HttpResponseRedirect("/reservationcart")


@login_required(login_url='/login')
def reservationroom(request):
    category = Category.objects.all()
    current_user = request.user
    reservationcart = ReservationCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in reservationcart:
        total += rs.room.price * rs.quantity

    if request.method == 'POST':    #if there is a post
        form = ReservationForm(request.POST)
        if form.is_valid():
            data = Reservation()
            data.first_name = form.cleaned_data['first_name']   #get room quantity form
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            reservationcode = get_random_string(5).upper()
            data.code = reservationcode
            data.save()

            # Move Shopcart items to Reservation hotels items
            reservationcart = ReservationCart.objects.filter(user_id=current_user.id)
            for rs in reservationcart:
                detail = ReservationRoom()
                detail.reservation_id = data.id
                detail.room_id = rs.room_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                detail.date_start = rs.date_start
                detail.date_end = rs.date_end
                # ***Reduce quantity of sold hotel from Amount of hotel
                room = Room.objects.get(id=rs.room_id)
                room.amount -= rs.quantity
                room.save()

                detail.price = rs.room.price
                detail.amount = rs.amount
                detail.save()

            ReservationCart.objects.filter(user_id=current_user.id).delete()   #clear & delete shopcart
            request.session['cart_items'] = 0
            messages.success(request, "Your Reservation has been completed. Thank you")
            return render(request, 'reservation_completed.html', {'reservationcode':reservationcode, 'category':category})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/reservation/reservationroom')

    form = ReservationForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'reservationcart': reservationcart,
               'category': category,
               'total': total,
               'form': form,
               'profile': profile,
               }
    return render(request, 'reservation_form.html', context)