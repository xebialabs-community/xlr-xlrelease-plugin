#
# Copyright 2021 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import json
import sys
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
""" % (templateName, processTags(tags), date.today())

#Check if template already exists - we don't want to create a duplicate
xlrResponse = XLRequest(xlrAPIUrl, 'GET', None, credentials['username'], credentials['password'], 'application/json').send()
if xlrResponse.status == TEMPLATES_FOUND_STATUS:
    data = json.loads(xlrResponse.read())
    for template in data["cis"]:
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
