"""Aadhar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from .views import *

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', Home, name='home'),
    path('register/', Register, name='register'),
    path('', Login, name='loginpage'),
    path('logout/', logoutuser, name='logout'),
    path('aboutus/', Aboutus, name='aboutus'),
    path('services/', Services, name='services'),
    path('contactus/', Contactus, name='contactus'),
    path('poll/', poll_list, name='poll_list'),
    path('poll/<int:poll_id>/', poll_view, name='poll'),
    path('results/<int:poll_id>/', results_view, name='results'),
]