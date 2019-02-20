# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render, redirect
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from .models import Hotels, Room, Booking,Profile
from datetime import datetime, date
from .forms import SignUpForm, BookingForm,ProfileUpdate
import uuid
import phonenumbers
import random
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.conf import settings

def index(request):
   
   return render(request,'catalog/index.html')
   
def searchhotels(request):
   return render(request,'catalog/searchhotels.html',{"User" : request.user}) 

def contact(request):
   return render(request,'catalog/contact.html') 

def errors(request):
   return render(request,'catalog/error.html') 

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'catalog/signup.html', {'form': form})

def search_hotel_results(request):    
    try:
        title = 'Hotel Result'
        if ('depature-location' in request.GET and request.GET['depature-location']) and ('check-in-date' in request.GET and request.GET['check-in-date']) and ('check-out-date' in request.GET and request.GET['check-out-date']):
            # Get the input departure
            search_departure_location = request.GET.get('depature-location').title()

            # Get the input arrival location
            check_in_date = request.GET.get('check-in-date')

            # Get the input date
            check_out_date = request.GET.get('check-out-date')

            # Convert string input to date type
            convert_to_check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date()
            convert_to_check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d').date()

            if convert_to_check_in_date < datetime.now().date():
                no_scheduled_bus_message = 'Invalid CheckIn Date'

                return render(request, 'catalog/searchResult.html', {'title':title, 'no_scheduled_bus_message':no_scheduled_bus_message, 'search_departure_location':search_departure_location, 'convert_to_check_in_date':convert_to_check_in_date, 'convert_to_check_out_date':convert_to_check_out_date})

            if convert_to_check_out_date < convert_to_check_in_date:
                no_scheduled_bus_message = 'Invalid Checkout Date'
            
                return render(request, 'catalog/searchResult.html', {'title':title, 'no_scheduled_bus_message':no_scheduled_bus_message, 'search_departure_location':search_departure_location, 'convert_to_check_in_date':convert_to_check_in_date, 'convert_to_check_out_date':convert_to_check_out_date})

            # Get the route 
            result_hotel = Hotels.get_search_hotels(search_departure_location)
    
        
            avaialbleRoom =[]
            # Check if route exists found
            if result_hotel.exists() :
                #convert_to_check_in_date, convert_to_check_out_date,
                for hotel in result_hotel:

                    for roomoj in (list(Room.get_hotel_rooms(hotel.id))):
                        avaialbleRoom.append(roomoj)

                if len(avaialbleRoom) > 0:
                    bookingobj = Booking.objects.all()
                    for roomObj in avaialbleRoom:
                        for x in bookingobj:
                            #print(x.room.hotels.location," ",roomObj.hotels.location)
                            if x.room.hotels.location == roomObj.hotels.location:
                                '''print(x.check_in.date())
                                print(convert_to_check_in_date)
                                print("--------")
                                print(x.check_out.date())
                                print(convert_to_check_out_date)
                                
                                print(x.check_in.date() <convert_to_check_out_date  and x.check_out.date() >convert_to_check_out_date )
                                print("-------------")'''
                                if (x.check_in.date() < convert_to_check_in_date and x.check_out.date() > convert_to_check_in_date ) or (x.check_in.date() < convert_to_check_out_date  and x.check_out.date() > convert_to_check_out_date ) or (x.check_in.date() <= convert_to_check_in_date and x.check_out.date() >=convert_to_check_out_date ):
                                    avaialbleRoom.remove(roomObj)
                    #   result_booking = Booking.get_book_hotel_room(roomObj.id, convert_to_check_in_date, convert_to_check_out_date)
                    #    print("result_boooking",result_booking)
    
                    return render(request, 'catalog/searchResult.html', {'title':title, 'search_departure_location':search_departure_location, 'convert_to_check_in_date':convert_to_check_in_date, 'convert_to_check_out_date':convert_to_check_out_date, 'avaialbleRoom':avaialbleRoom}) #'result_booking':result_booking})

                else:
                    no_scheduled_bus_message = 'No Hotels Available'

                    return render(request, 'catalog/searchResult.html', {'title':title, 'no_scheduled_bus_message':no_scheduled_bus_message, 'search_departure_location':search_departure_location, 'convert_to_check_in_date':convert_to_check_in_date, 'convert_to_check_out_date':convert_to_check_out_date})

               # Otherwise
            else:
                
                no_route_message = 'Hotels not found'

                return render(request, 'catalog/searchResult.html', {'title':title, 'no_route_message':no_route_message, 'search_departure_location':search_departure_location, 'convert_to_check_in_date':convert_to_check_in_date, 'convert_to_check_out_date':convert_to_check_out_date})
        
    except ObjectDoesNotExist:

        return redirect(Http404)



def room_details(request, room_id, check_in_date, check_out_date):

    try:

        selected_room = Room.get_single_room(room_id)

        title = '{selected_room.hotels.name} Details'        

        if request.method == 'POST':
            
            form = BookingForm(request.POST)
            if form.is_valid():
                
                Booking = form.save(commit=False)
                Booking.room = selected_room
                Booking.check_in = check_in_date
                Booking.check_out = check_out_date
                Booking.price = selected_room.price
                Booking.user = request.user
                Booking.save()    


                return redirect(room_booked)
            else:
                return render(request,'catalog/room_details.html',{"error": "Enter valid details"})
        else:

            form = BookingForm()
            return render(request, 'catalog/room_details.html', { 'title':title, 'form':form ,'selected_room':selected_room, 'check_in_date':check_in_date,'check_out_date':check_out_date})

    except ObjectDoesNotExist:

         return redirect(Http404)


def room_booked(request):
   return render(request,'catalog/roombooked.html')

def booking(request):
   obs = Booking.objects.filter(user = request.user)
   print(list(obs))
        
   return render(request,'catalog/booking.html',{'Booking' : list(obs),'User': request.user} )

def profile(request):
    med_root = settings.MEDIA_ROOT
    
    hotelobj = Hotels.objects.all()
    for inst in Profile.objects.all():
        if inst.user == request.user:
            return render(request,'catalog/profile.html',{'inst': inst,'hotelObj' : hotelobj,'MED':med_root})


def user_edit(request):
    user = Profile.objects.get(user = request.user)
    if request.method == 'POST':
        form = ProfileUpdate(request.POST , instance = user)
        if form.is_valid():
            form.save()
            return redirect('/profile/')
    else:
        form =ProfileUpdate(instance =request.user)
        return render(request,'catalog/Updateprofile.html',{"form": form})
    


def allhotels(request):
    hotels = Hotels.objects.all()
    return render(request,'catalog/allhotels.html',{"hotels" : hotels})

def allrooms(request,hotel_id):
    roomlist =[]

    for room in Room.objects.all():
        if room.hotels.id == int(hotel_id):
            roomlist.append(room)
    return render(request,'catalog/rooms.html',{"rooms" : roomlist})

def cancelBooking(request,Booking_id):
    print(Booking_id)
    Booking.objects.get(pk = Booking_id).delete()
    return redirect(booking)
