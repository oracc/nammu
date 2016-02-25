from email.mime.application import MIMEApplication
from email.encoders import encode_7or8bit
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

class HTTPRequest:
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
        else:
            pass

    def create_request_message(self, command, keys, attachment):
        self.create_soap_envelope(command=command, keys=keys, attachment=attachment)
        # mtompkg = self.create_mtom_package(type='multipart', host=self.url, envelope=self.envelope, attachment=attachment)
        #
        # mtompkg = MIMEMultipart('related',boundary='============boundary============', charset='utf-8', type='application/xop+xml', start='<SOAP-ENV:Envelope>')
        # #Doesn't like the hyphen in start-info when passing as MIMEMultipart param
        # mtompkg.set_param('start-info', 'application/soap+xml')
        # mtompkg['Host'] = "http://oracc.museum.upenn.edu:8085"
        # mtompkg['Connection'] = "close"
        # del(mtompkg['mime-version'])
        #
        # rootpkg = MIMEApplication(envelope, 'xop+xml', encode_7or8bit)
        # rootpkg.set_param('charset', 'utf-8')
        # rootpkg.set_param('type', 'application/soap+xml')
        # rootpkg.add_header('Content-ID', '<SOAP-ENV:Envelope>')
        # del(rootpkg['Content-Transfer-Encoding'])
        # rootpkg.add_header('Content-Transfer-Encoding', 'binary')
        # del(rootpkg['mime-version'])
        #
        # mtompkg.attach(rootpkg)
        #
        # document = MIMEBase('*','*')
        # document['Content-Transfer-Encoding'] = "binary"
        # document['Content-ID'] = "<id6>"
        # filename = "./osc-debug-2/request.zip"
        # document.set_payload(open(filename,'rb').read())
        # del(document['mime-version'])
        #
        # mtompkg.attach(document)
        #
        #
        # # extract body string from MIMEMultipart message
        # bound = '--%s' % (mtompkg.get_boundary(), )
        # marray = mtompkg.as_string().split(bound)
        # mtombody = bound
        # mtombody += bound.join(marray[1:])
        #
        # # set Content-Length
        # mtompkg.add_header("Content-Length", str(len(mtombody)))

    def create_response_message(self, keys):
        self.create_soap_envelope(keys=keys)

    def create_soap_envelope(self, **kwargs):
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
            osc_data_keys += '\n                            <osc-data:key>{}</osc-data:key>'.format(key)

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

    def generate_boundary(self):
        """
        Generate random boundary to separate HTTP POST request's areas.
        """
        pass

    def generate_cid(self):
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

    def handle_server_error(self):
        """
        Raise an exception when server can't be reached or request times out.
        """
        pass
