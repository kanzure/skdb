"""
Uses SimpleXMLRPCServer's SimpleXMLRPCDispatcher to serve XML-RPC requests

New BSD License
===============
Copyright (c) 2007, Graham Binns

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.
    * Neither the name of the <ORGANIZATION> nor the names of its contributors
      may be used to endorse or promote products derived from this software
      without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
from django.core.exceptions import ImproperlyConfigured
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
from xmlrpclib import Fault
from django.http import HttpResponse, HttpResponseServerError
from django.conf import settings
from django.shortcuts import render_to_response
import sys

# Declare xmlrpcdispatcher correctly depending on our python version
if sys.version_info[:3] >= (2,5,):
    xmlrpcdispatcher = SimpleXMLRPCDispatcher(allow_none=False, encoding=None)
else:
    xmlrpcdispatcher = SimpleXMLRPCDispatcher()

def test_xmlrpc(text):
    """
    Simply returns the args passed to it as a string
    """
    return "Here's a response! %s" % str(locals())

def handle_xmlrpc(request):
    """
    Handles XML-RPC requests. All XML-RPC calls should be forwarded here

    request
        The HttpRequest object that carries the XML-RPC call. If this is a
        GET request, nothing will happen (we only accept POST requests)
    """
    response = HttpResponse()
    if request.method == "POST":
        if settings.DEBUG:
            print request.raw_post_data
        try:
            response.write(
                xmlrpcdispatcher._marshaled_dispatch(request.raw_post_data))
            if settings.DEBUG:
                print response
            return response
        except Exception, e:
            return HttpResponseServerError()
    else:
        return render_to_response(settings.XMLRPC_GET_TEMPLATE)

# Load up any methods that have been registered with the server in settings
for path, name in settings.XMLRPC_METHODS:
    # if "path" is actually a function, just add it without fuss
    if callable(path):
        xmlrpcdispatcher.register_function(path, name)
        continue

    # Otherwise we try and find something that we can call
    i = path.rfind('.')
    module, attr = path[:i], path[i+1:]

    try:
        mod = __import__(module, globals(), locals(), [attr])
    except ImportError, e:
        raise ImproperlyConfigured, "Error registering XML-RPC method: " \
              + "module %s can't be imported" % module

    try:
        func = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured, 'Error registering XML-RPC method: ' \
              + 'module %s doesn\'t define a method "%s"' % (module, attr)

    if not callable(func):
        raise ImproperlyConfigured, 'Error registering XML-RPC method: ' \
              + '"%s" is not callable in module %s' % (attr, module)

    xmlrpcdispatcher.register_function(func, name)
