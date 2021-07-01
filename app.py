#!/usr/bin/python
import os
import traceback

from flask import Flask, jsonify
from flask_restful import Api
from flask_gzip import Gzip

from config import PORT, ENV, config_get_current_settings_as_list
from log import error, warn, info, debug
from http_coap_interface.resources import http_coap_interface_add_http_resources_to_api


application = Flask(
    __name__,
    static_url_path='/assets',
    static_folder='static',
)
flask_restful_api = Api(application)
flask_gzip = Gzip(application)
application.config['PROPAGATE_EXCEPTIONS'] = True


@application.errorhandler(404)
def page_not_found(error_msg):
    response = {
        "message": str(error_msg),
    }
    return jsonify(response), 404


@application.errorhandler(Exception)
def handle_exception(error_msg):
    response = {
        "message": str(error_msg),
    }
    return jsonify(response), 400


@application.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    response.headers.add('Cache-Control', 'no-store, no-cache')
    return response


@application.route("/status", methods=['GET'])
def status():
    return jsonify({
        "service_name": "http-coap-interface",
        "status": "running",
        "env": ENV,
    })


def _show_welcome_message():
    welcome_message = """\n\n
          /$$$$$$            /$$                    /$$$$$$      /$$$$$$$$
         /$$__  $$          | $$                   |_  $$_/     |__  $$__/
        | $$  \__/ /$$$$$$ /$$$$$$   /$$$$$$         | $$   /$$$$$$| $$   
        | $$ /$$$$/$$__  $|_  $$_/  /$$__  $$        | $$  /$$__  $| $$   
        | $$|_  $| $$  \ $$ | $$   | $$  \ $$        | $$ | $$  \ $| $$   
        | $$  \ $| $$  | $$ | $$ /$| $$  | $$        | $$ | $$  | $| $$   
        |  $$$$$$|  $$$$$$/ |  $$$$|  $$$$$$/       /$$$$$|  $$$$$$| $$   
         \______/ \______/   \___/  \______/       |______/\______/|__/   

                        SERVICE HTTP-COAP INTERFACE
                        ---------------------------
    \n"""
    settings_list = config_get_current_settings_as_list()
    print(welcome_message)
    print(f"\n{'#' * 80}\n")
    for setting in settings_list:
        print(f"# {setting}")
    print(f"\n{'#' * 80}\n\n")


def _init_application():
    _show_welcome_message()
    info("Starting to run HTTP-CoAP Interface Service")
    http_coap_interface_add_http_resources_to_api(flask_restful_api, prefix="/http_coap")


_init_application()


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=PORT, debug=True)