# Create your views here.
import random

from django.http import HttpResponse
from rest_framework import status, status, status, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import ResponseHandler
from ConfigurationValues import ConfigurationValues
from MasterConfiguration.views import MasterConfiguration
from .models import Master, RegistrationModel

from django.utils import timezone
import datetime
import json

import requests
# import the logging library
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)
logger = logging.getLogger('warning')


class Users:

    @api_view(['POST'])
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
                otp_result = Users.send_otp(req)
                if otp_result.status_code == 200:
                    return ResponseHandler.response_with_logger("Sent Successfully", status.HTTP_200_OK)

                else:
                    return Response("Failed to send OTP", status=status.HTTP_400_BAD_REQUEST)

            elif result is not None:
                user_value = RegistrationModel.objects.get(pk=result['user_rid'])
                user_value.user_mod_datetime = datetime.datetime.now(tz=timezone.utc)
                user_value.user_otp = Users.generate_otp()
                user_value.user_product_rid = req.get('productRid')

                user_value.save()
                logger.info('Already Registered -- Otp Sent Successfully')
                result = Users.send_otp(req)
                if result.status_code == 200:
                    return ResponseHandler.response_with_logger("Sent Successfully", status.HTTP_200_OK)

                else:
                    return ResponseHandler.response_with_logger("Failed to send OTP", status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return ResponseHandler.response_with_logger_error("Failed to send OTP " + str(e),
                                                              status.HTTP_400_BAD_REQUEST)

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


    def send_otp(req):

        config_value = MasterConfiguration.get_master_conf(ConfigurationValues.conf_sms_value,
                                                           req.get('productRid'))

        result = requests.post(config_value.get('config_url'), json=req)
        return result

