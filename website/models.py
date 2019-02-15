# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import models
from datetime import datetime, date, time, timedelta
from django.utils import timezone
import uuid
from decimal import Decimal


class Profile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   bio = models.TextField(max_length=500, blank=True)
   location = models.CharField(max_length=30, blank=True)
   birth_date = models.DateField(null=True, blank=True)
   name = models.CharField(db_column='NAME', max_length=100, default='')# Field name made lowercase.
   phone = models.IntegerField(blank = True,null = True,default = 0000000000)
   img = models.ImageField(upload_to = "profilepics",blank=True,default = "default.png")
    
   def __str__(self):
      return self.name

@receiver(post_save,sender = User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
   if created:
      Profile.objects.create(user=instance)
   instance.profile.save()
   


      
class Hotels(models.Model):
   name = models.CharField(max_length = 255)
   location = models.CharField(max_length = 255)
   logo = models.ImageField(upload_to = "logo-pics/",blank = True)

   def __str__(self):
      return self.name

    
   @classmethod
   def get_hotels(cls):

      get_hotels = cls.objects.all()
      return get_hotels

   @classmethod
   def get_search_hotels(cls, departure_location):
      foundHotels =cls.objects.filter(location = departure_location)
      print("hotl methos",foundHotels)
      return foundHotels

   
class Room(models.Model):
   '''
    Class to define a Room 
   '''
   hotels = models.ForeignKey(Hotels, on_delete=models.CASCADE)

   name = models.CharField(max_length=255)

   capacity = models.PositiveIntegerField(default=0)

   price = models.DecimalField(max_digits=15 ,decimal_places=2, default=Decimal(0.00))

   class Meta:
      ordering = ['price']
    
   def __str__(self):
      return self.hotels.name + ' ' + str(self.name)

   @classmethod
   def get_rooms(cls):
        
      rooms = cls.objects.all()

      return rooms

   @classmethod
   def get_single_room(cls, room_id):
        
      single_room = cls.objects.get(id=room_id)

      return single_room

   @classmethod
   def get_hotel_rooms(cls, hotels_id):
      
      hotel_rooms = cls.objects.filter(hotels=hotels_id)
      return hotel_rooms

class Booking(models.Model):
   # self.id in base 32 could be a nice booking ID (also returned as __str__)
   added =  models.DateTimeField(auto_now_add=True)
   check_in =  models.DateTimeField(auto_now_add=False)
   check_out =  models.DateTimeField(auto_now_add=False)
   price = models.DecimalField(max_digits=15 ,decimal_places=2, default=0.00)
   room = models.ForeignKey(Room, on_delete=models.CASCADE)
   name =  models.CharField(max_length=50)   
   phone_number = models.CharField(max_length = 255)
   user = models.ForeignKey(User,on_delete = models.CASCADE,default = 1,unique = False)
   def __str__(self):
      return ' Booking ' + str(self.id)
    
   @classmethod
   def get_book_hotel_room(cls, room_id, check_in_date, check_out_date):
      
      bookings = cls.objects.filter(room=room_id)
      result=[]
      # Get each existing route
      for x in bookings:
         print(x)
         if not (x.check_in.date() > check_in_date and x.check_out.date() < check_in_date) or (x.check_in.date() > check_out_date and x.check_out.date() < check_out_date) or (x.check_in.date() <= check_in_date and x.check_out.date() >= check_out_date):
            result.append(x)
         else:
            continue
      print("result",result)
      return result
