from django.urls import path
from . import views


urlpatterns = [
    path('master/', views.Users.insert_master),
    path('admin/', views.Users.user_registration_test),
    path('update-profile/', views.Users.user_update_profile),
    path('get-profile/', views.Users.get_users_information),
    path('signup/', views.Users.user_registration),
    path('signup-mobile/', views.Users.user_with_mobile_registration),
    path('verify-mobile/', views.Users.verify_users),

]