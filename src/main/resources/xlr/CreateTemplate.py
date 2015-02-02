#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys, string, time
import com.xhaus.jyson.JysonCodec as json
from datetime import date

TEMPLATE_CREATED_STATUS = 200
TEMPLATES_FOUND_STATUS = 200

def processTags(tags):
    result = ""
    if tags is None:
        return result
    else:
        first = True
        for tag in tags.split(','):
            if first:
                first = False
            else:
                result = result + ","
            result = result + "\"%s\"" % (tag)
    return result

if xlrServer is None:
    print "No server provided."
    sys.exit(1)

xlrUrl = xlrServer['url']
xlrUrl = xlrUrl.rstrip("/")

credentials = CredentialsFallback(xlrServer, username, password).getCredentials()

xlrAPIUrl = xlrUrl + '/releases/templates'

#Create Template
content = """
{"title":"%s","tags":[%s],"scheduledStartDate":"%sT23:58:00.000Z","dueDate":null,"plannedDuration":null,"allowConcurrentReleasesFromTrigger":true} 
""" % (templateName, processTags(tags) , date.today())

#Check if template already exists - we don't want to create a duplicate
xlrResponse = XLRequest(xlrAPIUrl, 'GET', None, credentials['username'], credentials['password'], 'application/json').send()
if xlrResponse.status ==TEMPLATES_FOUND_STATUS:
    data = json.loads(xlrResponse.read())
    for template in data:
        if template["title"] == templateName:
            print "ERROR: Template %s already exists - cannot create a duplicate" % (templateName)
            sys.exit(1)

print "New template - Sending content %s" % content

xlrResponse = XLRequest(xlrAPIUrl, 'POST', content, credentials['username'], credentials['password'], 'application/json').send()

templateId = None
if xlrResponse.status == TEMPLATE_CREATED_STATUS:
    data = json.loads(xlrResponse.read())
    templateId = data["id"]
    print "Created %s in XLR" % (templateId)
else:
    print "Failed to create Template in XLR"
    xlrResponse.errorDump()
    sys.exit(1)