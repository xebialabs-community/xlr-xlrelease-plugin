#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#
from xlr.XLReleaseClientUtil import XLReleaseClientUtil

if xlrServer is None:
    raise Exception("No server provided.")

if phases is None and len(phasesToDelete) == 0:
    raise Exception("At least one of \"phases (deprecated)\" or \"phases\" should have a value")

xlr_client = XLReleaseClientUtil.create_xl_release_client(xlrServer, username, password)

phases_to_delete = []
if len(phasesToDelete) > 0:
    phases_to_delete = phasesToDelete
else:
    phases_to_delete = phases.split(",")

id_list = []
release_phases = dict((release_phase.title, release_phase.id) for release_phase in release.phases)
for phase in phases_to_delete:
    if phase in release_phases.keys():
        print "Found matching phase [%s] for deletion.\n" % phase
        id_list.append(release_phases.get(phase))
    else:
        raise Exception("Did not find phase with title [%s]. Failing \n" % phase)

# Delete all relevant phases from the release
for id in id_list:
    xlr_client.delete_phase(id)
