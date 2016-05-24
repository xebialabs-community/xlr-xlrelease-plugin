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

xlr_client = XLReleaseClientUtil.createXLReleaseClient(xlrServer, username, password)

xlr_client.restart_phase(getCurrentRelease().id, fromPhaseId, fromTaskId)

