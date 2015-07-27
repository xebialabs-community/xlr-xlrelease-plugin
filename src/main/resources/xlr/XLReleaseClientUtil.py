#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from xlr.XLReleaseClient import XLReleaseClient


class XLReleaseClientUtil(object):

    @staticmethod
    def createXLReleaseClient(container, username, password):
        client = XLReleaseClient.create_client(container, username, password)
        return client