import os
import json
import time
import logging
import subprocess
from subprocess import Popen, PIPE

from http_coap_interface.events import *
from event.services import publish_event


def generate_invalid_coap_response(**kwargs):
    return {
        "error" : "invalid data received from client",
        "received" : kwargs,
        "solution" : "pass correct message request body in JSON format",
        "request_body_example": {
            "coap_server_ip" : "192.168.1.37",
            "coap_server_resource" : "light",
            "coap_server_port" : 5683,
            "coap_method" : "put",
            "coap_payload" : {
                "light": False
            }
        }
    }


def create_coap_fields_from_http_request(**kwargs):
    return {
        "coap_server_ip" : kwargs.get("coap_server_ip", "INVALID"),
        "coap_server_resource" : kwargs.get("coap_server_resource", "INVALID"),
        "coap_server_port" : int(kwargs.get("coap_server_port", 0)),
        "coap_method" : kwargs.get("coap_method", "INVALID").lower(),
        "coap_payload" : kwargs.get("coap_payload", {}),
    }


def generate_test_coap_response(**kwargs):
    return {
        "message" : "Test HTTP-COAP Interface endpoint",
        "received" : kwargs,
    }


def parse_coap_client_response(command_output):
    
    def _process_status_message(message):
        coap_status_message = {
            "2.00" : "OK",
            "2.01" : "Created",
            "2.02" : "Deleted",
            "2.03" : "Valid",
            "2.04" : "Changed",
            "2.05" : "Content",
            "2.31" : "Continue",
            "4.0"  : "Bad Request",
            "4.01" : "Unauthorized",
            "4.02" : "Bad Option",
            "4.03" : "Forbidden",
            "4.04" : "Not Found",
            "4.05" : "Method Not Allowed",
            "4.06" : "Not Acceptable",
            "4.08" : "Request Entity Incomplt.",
            "4.12" : "Precondition Failed",
            "4.13" : "Request Ent. Too Large",
            "4.15" : "Unsupported Content-Fmt.",
            "5.00" : "Internal Server Error",
            "5.01" : "Not Implemented",
            "5.02" : "Bad Gateway",
            "5.03" : "Service Unavailable",
            "5.04" : "Gateway Timeout",
            "5.05" : "Proxying Not Supported",
        }
        status_response = {
            "coap_status_response": message,
            "coap_status_description": coap_status_message.get(message, "")
        }
        return status_response
        
    splitted = command_output.split("\n")
    try:
        message_output = json.loads(splitted[1])
        if isinstance(message_output, (int, float)):
            message_output = _process_status_message(str(message_output))
    except:
        message_output = splitted[1]
    total_info = splitted[0].split(" ")
    version = total_info[0].split(":")[1]
    message_type = total_info[1].split(":")[1]
    method = total_info[2].split(":")[1]
    message_id = total_info[3].split(":")[1]
    return {
        "version": version,
        "message_type": message_type,
        "method": method,
        "message_id": f"0x{message_id}",
        "output" : message_output,
    }


def execute_coap_client_request(**kwargs):

    def _validate_fields():
        if kwargs.get('coap_server_ip') == "INVALID":
            return False
        if kwargs.get('coap_server_resource') == "INVALID":
            return False
        if kwargs.get('coap_server_port') == 0:
            return False
        if kwargs.get('coap_method') == "INVALID":
            return False
        if kwargs.get('coap_method') in ["put", "post"]:
            if not kwargs.get('coap_payload'):
                return False
        return True

    def _create_get_or_delete_command_list(method="get"):
        command_list = []
        command_list.append("coap-client")
        command_list.append("-m")
        command_list.append(method)
        command_list.append("-p")
        command_list.append(f"{kwargs.get('coap_server_port')}")
        connection = f"coap://{kwargs.get('coap_server_ip')}/{kwargs.get('coap_server_resource')}"
        command_list.append(connection)
        return command_list

    def _create_put_or_post_command_list(method="put"):
        command_list = []
        command_list.append("coap-client")
        command_list.append("-m")
        command_list.append(method)
        command_list.append("-e")
        payload = json.dumps(kwargs.get('coap_payload')).replace(" ", "")
        command_list.append(payload)
        command_list.append("-p")
        command_list.append(f"{kwargs.get('coap_server_port')}")
        connection = f"coap://{kwargs.get('coap_server_ip')}/{kwargs.get('coap_server_resource')}"
        command_list.append(connection)
        return command_list

    if not _validate_fields():
        return generate_invalid_coap_response(**kwargs)

    command_list = []
    if kwargs.get('coap_method') in ["get", "delete"]:
        command_list = _create_get_or_delete_command_list(method=kwargs.get('coap_method'))
    elif kwargs.get('coap_method') in ["put", "post"]:
        command_list = _create_put_or_post_command_list(method=kwargs.get('coap_method'))
    else:
        print(f"Unsupported CoAP method")
        return generate_invalid_coap_response(**kwargs)

    publish_event(HttpCoapRequest(command_list))
    command_output = subprocess.Popen(
        command_list, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT
        )
    stdout, _ = command_output.communicate()
    decoded_output = stdout.decode('utf-8')
    command_response = parse_coap_client_response(decoded_output)
    publish_event(CoapHttpResponse(command_response))
    return command_response
