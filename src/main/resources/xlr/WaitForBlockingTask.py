#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

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
