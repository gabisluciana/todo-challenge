import logging
import json

logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logging.info(f"Request URL: {request.method} - {request.path}")
        data = request.GET.dict() if request.method == "GET" else json.loads(request.body or "[]")
        if "password" not in data:
            logging.info(f"Request DATA: {data}")

        response = self.get_response(request)

        logging.info(f"Request USER: {request.user}")
        logging.info(f"Response STATUS_CODE: {response.status_code}")

        # Log response data
        # try:
        #     data = response.data
        #     if "access" not in data:
        #         logging.info(f"Response DATA: {data}")
        # except:
        #     pass

        return response
