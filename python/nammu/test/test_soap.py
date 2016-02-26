import pytest
import xml.dom.minidom
from ..SOAPClient.SOAPClient import SOAPClient
from ..SOAPClient.HTTPRequest import HTTPRequest

class TestSOAP:
    def setup(self):
        pass

    def teardown(self):
        pass

    def test_send_request(self):
        pass

    # def test_http_post_headers(self):
    #     goal_headers = {
    #         'Connection': 'close',
    #         'Content-Type': 'multipart/related; start="<SOAP-ENV:Envelope>"; charset="utf-8"; type="application/xop+xml"; boundary="============boundary============"; start-info="application/soap+xml"',
    #         'Host': 'http://oracc.museum.upenn.edu:8085'
    #     }
    #     client = SOAPClient('http://oracc.museum.upenn.edu:8085', method='POST')
    #     request = client.create_request()
    #     test_headers = requests.get_headers()
    #     assert test_headers == goal_headers
    #
    # def test_http_get_headers(self):
    #     goal_headers = {
    #         'Connection': 'close',
    #         'Content-Type': 'multipart/related; start="<SOAP-ENV:Envelope>"; charset="utf-8"; type="application/xop+xml"; boundary="============boundary============"; start-info="application/soap+xml"',
    #         'Host': 'http://oracc.museum.upenn.edu:8085'
    #     }
    #     client = SOAPClient('http://oracc.museum.upenn.edu:8085', method='POST')
    #     request = client.create_request()
    #     test_headers = requests.get_headers()
    #     assert test_headers == goal_headers

    def test_soap_request_envelope(self):
        goal_envelope = """<?xml version="1.0" encoding="UTF-8"?>
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
                    <osc-meth:Request>
                        <osc-data:keys>
                            <osc-data:key>atf</osc-data:key>
                            <osc-data:key>tests/mini</osc-data:key>
                            <osc-data:key>00atf/hyphens.atf</osc-data:key>
                        </osc-data:keys>
                        <osc-data:data>
                            <osc-data:item xmime5:contentType="*/*">
                                <xop:Include href="cid:request_zip"/>
                            </osc-data:item>
                        </osc-data:data>
                    </osc-meth:Request>
                </SOAP-ENV:Body>
            </SOAP-ENV:Envelope>"""
        client = SOAPClient('http://oracc.museum.upenn.edu:8085', method='POST')
        client.create_request(command='atf',
                              keys=['tests/mini', '00atf/hyphens.atf'],
                              attachment='resources/test/request.zip')
        test_envelope = client.request.get_soap_envelope()
        assert self.compare_soap_envelopes(test_envelope, goal_envelope)

    def test_soap_response_envelope(self):
        goal_envelope = """<?xml version="1.0" encoding="UTF-8"?>
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
                    <osc-meth:Response>
                        <osc-data:keys>
                            <osc-data:key>ZO3vNg</osc-data:key>
                        </osc-data:keys>
                    </osc-meth:Response>
                </SOAP-ENV:Body>
            </SOAP-ENV:Envelope>"""
        client = SOAPClient('http://oracc.museum.upenn.edu:8085', method='POST')
        client.create_request(keys=['ZO3vNg'])
        test_envelope = client.request.get_soap_envelope()
        assert self.compare_soap_envelopes(test_envelope, goal_envelope)

    def compare_soap_envelopes(self, test, goal):
        test_xml = xml.dom.minidom.parseString(test)
        goal_xml = xml.dom.minidom.parseString(goal)
        return self.pretty_print(test_xml) == self.pretty_print(goal_xml)

    def pretty_print(self, str):
        pretty_str = ''
        for line in str.toprettyxml().split('\n'):
            if not line.strip() == '':
                pretty_str += line
        return pretty_str

    def test_http_payload(self):
        pass

    def test_get_response_ok(self):
        pass

    def test_http_body(self):
        pass

    def test_response_ready(self):
        pass
