#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys
import time

from xlr.XLReleaseClientUtil import XLReleaseClientUtil

def find_planned_gate_task(tasks):
    for task in tasks:
        if task.getType() == "xlrelease.GateTask" and task["status"] == "PLANNED":
            return task

def process_variables(variables, updatable_variables):
    var_map = {}
    if variables is not None:
        for variable in variables.split(','):
            var_map[variable.split('=', 1)[0]]= variable.split('=', 1)[1]

    for updatable_variable in updatable_variables:
        key = str(updatable_variable["key"]).strip("${").strip("}")
        if key in var_map:
            updatable_variable["value"] = var_map[key]

    return str(updatable_variables).replace("u'","'").replace("'", '"').replace("None","null").replace("True","true").replace("False","false")

if xlrServer is None:
    print "No server provided."
    sys.exit(1)

xlr_client = XLReleaseClientUtil.create_xl_release_client(xlrServer, username, password)

#Get Template id
template = xlr_client.get_template(templateName)

# Create Release
updatable_variables = xlr_client.get_updatable_variables(template.id)
vars = process_variables(variables, updatable_variables)
if releaseDescription is None:
    releaseDescription = ""

release_id = xlr_client.create_release(releaseTitle, releaseDescription, vars, repr(template.tags).replace("'",'"'), template.id.split("/")[1])

# Start Release
xlr_client.start_release(release_id)

# Wait for subrelease to be finished (only if asynch is false)
while not asynch:
    status = xlr_client.get_release_status(release_id)
    if status == "COMPLETED":
        print "Subrelease %s completed in XLR" % (release_id)
        break
    if status == "ABORTED":
        print "Subrelease %s aborted in XLR" % (release_id)
        sys.exit(1)
    time.sleep(5)

if gateTaskTitle:
    tasks = taskApi.searchTasksByTitle(gateTaskTitle, None, getCurrentRelease().id)
    task = find_planned_gate_task(tasks)

    if task is None:
        print "Couldn't find a planned gate task with title %s in current release." % gateTaskTitle
        sys.exit(1)

    xlr_client.add_dependency(release_id, task.id)    

