from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse

from .models import Master


def insert_master(request):
    master = Master()
    master.master_name = "ABCD"

    master.save()
    return HttpResponse("Saved Successfully")
