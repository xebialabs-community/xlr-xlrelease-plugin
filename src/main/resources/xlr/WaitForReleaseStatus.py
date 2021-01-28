#
# Copyright 2021 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


import sys
import xlr

accepted_statuses = []
if untilInProgress: accepted_statuses.append('IN_PROGRESS')
if untilPaused: accepted_statuses.append('PAUSED')
if untilFailing: accepted_statuses.append('FAILING')
if untilFailed: accepted_statuses.append('FAILED')
if untilCompleted: accepted_statuses.append('COMPLETED')
if untilAborted: accepted_statuses.append('ABORTED')
if not accepted_statuses:
    print("At least one status has to be selected")
    sys.exit(1)

if 'Release' not in targetId:
    print("Passed ID does not look like a release ID: [%s]" % targetId)
    sys.exit(1)

targetRelease = xlr.get_release(releaseApi, targetId)
status = str(targetRelease.getStatus())
if status in accepted_statuses:
    targetStatus = status
else:
    # continue polling
    task.setStatusLine('Release is %s' % status.lower().replace('_', ' '))
    task.schedule('xlr/WaitForReleaseStatus.py')
