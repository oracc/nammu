'''
Copyright 2015 - 2018 University College London.

This file is part of Nammu.

Nammu is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Nammu is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Nammu.  If not, see <http://www.gnu.org/licenses/>.
'''


import StringIO
import re
import os
import logging
import logging.config
import requests
import urllib
from java.lang import System, ClassLoader
from zipfile import ZipFile
from logging import Formatter
from requests.exceptions import RequestException, ConnectTimeout
from HTTPRequest import HTTPRequest
import xml.etree.ElementTree as ET


class SOAPClient(object):
    """
    Sends and retrieves information to and from the ORACC SOAP server.
    """
    def __init__(self, url, port, url_dir, method):
        self.url = url
        self.port = port
        self.url_dir = url_dir
        self.method = method
        # TODO: Create logger in this module that reuses nammu controller's
        # logger configuration so output is in same file, but tells us it was
        # produced in this module.
        self.logger, self.request_log = self.setup_logger()

    def create_request(self, **kwargs):
        url = "{}:{}".format(self.url, self.port)
        request = HTTPRequest(url, self.method, **kwargs)
        self.request = request

    def send(self):
        """
        Elaborate HTTP POST request and send it to ORACC's server.
        """
        url = "{}:{}".format(self.url, self.port)
        headers = dict(self.request.get_headers())
        body = self.request.get_body()
        self.logger.debug("Sending request to server at %s.", url)
        self.logger.debug("HTTP request headers sent: %s", headers)
        self.logger.debug("HTTP request body sent: %s", body)
        try:
            self.response = requests.post(url, data=body, headers=headers,
                                          timeout=3)
        except ConnectTimeout:
            self.logger.error('Connection timed out when sending POST '
                              'request.')
            raise

    def get_response_text(self):
        return self.response.text

    def get_response_id(self):
        xml_root = ET.fromstring(self.response.text)
        # This should be done with xpath. See XPath and namespaces sections
        # here: https://docs.python.org/2/library/xml.etree.elementtree.html
        return xml_root[0][0][0][0].text

    def wait_for_response(self, request_id):
        """
        Check for a response to the request and obtain response zip file.
        Since it's an asynchronous communication, when sending a request for
        validation or lemmatisation, the server returns an ID for us to ask
        via HTTP GET until the request is ready.
        The response from the server can be:
        * "run\n" (request is being processed)
        * "done\n" (request is ready - we can send a new SOAP request to get
                    it)
        *  "err_stat\n" (something bad happened and we have to mail Steve)
        """
        url = "{}/{}/{}".format(self.url, self.url_dir, request_id)
        while True:
            try:
                response = requests.get(url)
            except RequestException:
                raise
            else:
                if response.text == "done\n":
                    return
                elif response.text == "err_stat\n":
                    raise Exception("UnknownServerError")

    def get_response(self):
        return self.response.content

    def get_server_logs(self):
        """
        Manipulate response to substract the content of oracc.log that is in
        the returned binary-coded zip file.
        """
        self.response.content
        binary_body = re.split('--==.*==',
                               self.response.content)[2].split('\r\n')[5]

        f = StringIO.StringIO()
        f.write(bytearray(binary_body))

        memory_zip = ZipFile(f)
        namelist = memory_zip.namelist()
        zip_content = {name: memory_zip.read(name) for name in namelist}
        oracc_log = zip_content['oracc.log']
        request_log = zip_content['request.log']

        # Check if server returns a lemmatised file
        autolem = None
        for key, value in zip_content.iteritems():
            if key.endswith("autolem.atf"):
                autolem = value

        self.logger.debug("The returned file from server contains: %s",
                          zip_content.keys())

        for file in zip_content.keys():
            self.logger.debug("These are the contents of %s: \n%s",
                              file,
                              zip_content[file])

        return oracc_log, request_log, autolem

    def setup_logger(self):
        """
        Creates logger for Nammu's functionality as well as to debug HTTP
        messages sent to the ORACC server and responses received.
        Output should be sent to Nammu's console as well as a local logfile and
        the system console.
        """
        logger = logging.getLogger("SOAPClient")
        requests_logger = logging.getLogger("requests.packages.urllib3")

        return logger, requests_logger
