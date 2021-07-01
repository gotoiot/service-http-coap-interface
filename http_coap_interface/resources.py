#!/usr/bin/python
from flask import request
from flask_restful import Resource

from config import config_write
from log import error, warn, info, debug
from http_coap_interface.services import *


class HttpCoapInterfaceTestResource(Resource):

    def put(self):
        if not request.json:
            return generate_invalid_coap_response()
        coap_fields = create_coap_fields_from_http_request(**request.json)
        return generate_test_coap_response(**coap_fields)


class HttpCoapInterfaceResource(Resource):

    def put(self):
        if not request.json:
            return generate_invalid_coap_response()

        coap_fields = create_coap_fields_from_http_request(**request.json)
        return execute_coap_client_request(**coap_fields)


def http_coap_interface_add_http_resources_to_api(flask_restful_api, prefix=""):
    prefix = f"/{prefix}" if prefix and not prefix.startswith("/") else prefix
    info(f"Adding 'http_resources_to_api' resources to application with prefix '{prefix}'")
    flask_restful_api.add_resource(HttpCoapInterfaceTestResource, f'{prefix}/test')
    flask_restful_api.add_resource(HttpCoapInterfaceResource, f'{prefix}/interface')
