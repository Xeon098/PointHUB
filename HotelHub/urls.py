"""HotelHub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.conf import settings
from django.conf.urls.static import static
from django.utils.translation import ugettext_lazy as _
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from website import views
urlpatterns = [
    url('admin/', admin.site.urls),
    url('',include('website.urls')),
    url('',views.index,name="index")
]


'''
from django.conf.urls import url, include
from django.contrib import admin
#from . import views, settings
from django.contrib.staticfiles.urls import static
from django.conf import settings
from django.conf.urls.static import static
from django.utils.translation import ugettext_lazy as _
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('PointApp.urls')),
    url(r'^ratings/', include('star_ratings.urls'))#, namespace='ratings', app_name='ratings')),
]
'''
admin.site.site_header = _("PointHub Admin")
admin.site.site_title = _("PointHub Admin")
