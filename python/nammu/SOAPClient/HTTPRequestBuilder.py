from email.mime.application import MIMEApplication
from email.encoders import encode_7or8bit
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

class HTTPRequestBuilder:
    """
    Builds an HTTP GET or POST request that ORACC's server understands to send
    and retrieve ATF data.
    """
    def __init__(self, **kwargs):
        pass

    def create_soap_envelope(self, **kwargs):
        """
        Format SOAP envelope to be attached in HTTP POST request.
        """
        pass

    def create_request_soap_envelope(self, command, atf_file, zip_file):
        """
        Customizes SOAP envelope with request user options.
        """
        pass

    def create_response_soap_envelope(self, id):
        """
        Customizes SOAP envelope with ATF file's ID.
        """
        pass

    def _generate_boundary(self):
        """
        Generate random boundary to separate HTTP POST request's areas.
        """
        pass

    def _generate_cid(self):
        """
        Generate random reference to attachment.
        """
        pass

    def get_headers(self):
        """
        Return dict with message headers - ready to use by requests module.
        """
        pass

    def get_body(self):
        """
        Return dict with message body/payload - ready to use by requests module.
        """
        pass
