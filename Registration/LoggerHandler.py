import logging

from rest_framework.response import Response
logger = logging.getLogger(__name__)
from rest_framework import status


def logger_with_response(result, response):
    print(result, ', ' + str(response))
    logger.warning((str(result) + ', Status=' + str(response)))
    return Response(result, status=response)


def logger_with_response_error(result, response):
    logger.error((result + ', Status=' + str(response)))
    return Response(result, status=response)


def logger_with_exception(message, exception):
    logger.info(message, str(exception))
    # return Response(message, status=exception)
