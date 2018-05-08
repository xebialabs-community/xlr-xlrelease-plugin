#
# Copyright 2018 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import requests

class HttpClient(object):
    def __init__(self, http_connection, username=None, password=None):
        self.http_connection = http_connection
        self.url = http_connection['url']
        self.username = username if username else http_connection['username']
        self.password = password if password else http_connection['password']
        self.proxy = None
        if http_connection['proxyHost']:
            self.proxy = {'http': '%s:%s' % (http_connection['proxyHost'], http_connection['proxyPort'])}
        self.verify_ssl = http_connection['enableSslVerification']

    def get_request(self, context_root, additional_headers=None):
        request_url = self.url + context_root
        return requests.get(request_url, auth=(self.username, self.password), headers=additional_headers,
                            proxies=self.proxy, verify=self.verify_ssl)

    def post_request(self, context_root, content, additional_headers=None):
        request_url = self.url + context_root
        return requests.post(request_url, auth=(self.username, self.password), headers=additional_headers,
                             proxies=self.proxy, verify=self.verify_ssl, data=content)

    def put_request(self, context_root, content, additional_headers=None):
        request_url = self.url + context_root
        return requests.put(request_url, auth=(self.username, self.password), headers=additional_headers,
                            proxies=self.proxy, verify=self.verify_ssl, data=content)

    def delete_request(self, context_root, additional_headers=None):
        request_url = self.url + context_root
        return requests.delete(request_url, auth=(self.username, self.password), headers=additional_headers,
                               proxies=self.proxy, verify=self.verify_ssl)


