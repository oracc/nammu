import requests
import logging
import httplib as http_client
import HTTPRequestBuilder

class SOAPClient:
    """
    Sends and retrieves information to and from the ORACC SOAP server.
    """
    def __init__(self, url):
        self.url = url

    def send_message(self):
        """
        Elaborate HTTP POST request and send it to ORACC's server.
        """
        pass

    def get_response(self):
        """
        Check for a response to the request and obtain response zip file.
        """
        pass

    def _check_response_ready(self, id):
        """
        Send a HTTP GET request to ORACC's server and retrieve status.
        """
        pass
