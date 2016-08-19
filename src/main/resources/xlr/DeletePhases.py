#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys

from xlr.XLReleaseClientUtil import XLReleaseClientUtil

if xlrServer is None:
    print "No server provided."
    sys.exit(1)


xlr_client = XLReleaseClientUtil.create_xl_release_client(xlrServer, username, password)


phases = phases.split(",")
idlist = []

release_phases = dict((release_phase.title,release_phase.id) for release_phase in release.phases)
for phase in phases:
    if phase in release_phases.keys():
        print "Found matching phase [%s] for deletion.\n" % phase
        idlist.append(release_phases.get(phase))
    else:
        print "Did not find phase with title [%s]. Failing \n" % phase
        sys.exit(1)

# Delete all relevant phases from the release
for id in idlist:
    xlr_client.delete_phase(id)