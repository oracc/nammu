import StringIO, re, os, logging, logging.config, requests
from java.lang import System
from zipfile import ZipFile
from logging import Formatter
from requests.exceptions import RequestException
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
        self.response = requests.post(url, data=body, headers=headers)

        
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
        * "done\n" (request is ready - we can send a new SOAP request to get it)
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
        Manipulate response to substract the content of oracc.log that is in the
        returned binary-coded zip file.
        """
        self.response.content
        binary_body = re.split('--==.*==', 
                               self.response.content)[2].split('\r\n')[5]

        f = StringIO.StringIO()
        f.write(bytearray(binary_body))

        memory_zip = ZipFile(f)
        zip_content = {name: memory_zip.read(name) for name in memory_zip.namelist()}
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
        
        # First of all check Operating System where we are running to save 
        # log in appropriate place.
        os_name = System.getProperty("os.name").lower()
        if "mac" or "nix" or "nux" or "sunos" or "solaris" in os_name:
            env_var_name = "HOME"
        elif "win" in os_name:
            env_var_name = "USERPROFILE"
            
        try:
            log_dir = os.path.join(os.environ[env_var_name], '.nammu/')
        except KeyError:
            print "OS not recognised: " + os_name
        
        if not os.path.exists(log_dir) and log_dir is not "":
            os.makedirs(log_dir)            
            
        logger = logging.getLogger('SOAPClient')
        logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        file_handler = logging.FileHandler(log_dir + 'nammu.log')
        file_handler.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        # TODO: Users might not be insterested on this.
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # create formatter and add it to the handlers
        formatter = logging.Formatter( 
                        '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                        '%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        # Nammu console format
        console_formatter = logging.Formatter('%(message)s')

        request_log = logging.getLogger("requests.packages.urllib3")
        request_log.addHandler(file_handler)
        request_log.addHandler(console_handler)
        
        request_log.setLevel(logging.DEBUG)
        
        return logger, request_log
    
        