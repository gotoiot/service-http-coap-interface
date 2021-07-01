from datetime import datetime
from event.models import BaseEvent


class HttpCoapRequest(BaseEvent):

    def __init__(self, data):
        super(HttpCoapRequest, self).__init__()
        self.actor = "http_client"
        self.target = "coap_server"
        self.data = data
        self.time = datetime.now()
        self.type = "HTTP_COAP_REQUEST"


class CoapHttpResponse(BaseEvent):

    def __init__(self, data):
        super(CoapHttpResponse, self).__init__()
        self.actor = "coap_server"
        self.target = "http_client"
        self.data = data
        self.time = datetime.now()
        self.type = "COAP_HTTP_RESPONSE"
    