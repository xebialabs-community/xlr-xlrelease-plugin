#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys, string, time
import com.xhaus.jyson.JysonCodec as json
from datetime import date

xlrUrl = xlrServer['url']
xlrUrl = xlrUrl.rstrip("/")

credentials = CredentialsFallback(xlrServer, username, password).getCredentials()

xlrAPIUrl = xlrUrl + '/api/v1/releases'


#server = { 'url': xlrServer['url'], 'username': username, 'password': password, 'proxyHost': proxyHost, 'proxyPort': proxyPort}
#request = HttpRequest(server, username, password)

phase = getCurrentPhase()
task = getCurrentTask()

isRunning = True
pollCount = 0

while isRunning == True :
   pollCount = pollCount + 1
   isRunning = False
   request = XLRequest(xlrAPIUrl, 'GET', None, credentials['username'], credentials['password'], 'application/json').send()
   releases = json.loads(request.read())

   print "Http Status: %s" % request.status
   if request.status == 200:
       for release in releases:
          #print "Release = %s" % (release["title"])
          for phase in release["phases"]:
             #print ">>> Phase = %s" % (phase["title"])
             if phase["title"] == phaseName:
                for task in phase["tasks"]:
                   if task["title"] == taskName or taskName == "*" :
                      print ">>>***id = %s, title = %s***" % ( task["id"], task["title"] )
                      print "   Status = %s " % ( task["status"] )
                      if task["status"] == "IN_PROGRESS" :
                         isRunning = True
                         break
                   # End if
                # End for
             # End if
             if isRunning == True :
                break
          # End for
          if isRunning == True :
                break
       # End for
   else:
       print "Failed to connect at %s." % URL
       response.errorDump()
       #sys.exit(1)
   # End if
   if isRunning :
      time.sleep( pollInterval )
   if pollCount >= maxPolls :
       if maxPolls > 0:
          print "Max Polls reached.  Exiting"
          sys.exit(1)
       # End if
   # End if
   print "Is Running? %s " % (isRunning)
# End while
sys.exit(0)
