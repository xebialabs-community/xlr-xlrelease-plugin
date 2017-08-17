#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import json

TASK_CREATED_STATUS = 200

if xlrServer is None:
    print "No server provided."
    sys.exit(1)

xlr_url = xlrServer['url']
xlr_url = xlr_url.rstrip("/")

credentials = CredentialsFallback(xlrServer, username, password).getCredentials()

target_release = releaseApi.searchReleasesByTitle(releaseName)
target_phase = phaseApi.searchPhasesByTitle(phaseName, target_release[0].id)

xlr_api_url = xlr_url + '/api/v1/tasks/' + target_phase[0].id + '/tasks'
xld_server_url = xlr_url + '/api/v1/config/byTypeAndTitle?configurationType=xldeploy.XLDeployServer&title=' + xldServer['title']

xlr_server_response = XLRequest(xld_server_url, 'GET', None, credentials['username'], credentials['password'], 'application/json').send()

xlr_server_data = json.loads(xlr_server_response.read())

content = {
    "id":"null",
    "type": "xlrelease.CustomScriptTask",
    "pythonScript": {
        "type": "xldeploy.Deploy",
        "id": "null",
        "server": xlr_server_data[0],
        "deploymentPackage":deploymentPackage,
        "deploymentEnvironment":deploymentEnvironment,
        "rollbackOnFailure": rollbackOnFailure
    },
    "title": taskTitle
}

xlr_response = XLRequest(xlr_api_url, 'POST', json.dumps(content), credentials['username'], credentials['password'], 'application/json').send()

if xlr_response.status == TASK_CREATED_STATUS:
    data = json.loads(xlr_response.read())
    task_id = data["id"]
    print "Created task %s with id %s in %s release." % (taskTitle, task_id, releaseName)
else:
    print "Failed to create Task in %s release." % (releaseName)
    xlr_response.errorDump()
    sys.exit(1)
