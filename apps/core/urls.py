from django.urls import path, include
from . import views
from .views import home


urlpatterns = [

    path("contact/", views.contact, name="contact"),
    path('', views.home, name='home'),
    path("", home, name="home"),
    


]