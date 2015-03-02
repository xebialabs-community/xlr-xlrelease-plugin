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
    if task.title == taskTitle:
        taskPath = task.id
        break

if taskPath:
    print "Task with title [%s] found with id [%s].\n" % (taskTitle, taskPath)
    taskPath = taskPath.replace('/','-')
    prefix = 'Applications-'
    taskId = taskPath
    if taskPath.startswith(prefix):
       taskId = taskPath[len(prefix):]
    sys.exit(0)
    
print "Task with title [%s] not found.\n" % taskTitle
sys.exit(1)