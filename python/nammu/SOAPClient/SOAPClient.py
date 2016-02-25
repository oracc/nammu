import requests
import logging
import httplib as http_client
import HTTPRequestBuilder

# Dunno if this is the right place to set up logging
logging.basicConfig()

class SOAPClient:
    """
    Sends and retrieves information to and from the ORACC SOAP server.
    """
    def __init__(self, url):
        self.url = url
        self.logger, self.request_log = self.set_logger()

    def create_logger(self):
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
