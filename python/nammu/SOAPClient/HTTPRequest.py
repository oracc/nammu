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

import zipfile
from email.mime.application import MIMEApplication
from email.encoders import encode_7or8bit
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from cStringIO import StringIO


class HTTPRequest(object):
    '''
    Builds an HTTP GET or POST request that ORACC's server understands to send
    and retrieve ATF data.
    '''
    def __init__(self, url, method, **kwargs):
        self.method = method
        self.url = url
        if method == 'POST':
            if 'command' in kwargs.keys():
                self.create_request_message(kwargs['command'], kwargs['keys'],
                                            kwargs['atf_basename'],
                                            kwargs['atf_text'])
            else:
                self.create_response_message(kwargs['keys'])

    def create_request_message(self, command, keys, atf_basename, atf_text):
        """
        Send attachment to server containing ATF file and necessary data to
        run given command (validate, lemmatise, etc).
        """
        self.mtompkg = MIMEMultipart('related')
        self.set_multipart_params()
        self.set_soap_envelope(command=command,
                               keys=keys,
                               atf_basename=atf_basename,
                               atf_text=atf_text)
        self.rootpkg = MIMEApplication(self.envelope,
                                       'xop+xml',
                                       encode_7or8bit)
        self.set_multipart_payload()
        self.document = MIMEBase('*', '*')
        self.set_document_payload(atf_basename, atf_text)

        # The headers can't be created until the body is finished since they
        # need it to populate the Content-Length header
        self.set_multipart_headers()

    def create_response_message(self, keys):
        """
        Asks the server for the response request.zip attachment containing
        validated/lemmatised/etc ATF file.
        """
        self.set_soap_envelope(keys=keys)
        self.mtompkg = MIMEApplication(self.envelope,
                                       'soap+xml',
                                       encode_7or8bit)
        self.mtompkg.add_header("Host", self.url)

    def set_response_headers(self):
        del(self.mtompkg['Content-Transfer-Encoding'])
        headers = ['Host', 'Content-Length', 'Connection']
        values = [self.url, '623', 'close']
        for header, value in zip(headers, values):
            self.mtompkg.add_header(header, value)

    def set_response_params(self):
        self.mtompkg.set_param('charset', 'utf-8')

    def set_multipart_payload(self):
        self.set_payload_headers()
        self.set_payload_params()
        self.mtompkg.attach(self.rootpkg)

    def set_document_payload(self, atf_basename, atf_text):
        self.set_document_headers()

        mem_data = StringIO()
        mem_zip = zipfile.ZipFile(mem_data, "w", zipfile.ZIP_DEFLATED, False)
        mem_zip.writestr("00atf/"+atf_basename, atf_text)
        mem_zip.close()
        mem_data.seek(0)

        self.document.set_payload(mem_data.getvalue())
        self.mtompkg.attach(self.document)

    def set_document_headers(self):
        headers = ['Content-ID', 'Content-Transfer-Encoding']
        values = ['<request_zip>', 'binary']
        for header, value in zip(headers, values):
            self.document.add_header(header, value)

    def set_payload_params(self):
        params = ['charset', 'type']
        values = ['utf-8', 'application/soap+xml']
        for param, value in zip(params, values):
            self.rootpkg.set_param(param, value)

    def set_payload_headers(self):
        # Content-Transfer-Encoding is set to 7bit by default
        del(self.rootpkg['Content-Transfer-Encoding'])
        headers = ['Content-ID', 'Content-Transfer-Encoding']
        values = ['<SOAP-ENV:Envelope>', 'binary']
        for header, value in zip(headers, values):
            self.rootpkg.add_header(header, value)

    def set_multipart_headers(self):
        headers = ['Host', 'Content-Length', 'Connection']
        values = [self.url, str(len(self.get_body())), 'close']
        for header, value in zip(headers, values):
            self.mtompkg.add_header(header, value)

    def set_multipart_params(self):
        params = ['charset', 'type', 'start', 'start-info', 'boundary']
        values = ['utf-8', 'application/xop+xml', '<SOAP-ENV:Envelope>',
                  'application/soap+xml', '==========boundary========']
        for param, value in zip(params, values):
            self.mtompkg.set_param(param, value)

    def set_soap_envelope(self, **kwargs):
        """
        Format SOAP envelope to be attached in HTTP POST request.
        """
        # The number of keys in the SOAP envelope depends on the command and
        # the message type (Request/Response)
        keys = ''  # osc-data keys

        # Only Request messages have data, but the template has a reference to
        # it in both cases.
        data = ''

        if 'command' in kwargs.keys():
            keys += '<osc-data:key>{}</osc-data:key>'.format(kwargs['command'])
            message_type = 'Request'
            data += """<osc-data:data>
                            <osc-data:item xmime5:contentType="*/*">
                                <xop:Include href="cid:request_zip"/>
                            </osc-data:item>
                        </osc-data:data>"""
        else:
            message_type = 'Response'

        for key in kwargs['keys']:
            keys += '<osc-data:key>{}</osc-data:key>'.format(key)

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
                                           keys=keys,
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
        Returns the body of the HTTP POST request containing the soap envelope
        including the encoded compressed ATF.
        """
        # Header and body on a HTTP SOAP/MTOM message is separated by \n\n
        body = self.mtompkg.as_string().split('\n\n', 1)[1]

        # This returns the randomly created boundary string, which separates
        # the different elements in the request (document, envelope and
        # payload)
        bound = self.mtompkg.get_boundary()

        # There's two different kinds of SOAP HTTP POST requests handled, due
        # to the communication with the server being asynchronous:
        # * One that contains an ATF attachment submitted for validation/lemm
        # * One that contains only a request ID to ask for the validated/lemm'd
        #   ATF.
        # The boundary will be empty in the second case.
        if bound is not None:
            # Encoded zip files start with "\n\nPK" and end with a new line
            # follwed by the ending boundary (in the form "--random_boundary--"
            attachment = body.split("\n\nPK")[1].split("\n--" + str(bound))[0]
            # Some line endings are \n and some are \r\n. The email module
            # automatically replaces some of them causing the server not to
            # understand line endings correctly. For this, we need to first
            # make sure all of the line endings are \n, then convert them all
            # to \r\n (to avoid having '\r\n' converted to '\r\r\n'.
            # Note the encoding of the zipped ATF might coincidentally contain
            # a '\n' substring. We have to avoid replacing those, otherwise
            # the zipped ATF will be corrupt and imposible to open by the
            # server.
            body = body.replace(attachment, '<attachment>')
            body = body.replace('\r\n', '\n').replace('\n', '\r\n')
            body = body.replace("<attachment>", attachment)
        else:
            body = body.replace('\r\n', '\n').replace('\n', '\r\n')

        return body
