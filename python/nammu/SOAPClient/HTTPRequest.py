from email.mime.application import MIMEApplication
from email.encoders import encode_7or8bit
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

class HTTPRequest(object):
    """
    Builds an HTTP GET or POST request that ORACC's server understands to send
    and retrieve ATF data.
    """
    def __init__(self, url, method, **kwargs):
        self.method = method
        self.url = url
        if method == 'POST':
            if 'command' in kwargs.keys():
                self.create_request_message(kwargs['command'], kwargs['keys'],
                                            kwargs['attachment'])
            else:
                self.create_response_message(kwargs['keys'])

    def create_request_message(self, command, keys, attachment):
        """
        Send attachment to server containing ATF file and necessary data to
        run given command (validate, lemmatise, etc).
        """
        self.mtompkg = MIMEMultipart('related')
        self.set_multipart_params()
        self.set_soap_envelope(command=command,
                               keys=keys,
                               attachment=attachment)

        self.rootpkg = MIMEApplication(self.envelope, 'xop+xml', encode_7or8bit)
        self.set_multipart_payload()

        #The headers can't be created until the body is finished since they need
        #it to populate the Content-Length header
        self.set_multipart_headers()

    def create_response_message(self, keys):
        """
        Asks the server for the response request.zip attachment containing
        validated/lemmantised/etc ATF file.
        """
        self.set_soap_envelope(keys=keys)

    def create_request_body(self):
        pass

    def create_request_headers(self):
        envelope_headers = ['Content-ID', 'Content-Transfer-Encoding']
        envelope_header_values = ['<SOAP-ENV:Envelope>', 'binary']
        attachment_header_values = ['request_zip', 'binary']
        self.request_headers = \
            dict(zip(request_headers, request_header_values))
        self.envelope_headers = \
            dict(zip(envelope_headers, envelope_header_values))
        self.attachment_headers = \
            dict(zip(envelope_headers, attachment_header_values))

    def set_multipart_payload(self):
        self.set_multipart_params()
        self.set_multipart_headers()
        self.mtompkg.attach(self.rootpkg)


    def set_multipart_params(self):
        params = ['charset', 'type']
        values = ['utf-8', 'application/soap+xml']
        for param, value in dict(zip(params, values)).iteritems():
            self.rootpkg.set_param(param, value)

    def set_multipart_headers(self):
        headers = ['Content-ID', 'Content-Transfer-Encoding']
        values = ['<SOAP-ENV:Envelope>', 'binary']
        for header, value in dict(zip(header, value)):
            self.rootpkg.add_header(header, value)

    def set_multipart_headers(self):
        headers = ['Host', 'Content-Length', 'Connection']
        # values = [self.url, len(str(self.mtombody)), 'close']
        values = [self.url, '1500', 'close']
        for header, value in dict(zip(headers, values)).iteritems():
            self.mtompkg.add_header(header, value)

    def set_multipart_params(self):
        params = ['boundary', 'charset', 'type', 'start', 'start-info']
        values = ['============boundary============', 'utf-8',
            'application/xop+xml', '<SOAP-ENV:Envelope>', 'application/soap+xml']
        for param, value in dict(zip(params, values)).iteritems():
            self.mtompkg.set_param(param, value)
    #
    # def set_element_params(self, params, values, element):
    #     d = dict(zip(params, values))
    #     for param, value in d.iteritems():
    #         element.set_param(param, value)
    #     return element
    #
    # def set_element_headers(self, headers, values, element):
    #     d = dict(zip(headers, values))
    #     for header, value in d.iteritems():
    #         element.add_header(header, value)
    #     return element

    def set_soap_envelope(self, **kwargs):
        """
        Format SOAP envelope to be attached in HTTP POST request.
        """
        #The number of keys in the SOAP envelope depends on the command and
        #the message type (Request/Response)
        osc_data_keys = ''

        #Only Request messages have data, but the template has a reference to
        #it in both cases.
        data = ''

        if 'command' in kwargs.keys():
            osc_data_keys += '<osc-data:key>{}</osc-data:key>'.format(kwargs['command'])
            message_type = 'Request'
            data += """<osc-data:data>
                            <osc-data:item xmime5:contentType="*/*">
                                <xop:Include href="cid:request_zip"/>
                            </osc-data:item>
                        </osc-data:data>"""
        else:
            message_type = 'Response'

        for key in kwargs['keys']:
            osc_data_keys += '<osc-data:key>{}</osc-data:key>'.format(key)

        envelope = """<?xml version="1.0" encoding="UTF-8"?>
            <SOAP-ENV:Envelope
                xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope"
                xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                xmlns:xop="http://www.w3.org/2004/08/xop/include"
                xmlns:xmime5="http://www.w3.org/2005/05/xmlmime"
                xmlns:osc-data="http://oracc.org/wsdl/ows.xsd"
                xmlns:osc-meth="http://oracc.org/wsdl/ows.wsdl">
                <SOAP-ENV:Body>
                    <osc-meth:{type}>
                        <osc-data:keys>
                            {keys}
                        </osc-data:keys>
                        {data}
                    </osc-meth:{type}>
                </SOAP-ENV:Body>
            </SOAP-ENV:Envelope>""".format(type=message_type,
                                           keys=osc_data_keys,
                                           data=data)
        self.envelope = envelope

    def get_soap_envelope(self):
        return self.envelope

    def get_headers(self):
        """
        Return dict with message headers - ready to use by requests module.
        """
        return dict(self.mtompkg.items())

    def get_body(self):
        """
        Return dict with message body/payload - ready to use by requests module.
        """
        pass

    def handle_server_error(self):
        """
        Raise an exception when server can't be reached or request times out.
        """
        pass
