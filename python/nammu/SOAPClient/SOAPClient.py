import requests
import logging
import re
import StringIO
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import httplib as http_client
from HTTPRequest import HTTPRequest

class SOAPClient(object):
    """
    Sends and retrieves information to and from the ORACC SOAP server.
    """
    def __init__(self, url, method):
        self.url = url
        self.method = method
        logging.basicConfig()
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
        url = "http://oracc.museum.upenn.edu:8085"
        headers = dict(self.request.get_headers())
        body = self.request.get_body()
        self.response = requests.post(url, data=body, headers=headers)
        # try:
        #    response = requests.post(url, data=body, headers=headers, timeout=10)
        # except ReadTimeout:
        #          print "Timed out!"

    def get_response_text(self):
        return self.response.text

    def get_response_id(self):
        xml_root = ET.fromstring(self.response.text)
        # This should be done with xpath. See XPath and namespaces sections
        # here: https://docs.python.org/2/library/xml.etree.elementtree.html
        return xml_root[0][0][0][0].text

    def wait_for_response(self, id):
        """
        Check for a response to the request and obtain response zip file.
        """
        while True:
            ready_response = requests.get('http://oracc.museum.upenn.edu/p/' + id)
            if ready_response.text == "done\n":
                return

    def get_response(self):
        return self.response.content

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

    def get_oracc_log(self):
        """
        Manipulate response to substract the content of oracc.log that is in the
        returned binary-coded zip file.
        """
        self.response.content
        binary_body = re.split('--==.*==', self.response.content)[2].split('\r\n')[5]

        f = StringIO.StringIO()
        f.write(bytearray(binary_body))

        # if zipfile.is_zipfile(f):
        memory_zip = ZipFile(f)
        zip_content = {name: memory_zip.read(name) for name in memory_zip.namelist()}
        oracc_log = zip_content['oracc.log']

        return oracc_log
