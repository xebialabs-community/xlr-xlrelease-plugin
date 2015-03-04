#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys

currentRelease = getCurrentRelease()
tasks = taskApi.searchTasksByTitle(taskTitle, None, currentRelease.id)

taskPath = None
for task in tasks:
    print "Received task with title: [%s].\n" % task.title
    if task.title == taskTitle and task.status == "PLANNED":
        taskId = task.id
        break

if taskId:
    print "Task with title [%s] found with id [%s].\n" % (taskTitle, taskId)
    sys.exit(0)
    
print "Task with title [%s] not found.\n" % taskTitle
sys.exit(1)