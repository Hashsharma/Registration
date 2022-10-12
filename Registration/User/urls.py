from django.urls import path
from . import views


urlpatterns = [
    path('master/', views.insert_master),

]