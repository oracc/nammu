import requests
import logging
import httplib as http_client
from HTTPRequest import HTTPRequest

# Dunno if this is the right place to set up logging
logging.basicConfig()

class SOAPClient:
    """
    Sends and retrieves information to and from the ORACC SOAP server.
    """
    def __init__(self, url, method):
        self.url = url
        self.method = method
        self.logger, self.request_log = self.setup_logger()

    def setup_logger(self):
        """
        Creates logger to debug HTTP messages sent and responses received.
        Output should be sent to Nammu's console.
        """
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        request_log = logging.getLogger("requests.packages.urllib3")
        request_log.setLevel(logging.DEBUG)
        request_log.propagate = True
        return logger, request_log

    def create_request(self, **kwargs):
        request = HTTPRequest(self.url, self.method, **kwargs)
        self.request = request

    def send(self):
        """
        Elaborate HTTP POST request and send it to ORACC's server.
        """
        pass

    def get_response(self):
        """
        Check for a response to the request and obtain response zip file.
        """
        pass

    def parse_response(self):
        """
        Extract information sent in server response.
        """
        pass

    def _check_response_ready(self, id):
        """
        Send a HTTP GET request to ORACC's server and retrieve status.
        """
        pass

    def create_request_zip(self):
        """
        Pack attachment in a zip file.
        """
        pass
