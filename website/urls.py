from django.conf.urls import url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework.authtoken import views as api_views

urlpatterns = [
    url('login/', auth_views.LoginView.as_view(template_name='catalog/login.html'), name='login'),
    url('logout/', auth_views.LogoutView.as_view(template_name='catalog/logged_out.html'), name='logout'),
    url('index/',views.index, name ="index"),
    url('bookings/',views.booking, name = "booking"),
    url('profile/',views.profile, name = 'Profile'),
    url('error/', views.errors, name='error'),
    url('signup/', views.signup, name='signup'),
    url('allhotels/',views.allhotels, name="allhotels"),
    url('allrooms/(\d+)',views.allrooms,name="allrooms"),
    url('searchhotel/',views.searchhotels, name = 'search_results'),
    url('hotels/', views.searchhotels, name='searchhotel'),
    url('search_hotel_results/',views.search_hotel_results, name = 'search_hotel_results'),
    url('room_details/(\d+)/([-\w]+)/([-\w]+)',views.room_details, name = 'room_details'),  
    url('room_booked/',views.room_booked, name = 'room_booked'),   
    url('contact/', views.contact, name='contact'),
    url('edit/',views.user_edit, name="DS"),
    url('cancelBooking/(\d+)/',views.cancelBooking, name = "cancelbooking"),
    
    
] 
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''
    
    url(r'^bus-details/(\d+)',views.bus_details, name = 'bus_details'),
    url(r'^mobile_payment/(\d+)',views.mobile_payment, name = 'mobile_payment'),
    url(r'^searchtraval/', views.searchtravals, name='searchtraval'),

    url(r'^flights_hotels/', views.flights, name='flights'),
    url(r'^holidays/', views.holidays, name='holidays'),
         
     url(r'^allbus/', views.allbuss, name='allbus'),'''