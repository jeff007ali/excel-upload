import logging
from re import sub
from django.http import JsonResponse


logger = logging.getLogger("app")

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        header_token = request.META.get("HTTP_AUTHORIZATION", None)
        if header_token is None or header_token != "Token qwerty12345": 
        # I took this hard coded value as of now, but we can generate token using username and password and store token in cache and validate it.
            logger.debug("Token authentication failed!!!")
            return JsonResponse(
                {"result": False, "message": "Unauthorized Access"},
                status=401,
            )

        response = self.get_response(request)

        return response
