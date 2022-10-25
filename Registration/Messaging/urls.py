from django.urls import path
from . import views


urlpatterns = [
    path('send-mobile-otp/', views.Messaging.send_mobile_message),
    path('otp-connection/', views.Messaging.connected),
    path('send-otp/', views.Messaging),


]