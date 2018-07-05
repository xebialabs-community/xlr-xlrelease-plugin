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
import sys
import time

from xlr.XLReleaseClientUtil import XLReleaseClientUtil
from xlr.XLReleaseClient import XLReleaseClient

def find_planned_gate_task(tasks):
    for task in tasks:
        if task.getType() == "xlrelease.GateTask" and task["status"] == "PLANNED":
            return task

def process_variables(variables, variable_map, updatable_variables):
    var_map = {}
    result = {}
    if variables is not None:
        for variable in variables.split(','):
            var_map[variable.split('=', 1)[0]]= variable.split('=', 1)[1]

    var_map.update(variable_map)

    for updatable_variable in updatable_variables:
        key = str(updatable_variable["key"]).strip("${").strip("}")
        if key in var_map:
            updatable_variable["value"] = var_map[key]
            result[key] = updatable_variable["value"]

    return json.dumps(result).replace("None","null").replace("True","true").replace("False","false")

if xlrServer is None:
    print "No server provided."
    sys.exit(1)

xlr_client = XLReleaseClientUtil.create_xl_release_client(xlrServer, username, password)

#Get Template id
template = xlr_client.get_template(templateName)

# Create Release
updatable_variables = xlr_client.get_updatable_variables(template["id"])
vars = process_variables(variables, variableMap, updatable_variables)
if releaseDescription is None:
    releaseDescription = ""

release_id = xlr_client.create_release(releaseTitle, releaseDescription, vars, template)

# Wait for subrelease to be finished (only if asynch is false)
while not asynch:
    status = xlr_client.get_release_status(release_id)
    print "Subrelease [%s](#/releases/%s) has status [%s] in XLR\n" % (
            releaseTitle, XLReleaseClient.get_release_url(release_id), status)
    if status == "COMPLETED":
        break
    if status == "ABORTED":
        sys.exit(1)
    time.sleep(5)

if gateTaskTitle:
    tasks = taskApi.searchTasksByTitle(gateTaskTitle, None, getCurrentRelease().id)
    task = find_planned_gate_task(tasks)

    if task is None:
        print "Couldn't find a planned gate task with title %s in current release." % gateTaskTitle
        sys.exit(1)

    xlr_client.add_dependency(release_id, task.id)    

