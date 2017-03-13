#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


class HttpResponse:
    def getStatus(self):
        """
        Gets the status code
        :return: the http status code
        """
        return self.status

    def getResponse(self):
        """
        Gets the response content
        :return: the reponse as text
        """
        return self.response

    def isSuccessful(self):
        """
        Checks if request successful
        :return: true if successful, false otherwise
        """
        return 200 <= self.status < 400

    def getHeaders(self):
        """
        Returns the response headers
        :return: a dictionary of all response headers
        """
        return self.headers

    def errorDump(self):
        """
        Dumps the whole response
        """
        print 'Status: ', self.status, '\n'
        print 'Response: ', self.response, '\n'
        print 'Response headers: ', self.headers, '\n'

    def __init__(self, status, response, headers):
        self.status = status
        self.response = response
        self.headers = {}
        for header in headers:
            self.headers[str(header.getName())] = str(header.getValue())
