from django.urls import path
from . import views


urlpatterns = [
    path('update-profile/', views.Users.user_update_profile),
    path('signup/', views.Users.user_registration),
    path('signup-mobile/', views.Users.user_with_mobile_registration),
    path('verify-mobile/', views.Users.verify_users),
    path('send-otp/', views.Users.send_otp),
]