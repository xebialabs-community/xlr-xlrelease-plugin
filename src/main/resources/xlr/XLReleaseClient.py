#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import urllib
from datetime import date
import com.xhaus.jyson.JysonCodec as json
from httputil.HttpRequest import HttpRequest

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class AuthenticationError(Error):
    def __init__(self, msg):
        self.msg = msg

class ServerError(Error):
    def __init__(self, msg):
        self.msg = msg


class XLTemplate(object):
    def __init__(self, id, tags):
        self.id = id
        self.tags = tags

class XLReleaseClient(object):
    def __init__(self, http_connection, username=None, password=None):
        self.httpRequest = HttpRequest(http_connection, username, password)

    @staticmethod
    def create_client(http_connection, username=None, password=None):
        return XLReleaseClient(http_connection, username, password)


    def get_template(self, template_name):
        filter = {'filter': template_name}
        xlr_api_url = '/api/v1/templates?%s' % urllib.urlencode(filter)
        xlr_response = self.httpRequest.get(xlr_api_url, contentType='application/json')
        if xlr_response.isSuccessful():
            data = json.loads(xlr_response.getResponse())
            for template in data:
                if template["title"] == template_name:
                    print "Found template %s with id %s" % (template_name, template["id"])
                    return XLTemplate(template["id"],[str(t) for t in template["tags"]])
        print "Failed to find template in XL Release %s" % template_name
        xlr_response.errorDump()
        raise ServerError(str(xlr_response.getResponse()))


    def create_release(self, release_title, release_description, variables, tags, template_id):
        content = """
        {"title":"%s","description":"%s","scheduledStartDate":"%sT23:58:00.000Z","dueDate":"%sT23:59:00.000Z","plannedDuration":null,"variables":%s,"tags":%s,"flag":{"status":"OK"},"templateId":"%s"}
        """ % (release_title, release_description, date.today(), date.today(), variables, tags, template_id)

        print "Sending content %s" % content

        xlr_api_url = '/releases'
        xlr_response = self.httpRequest.post(xlr_api_url, content, contentType='application/json')

        if xlr_response.isSuccessful():
            data = json.loads(xlr_response.getResponse())
            release_id = data["id"]
            print "Created %s in XLR" % release_id
            return release_id
        else:
            print "Failed to create release in XLR"
            xlr_response.errorDump()
            raise ServerError(str(xlr_response.getResponse()))


    def start_release(self, release_id):
        # Start Release
        content = """
        {}
        """

        xlr_api_url = '/releases/' + release_id + "/start"
        xlr_response = self.httpRequest.post(xlr_api_url, content, contentType='application/json')
        if xlr_response.isSuccessful():
            print "Started %s in XLR" % (release_id)
        else:
            print "Failed to start release in XLR"
            xlr_response.errorDump()
            raise ServerError(str(xlr_response.getResponse()))


    def get_release_status(self, release_id):
        xlr_api_url = '/releases/' + release_id
        xlr_response = self.httpRequest.get(xlr_api_url, contentType='application/json')
        if xlr_response.isSuccessful():
            data = json.loads(xlr_response.getResponse())
            status = data["status"]
            print "Subrelease [%s] has status [%s] in XLR" % (release_id,status)
            return status
        else:
            print "Failed to get release status in XLR"
            xlr_response.errorDump()
            raise ServerError(str(xlr_response.getResponse()))

    def get_updatable_variables(self,template_id):
        xlr_api_url = '/releases/%s/updatable-variables' % template_id.split("/")[1]
        xlr_response = self.httpRequest.get(xlr_api_url, contentType='application/json')
        if xlr_response.isSuccessful():
            data = json.loads(xlr_response.getResponse())
            return data
        else:
            print "Failed to get variables in XLR"
            xlr_response.errorDump()
            raise ServerError(str(xlr_response.getResponse()))