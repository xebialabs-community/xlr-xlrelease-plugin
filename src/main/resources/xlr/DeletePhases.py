#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys, string, time, urllib
import com.xhaus.jyson.JysonCodec as json

if xlrServer is None:
    print "No server provided."
    sys.exit(1)

xlrUrl = xlrServer['url']
xlrUrl = xlrUrl.rstrip("/")

credentials = CredentialsFallback(xlrServer, username, password).getCredentials()

phases = phases.split(",")
idlist = []

# find any matching phase in the existing release (release.id)
request = HttpRequest({'url': xlrUrl}, credentials['username'], credentials['password'])
response = request.get('/releases/' + release.id.split("/")[1], contentType = 'application/json')

releasedata = json.loads(response.response)
for phaseToDelete in phases:
    for phase in releasedata['phases']:
        if phase['title'] == phaseToDelete:
            idlist.append(phase['id'])

# Delete all relevant phases from the release

for id in idlist:
    response = request.delete('/phases/' + id, contentType = 'application/json')