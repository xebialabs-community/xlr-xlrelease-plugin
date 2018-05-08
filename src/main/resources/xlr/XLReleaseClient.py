#
# Copyright 2018 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import json
import urllib

from distutils.version import LooseVersion
from xlr.HttpClient import HttpClient

class XLReleaseClient(object):
    def __init__(self, http_connection, username=None, password=None):
        self.http_request = HttpClient(http_connection, username, password)

    @staticmethod
    def create_client(http_connection, username=None, password=None):
        return XLReleaseClient(http_connection, username, password)

    def get_version(self):
        xlr_api_url = '/server/info'
        xlr_response = self.http_request.get_request(
            xlr_api_url, additional_headers={"Accept": "application/json"})
        xlr_response.raise_for_status()
        data = xlr_response.json()
        return data["version"]

    def _is_using_filter(self):
        return LooseVersion(self.get_version()) < LooseVersion("7.2.0")

    def get_template(self, template_name):
        if self._is_using_filter():
            xlr_api_url = '/api/v1/templates?filter=%s' % urllib.quote(
                template_name)
        else:
            xlr_api_url = '/api/v1/templates?title=%s' % urllib.quote(
                template_name)

        print "Going to use xlr_api_url: ", xlr_api_url
        xlr_response = self.http_request.get_request(
            xlr_api_url, additional_headers={"Accept": "application/json"})
        xlr_response.raise_for_status()
        data = xlr_response.json()
        for template in data:
            if template["title"] == template_name:
                print "Found template %s with id %s" % (
                    template_name, template["id"])
                return template

    def create_release(self, release_title, release_description, variables, template):
        content = """
        {"releaseTitle" : "%s", "releaseVariables" : %s, "scheduledStartDate" : null, "autoStart" : true }
        """ % (release_title, variables)
        print "Sending content %s" % content
        xlr_api_url = '/api/v1/templates/%s/create' % template["id"]
        xlr_response = self.http_request.post_request(xlr_api_url, content, additional_headers={"Accept": "application/json",
                                                                                                "Content-Type": "application/json"})

        xlr_response.raise_for_status()
        data = xlr_response.json()
        release_id = data["id"]
        print "Created [%s](#/releases/%s) in XLR\n" % (release_id,
                                                        release_id.replace("Applications/", ""))
        self.update_release(data, release_description)
        return release_id

    def update_release(self, release, release_description):
        release["description"] = release_description
        xlr_api_url = '/api/v1/releases/%s' % release["id"]
        xlr_response = self.http_request.put_request(xlr_api_url, json.dumps(release), additional_headers={"Accept": "application/json",
                                                                                                           "Content-Type": "application/json"})
        xlr_response.raise_for_status()

    def get_release_status(self, release_id):
        xlr_api_url = '/api/v1/releases/%s' % release_id
        xlr_response = self.http_request.get_request(
            xlr_api_url, additional_headers={"Accept": "application/json"})
        xlr_response.raise_for_status()
        data = xlr_response.json()
        return data["status"]

    def get_updatable_variables(self, template_id):
        xlr_api_url = '/api/v1/releases/%s/variables' % template_id
        xlr_response = self.http_request.get_request(
            xlr_api_url, additional_headers={"Accept": "application/json"})
        xlr_response.raise_for_status()
        return xlr_response.json()

    def add_new_task(self, new_task_title, new_task_type, container_id):
        xlr_api_url = '/tasks/%s' % container_id
        content = {"title": new_task_title, "taskType": new_task_type}
        xlr_response = self.http_request.post_request(xlr_api_url, json.dumps(content),
                                                      additional_headers={"Accept": "application/json",
                                                                          "Content-Type": "application/json"})
        xlr_response.raise_for_status()
        print "Created %s\n" % new_task_title
        return xlr_response.json()

    def update_task(self, updated_task):
        xlr_api_url = '/tasks/%s' % updated_task['id']
        content = updated_task
        xlr_response = self.http_request.put_request(xlr_api_url, json.dumps(content),
                                                     additional_headers={"Accept": "application/json",
                                                                         "Content-Type": "application/json"})
        xlr_response.raise_for_status()
        print "Updated task %s\n" % updated_task['title']

    def add_link(self, container_id, source_task_id, target_task_id):
        xlr_api_url = '/planning/links/%s' % container_id
        content = {"sourceId": source_task_id, "targetId": target_task_id}
        xlr_response = self.http_request.post_request(xlr_api_url, json.dumps(content),
                                                      additional_headers={"Accept": "application/json",
                                                                          "Content-Type": "application/json"})
        xlr_response.raise_for_status()
        print "Added task link\n"

    def add_dependency(self, dependency_release_id, gate_task_id):
        # the internal api uses a rel-phase-task format instead of Applications/Rel/Phase/Task
        # is there a cleaner way to do this??
        # TODO move to public API once it is possible using the public API
        internal_format_task_id = gate_task_id.replace(
            'Applications/', '').replace('/', '-')

        xlr_api_url = '/gates/%s/dependencies' % internal_format_task_id
        content = {"target": {"releaseId": dependency_release_id}}
        xlr_response = self.http_request.post_request(xlr_api_url, json.dumps(content),
                                                      additional_headers={"Accept": "application/json",
                                                                          "Content-Type": "application/json"})
        xlr_response.raise_for_status()
        print "Dependency added to Gate task\n"

    def delete_phase(self, phase_id):
        phase_id = phase_id.replace("Applications/", "").replace("/", "-")
        xlr_response = self.http_request.delete_request('/phases/%s' % phase_id,
                                                        additional_headers={"Accept": "application/json"})
        xlr_response.raise_for_status()
        print "Deleted phase with id [%s]\n" % phase_id
