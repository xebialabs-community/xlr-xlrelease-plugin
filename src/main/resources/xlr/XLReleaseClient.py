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
        xlr_api_url = '/api/v1/templates?filter=%s' % urllib.quote(template_name)
        print "Going to use xlr_api_url: ", xlr_api_url
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
        xlr_api_url = 'api/v1/releases/%s/variables' % template_id
        xlr_response = self.httpRequest.get(xlr_api_url, contentType='application/json')
        if xlr_response.isSuccessful():
            data = json.loads(xlr_response.getResponse())
            return data
        else:
            print "Failed to get variables in XLR"
            xlr_response.errorDump()
            raise ServerError(str(xlr_response.getResponse()))

    def add_new_task(self, newTaskTitle, newTaskType, containerId):
      xlr_api_url = '/tasks/%s' % containerId
      content = {"title":newTaskTitle,"taskType":newTaskType}
      xlr_response = self.httpRequest.post(xlr_api_url, json.dumps(content), contentType='application/json')
      if xlr_response.isSuccessful():
        newTask = json.loads(xlr_response.getResponse())
        print "Created %s\n" % newTaskTitle
      else:
        print "Failed to create %s\n" % newTaskTitle
        print xlr_response.errorDump()
        sys.exit(1)  
      return newTask

    def update_task(self, updatedTask):
      xlr_api_url = '/tasks/%s' % updatedTask['id']
      content = updatedTask
      xlr_response = self.httpRequest.put(xlr_api_url, json.dumps(content), contentType='application/json')
      if xlr_response.isSuccessful():
        print "Updated task %s\n" % updatedTask['title']
      else:
        print "Failed to update task\n" % updatedTask['title']
        print xlr_response.errorDump()
        sys.exit(1)

    def add_link(self, containerId, sourceTaskId, targetTaskId):
      xlr_api_url = '/planning/links/%s' % containerId
      content = {"sourceId":sourceTaskId,"targetId":targetTaskId}
      xlr_response = self.httpRequest.post(xlr_api_url, json.dumps(content), contentType='application/json')
      if xlr_response.isSuccessful():
        print "Added task link\n"
      else:
        print "Failed to task link\n"
        print xlr_response.errorDump()
        sys.exit(1)

    def add_dependency(self, dependencyReleaseId, gateTaskId):
        # the internal api uses a rel-phase-task format instead of Applications/Rel/Phase/Task
        # is there a cleaner way to do this??
        # TODO move to public API once it is possible using the public API
        internal_format_task_id = gateTaskId.replace('Applications/', '').replace('/', '-')
        
        xlr_api_url = '/gates/%s/dependencies' % internal_format_task_id
        content = { "target": { "releaseId" : dependencyReleaseId } }
        xlr_response = self.httpRequest.post(xlr_api_url, json.dumps(content), contentType='application/json')

        if xlr_response.isSuccessful():
            print "Dependency added to Gate task\n"
        else:
            print "Failed to add dependency\n"
            print xlr_response.errorDump()
            sys.exit(1)

