#
# Copyright 2018 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
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
