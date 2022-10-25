# Create your views here.
import random

from django.http import HttpResponse
from django.shortcuts import render

from .models import Master, RegistrationModel

from django.utils import timezone
import datetime
import json
from django.forms.models import model_to_dict
import requests


class Users:

    def user_with_mobile_registration(request):
        try:
            user_model = RegistrationModel()
            req = json.loads(request.body)

            result = Users.get_user_info(req)

            if result is None:

                user_model.user_mobile = req.get('mobile')
                user_model.user_created_datetime = datetime.datetime.now(tz=timezone.utc)
                user_model.user_product_rid = req.get('productRid')
                user_model.user_ip_address = Users.get_ip_address(request)
                user_model.user_otp = Users.generate_otp()
                user_model.save()
                Users.send_otp()
                return HttpResponse("Sent Successfully", status=200)

            elif result is not None:
                user_value = RegistrationModel.objects.get(pk=result['user_rid'])
                user_value.user_mod_datetime = datetime.datetime.now(tz=timezone.utc)
                user_value.user_otp = Users.generate_otp()
                user_value.user_product_rid = req.get('productRid')

                user_value.save()
                return HttpResponse("Sent Successfully", status=200)

        except Exception as e:
            return HttpResponse(' Failed to register ' + str(e))

    def get_user_info(user_data):
        try:
            result = RegistrationModel.objects.filter(user_mobile=user_data.get('mobile'),
                                                  user_product_rid=user_data.get('productRid')).values()
            result = dict(result[0])
            return result

        except Exception as err:
            return None



    def insert_master(request):
        master = Master()
        master.master_name = "ABCD"

        master.save()
        return HttpResponse("Saved Successfully")

    def user_registration(request):
        try:
            user_model = RegistrationModel()
            req = json.loads(request.body)
            user_model.user_first_name = req.get('firstName')
            user_model.user_last_name = req.get('lastName')
            user_model.user_email = req.get('email')
            user_model.user_mobile = req.get('mobile')
            user_model.user_address = req.get('address')
            user_model.user_gender = req.get('gender')
            user_model.user_created_datetime = datetime.datetime.now(tz=timezone.utc)
            user_model.user_product_rid = req.get('productRid')
            user_model.user_ip_address = Users.get_ip_address(request)

            user_model.save()
            return HttpResponse("Saved Successfullyd", status=200)

        except Exception as e:
            return HttpResponse(str(e))

    def user_registration_test(request):
        try:
            user_model = RegistrationModel()
            user_model.user_first_name = 'anand'
            user_model.user_last_name = 1
            user_model.user_email = 'anand@gmail.com'
            user_model.user_mobile = '979792345'
            user_model.user_address = 'abcdefgh'
            user_model.user_gender = 1
            user_model.user_created_datetime = datetime.datetime.now()

            user_model.save()
            return HttpResponse("Saved Successfully")

        except Exception as e:
            return HttpResponse(str(e))

    def user_update_profile(request):
        try:
            user_model = RegistrationModel()
            req = json.loads(request.body)

            user_model = user_model.objects.all()
            print(user_model)

            if req is not None:
                if req.first_name is not None:
                    user_model.user_first_name = req.first_name

                if req.last_name is not None:
                    user_model.user_first_name = req.last_name

                if req.email is not None:
                    user_model.email = req.email

                if req.mobile is not None:
                    user_model.user_mobile = req.mobile

                if req.gender is not None:
                    user_model.user_gender = req.gender

                if req.dob is not None:
                    user_model.user_dob = req.dob

                if req.calculated_dob is not None:
                    user_model.user_calculated_dob = req.calculated_dob

                if req.address is not None:
                    user_model.user_address = req.address

            return HttpResponse(user_model)


        except Exception as e:
            return HttpResponse(str(e))

    def get_users_information(request):

        try:
            user_model = RegistrationModel()
            # req = json.loads(request.body)

            user_model = RegistrationModel.objects.all().values()
            print(user_model)
            return HttpResponse(user_model)

        except Exception as e:
            return HttpResponse(str(e))

    def get_ip_address(request):

        user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
        if user_ip_address:
            ip = user_ip_address.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @classmethod
    def generate_otp(self):
        otp = random.randrange(000000, 999999)
        return otp

    def verify_users(request):
        try:
            req = json.loads(request.body)

            result = RegistrationModel.objects.filter(user_mobile=req.get('mobile'),
                                                      user_product_rid=req.get('productRid')).values()
            result = dict(result[0])

            if result:
                if result['user_otp'] == req.get('otp'):
                    user_value = RegistrationModel.objects.get(pk=result['user_rid'])
                    user_value.user_otp = 0
                    user_value.user_mobile_verify = 1

                    user_value.save()
                    return HttpResponse("Verified Successfully", status=200)

                else:
                    return HttpResponse("Wrong OTP", status=400)

            else:
                return HttpResponse("Not Registered", status=400)

        except Exception as e:
            return HttpResponse(str(e))


    def send_otp(self):
        result = requests.get("http://127.0.0.1:8080/message/otp-connection/")
        return HttpResponse(result)

