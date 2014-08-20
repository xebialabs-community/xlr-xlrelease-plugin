import sys, string, time
import com.xhaus.jyson.JysonCodec as json
from datetime import date

RELEASE_CREATED_STATUS = 200
TEMPLATES_FOUND_STATUS = 200
RELEASE_STARTED_STATUS = 200
RECEIVED_RELEASE_STATUS = 200

def processVariables(variables):
    result = ""
    if variables is None:
        return result
    else:
        first = True
        for variable in variables.split(','):
            if first:
                first = False
            else:
                result = result + ","    
            result = result + "{\"key\":\"${%s}\",\"value\":\"%s\",\"type\":\"DEFAULT\"}" % (variable.split('=', 1)[0],variable.split('=', 1)[1])
    return result

if xlrServer is None:
    print "No server provided."
    sys.exit(1)

xlrUrl = xlrServer['url']

credentials = CredentialsFallback(xlrServer, username, password).getCredentials()

#Get Template id
templateId = None
xlrAPIUrl = xlrUrl + '/releases/templates'
xlrResponse = XLRequest(xlrAPIUrl, 'GET', None, credentials['username'], credentials['password'], 'application/json', None, None).send()
if xlrResponse.status ==TEMPLATES_FOUND_STATUS:
    data = json.loads(xlrResponse.read())
    for template in data:
        if template["title"] == templateName:
            templateId = template["id"]
            print "Found template %s with id %s" % (templateName,templateId)
            break
    if templateId is None:
        print "Failed to find template in XL Release %s" % templateName
        sys.exit(1)
else:
    print "Failed to find template in XL Release %s" % templateName
    xlrResponse.errorDump()
    sys.exit(1)


# Create Release
variables = processVariables(variables)
if releaseDescription is None:
    releaseDescription = ""

content = """
{"title":"%s","description":"%s","scheduledStartDate":"%sT23:58:00.000Z","dueDate":"%sT23:59:00.000Z","plannedDuration":null,"variables":[%s],"tags":[],"flag":{"status":"OK"},"templateId":"%s"}
""" % (releaseTitle, releaseDescription, date.today(), date.today(), variables, templateId)

print "Sending content %s" % content

xlrAPIUrl = xlrUrl + '/releases'

xlrResponse = XLRequest(xlrAPIUrl, 'POST', content, credentials['username'], credentials['password'], 'application/json', None, None).send()

releaseId = None
if xlrResponse.status == RELEASE_CREATED_STATUS:
    data = json.loads(xlrResponse.read())
    releaseId = data["id"]
    print "Created %s in XLR" % (releaseId)
else:
    print "Failed to create release in XLR"
    xlrResponse.errorDump()
    sys.exit(1)


# Start Release
content = """
{}
"""

xlrAPIUrl = xlrUrl + '/releases/' + releaseId + "/start"
xlrResponse = XLRequest(xlrAPIUrl, 'POST', content, credentials['username'], credentials['password'], 'application/json', None, None).send()
if xlrResponse.status == RELEASE_STARTED_STATUS:
    print "Started %s in XLR" % (releaseId)
else:
    print "Failed to start release in XLR"
    xlrResponse.errorDump()
    sys.exit(1) 


# Wait for subrelease to be finished
xlrAPIUrl = xlrUrl + '/releases/' + releaseId

while True:
    xlrResponse = XLRequest(xlrAPIUrl, 'GET', None, credentials['username'], credentials['password'], 'application/json', None, None).send()
    if xlrResponse.status == RECEIVED_RELEASE_STATUS:
        data = json.loads(xlrResponse.read())
        status = data["status"]
        if status == "COMPLETED":
            print "Subrelease %s completed in XLR" % (releaseId)
            break
        if status == "ABORTED":
            print "Subrelease %s aborted in XLR" % (releaseId)
            sys.exit(1)
    else:
        print "Failed to get release status in XLR"
        xlrResponse.errorDump()
        sys.exit(1) 
    time.sleep(5)