#
#	XMLRPC Client Basic HTTP Authentication Transport
#	by Troy Melhase <troy at gci.net>
#	as per http://mail.python.org/pipermail/python-list/2003-June/208575.html
#
#	Changes and additions by Smári McCarthy <smari@fabfolk.com>
#
#	Usage:
#>>> srv = XMLRPCAuthenticatedServer("http://host/xmlrpc/path", username="joe", password="secretpassword")
#
#	Traditional usage example:
#>>> auth_tran = BasicHTTPAuthTransport()
#>>> auth_tran.credentials = ("joe", "secretpassword")
#>>> srv = xmlrpclib.Server("http://host/xmlrpc/path", transport=auth_tran)
#
#

import base64
import xmlrpclib


class XMLRPCAuthenticatedServer(xmlrpclib.Server):
	def __init__(self, path, username=None, password=None, encoding=None, verbose=0, allow_none=0, use_datetime=0):
		self.auth_tran = BasicHTTPAuthTransport()
		self.auth_tran.credentials = (username, password)
		xmlrpclib.Server.__init__(self, path, transport=self.auth_tran, encoding=encoding, verbose=verbose, allow_none=allow_none, use_datetime=use_datetime)



class BasicHTTPAuthTransport(xmlrpclib.Transport):
    """ xmlrpclib.Transport subtype that sends Basic HTTP Authorization

        This subclass recognizes xmlrpclib versions '1.0.0' and '0.9.8' and
        adjusts accordingly during class definition.  Using any other
        version of xmlrpclib will raise an exception.
    """
    user_agent = '*py*'
    credentials = ()

    def send_basic_auth(self, connection):
        """ Include HTTP Basic Authorization data in a header """
        auth = base64.encodestring('%s:%s' % self.credentials).strip()
        auth = 'Basic %s' % (auth, )
        connection.putheader('Authorization', auth)

    if xmlrpclib.__version__ in ('1.0.0', '1.0.1'):
        ## override the send_host hook to also send basic auth
        def send_host(self, connection, host):
            xmlrpclib.Transport.send_host(self, connection, host)
            self.send_basic_auth(connection)

    elif xmlrpclib.__version__ == '0.9.8':
        ## override the request method to send all 
        ## the normal and plus basic auth
        def request(self, host, handler, request_body):
            import httplib
            h = httplib.HTTP(host)
            h.putrequest("POST", handler)
            h.putheader("Host", host)
            h.putheader("User-Agent", self.user_agent)
            h.putheader("Content-Type", "text/xml")
            h.putheader("Content-Length", str(len(request_body)))
            self.send_basic_auth(h)
            h.endheaders()

            if request_body:
                h.send(request_body)
            errcode, errmsg, headers = h.getreply()
            if errcode != 200:
                raise xmlrpclib.ProtocolError(host + handler, errcode, \
                    errmsg, headers)
            return self.parse_response(h.getfile())

    else:
        ## don't know what to redefine
        raise TypeError("Unrecognized xmlrpclib version: %s" % \
             (xmlrpclib.__version__, ))

