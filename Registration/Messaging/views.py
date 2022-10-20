from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
import json

from Messaging.models import MessageModel


class Messaging:

    def connected(self):
        return HttpResponse('Connected', status=200)

    def send_mobile_message(request):
        try:
            message_model = MessageModel()

            req = json.loads(request.body)
            message_model.msg_number = req.get('mobile')
            message_model.msg_generated_datetime = datetime.now()
            message_model.msg_status = req.get('status')
            message_model.msg_product_rid = req.get('product_rid')
            message_model.msg_count = req.get('count')

            message_model.save()
            return HttpResponse('Sent Successfully', status=200)

        except Exception as e:
            return HttpResponse('Failed to Sent ' + str(e), status=400)


