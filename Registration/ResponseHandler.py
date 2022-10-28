import logging

from rest_framework.response import Response
logger = logging.getLogger(__name__)
from rest_framework import status



def response_with_logger(result, response):
    print(result + ', ' + str(response))
    logger.warning((result + ', Status=' + str(response)))
    return Response(result, status=response)


def response_with_logger_error(result, response):
    logger.error((result + ', Status=' + str(response)))
    return Response(result, status=response)
