import sys
from com.xebialabs.deployit.exception import NotFoundException


if 'Release' not in targetId:
    print("Passed ID does not look like a release ID: [%s]" % targetId)
    sys.exit(1)

# get target release from current or archived DB
try:
    targetRelease = releaseApi.getRelease(targetId)
except NotFoundException:
    targetRelease = releaseApi.getArchivedRelease(targetId)

status = str(targetRelease.getStatus())
if status in ['COMPLETED', 'FAILED', 'ABORTED']:
    targetStatus = status
else:
    # continue polling
    task.setStatusLine('Release is %s' % status.lower().replace('_', ' '))
    task.schedule('xlr/FailableGateTask.py')
