# Create your views here.
import random

from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

import LoggerHandler
from Utility import ConfigurationUtility
from Utility.ConfigurationUtility import convert_db_datetime
from Utility.ConfigurationValues import ConfigurationValues
from MasterConfiguration.views import MasterConfiguration
from .UserSerializer import UserSerializer
from .models import Master, UserRegistrationModel

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


class Users(APIView):

    @api_view(['POST'])
    def user_with_mobile_registration(request):
        try:
            user_model = UserRegistrationModel()
            req = json.loads(request.body)

            query_set = Users.get_user_by_mobile(req)  # Need to check without dictionary

            if query_set is None:  # Checking query_set is null

                user_model.user_mobile = req.get('mobile')
                user_model.user_created_datetime = datetime.datetime.now()
                user_model.user_product_rid = req.get('productRid')
                user_model.user_ip_address = Users.get_ip_address(request)
                user_model.user_otp = Users.generate_otp()
                user_model.save()
                otp_result = Users.send_otp(req)
                if otp_result.status_code == 200:
                    return LoggerHandler.logger_with_exception("Sent Successfully", status.HTTP_200_OK)

                else:
                    return Response("Failed to send OTP", status=status.HTTP_400_BAD_REQUEST)

            elif query_set is not None:
                user_value = Users.get_user_by_id(query_set.pk)  # pk is user_rid
                user_value.user_mod_datetime = datetime.datetime.now()
                user_value.user_otp = Users.generate_otp()
                user_value.user_product_rid = req.get('productRid')

                user_value.save()
                logger.info('Already Registered -- Otp Sent Successfully')
                result = Users.send_otp(req)
                if result.status_code == 200:
                    return LoggerHandler.logger_with_response("Sent Successfully", status.HTTP_200_OK)

                else:
                    return LoggerHandler.logger_with_response("Failed to send OTP", status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return LoggerHandler.logger_with_response("Failed to send OTP " + str(e),
                                                      status.HTTP_400_BAD_REQUEST)

    def get_user_by_mobile(user_data):
        try:
            query_set = UserRegistrationModel.objects.filter(user_mobile=user_data.get('mobile'),
                                                             user_product_rid=user_data.get('productRid'))\
                .order_by('user_rid').reverse()
            # user_serializer = UserSerializer(query_set, many=True)
            if query_set.exists():
                return query_set[0]  # Can not have two entries in table with same mobile number and product id
            else:
                return None
        except Exception as err:
            LoggerHandler.logger_with_exception("Failed to get user Info", err)
            return None

    def user_registration(request):
        try:
            user_model = UserRegistrationModel()
            req = json.loads(request.body)
            user_model.user_first_name = req.get('firstName')
            user_model.user_last_name = req.get('lastName')
            user_model.user_email = req.get('email')
            user_model.user_mobile = req.get('mobile')
            user_model.user_address = req.get('address')
            user_model.user_gender = req.get('gender')
            user_model.user_created_datetime = datetime.datetime.now()
            user_model.user_product_rid = req.get('productRid')
            user_model.user_ip_address = Users.get_ip_address(request)

            user_model.save()
            return HttpResponse("Saved Successfully", status=200)

        except Exception as e:
            return HttpResponse(str(e))

    @api_view(['POST'])
    def user_update_profile(request):
        try:
            req = json.loads(request.body)
            query_set = Users.get_user_by_id(req.get('user_rid'))

            if query_set is not None:
                if req.get('firstName') is not None:
                    query_set.user_first_name = req.get('firstName')

                if req.get('lastName') is not None:
                    query_set.user_last_name = req.get('lastName')

                if req.get('email') is not None:
                    query_set.email = req.get('email')

                # if req.get('mobile') is not None:
                #     query_set.user_mobile = req.get('mobile')

                if req.get('gender') is not None:
                    query_set.user_gender = req.get('gender')

                if req.get('DOB') is not None:
                    query_set.user_dob = req.get('DOB')

                if req.get('calculatedDOB') is not None:
                    query_set.user_calculated_dob = req.get('calculatedDOB')

                if req.get('address') is not None:
                    query_set.user_address = req.get('address')
        
                query_set.save()

            return LoggerHandler.logger_with_response("Updated successfully", status.HTTP_200_OK)

        except Exception as e:
            return LoggerHandler.logger_with_response("Failed to update " + str(e),
                                                      status.HTTP_400_BAD_REQUEST)

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

            result = UserRegistrationModel.objects.filter(user_mobile=req.get('mobile'),
                                                          user_product_rid=req.get('productRid'))\
                .order_by('msg_rid').reverse()
            result = dict(result[0])

            if result:
                if result['user_otp'] == req.get('otp'):
                    user_value = UserRegistrationModel.objects.get(pk=result['user_rid'])
                    user_value.user_otp = 0
                    user_value.user_mobile_verify = 1

                    user_value.save()
                    return LoggerHandler.logger_with_response("Verified Successfully", status.HTTP_200_OK)

                else:
                    return LoggerHandler.logger_with_response("Wrong OTP", status.HTTP_400_BAD_REQUEST)

            else:
                return LoggerHandler.logger_with_response("Not Registered", status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return LoggerHandler.logger_with_exception("Not Registered " + str(e), status.HTTP_400_BAD_REQUEST)

    def send_otp(req):

        config_value = MasterConfiguration.get_master_conf(ConfigurationValues.conf_sms_value,
                                                           req.get('productRid'))

        result = requests.post(config_value.get('config_url'), json=req)
        return result

    def get_user_by_id(user_rid):
        try:
            query_set = UserRegistrationModel.objects.get(pk=user_rid)
            return query_set  # Can not have two entries in table with same mobile number and product id

        except Exception as err:
            LoggerHandler.logger_with_exception("Failed to get user Info" + str(err), status.HTTP_400_BAD_REQUEST)
            return None

