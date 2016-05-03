#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys
import time
import pprint

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

from xlr.XLReleaseClientUtil import XLReleaseClientUtil

def report_variables(variables):
    print bcolors.OKBLUE + bcolors.BOLD + "inbound variables"
    print "-----------------------------------"
    print bcolors.OKGREEN + "{0:25s}|{1:25s} ".format('key', 'value')
    for k,v in variables.items():
        print bcolors.BOLD + '{0:25s}| {1:25s}'.format(k,v)



def report_updatable_variables(updatable_variables, final=False):

    if final:
        print bcolors.OKBLUE + bcolors.BOLD + "final variable mapping"
    else:
        print bcolors.OKBLUE + bcolors.BOLD + "variables in target template needed to be mapped"

    print "-----------------------------------"
    print bcolors.OKGREEN + '{0:25s} |{1:25s} |{2:25s}'.format("key", "type", "value")

    for var in updatable_variables:
        key = var['key'].replace('${', '').replace('}', '')
        type = var['type'].replace('DEFAULT', 'string')

        print bcolors.BOLD + ' {0:25s}| {1:25s}| {2:15s}'.format(key, type, var['value'])


def process_variables(variables, updatable_variables):

    var_map = {}
    if variables is not None:
        for variable in variables.split(','):
            var_map[variable.split('=', 1)[0]]= variable.split('=', 1)[1]

    report_variables(var_map)

    for updatable_variable in updatable_variables:
        key = str(updatable_variable["key"]).strip("${").strip("}")
        if key in var_map:
            updatable_variable["value"] = var_map[key]
        else:
            print bcolors.FAIL + "required variable not found : %s " % (key)
            system.exit(2)

    report_updatable_variables(updatable_variables, final=True)

    return str(updatable_variables).replace("u'","'").replace("'", '"').replace("None","null")


if xlrServer is None:
    print bcolors.FAIL + "No server provided."
    sys.exit(1)

xlr_client = XLReleaseClientUtil.createXLReleaseClient(xlrServer, username, password)

#Get Template id
template = xlr_client.get_template(templateName)

# Create Release
updatable_variables = xlr_client.get_updatable_variables(template.id)
vars = process_variables(variables, updatable_variables)
if releaseDescription is None:
    releaseDescription = ""

release_id = xlr_client.create_release(releaseTitle, releaseDescription, vars, repr(template.tags).replace("'",'"'), template.id.split("/")[1])
# Start Release
xlr_client.start_release(release_id)

# Wait for subrelease to be finished (only if asynch is true)
while not asynch:
    status = xlr_client.get_release_status(release_id)
    if status == "COMPLETED":
        print bcolors.OKGREEN + "Subrelease %s completed in XLR" % (release_id)
        break
    if status == "ABORTED":
        print bcolors.FAIL + "Subrelease %s aborted in XLR" % (release_id)
        sys.exit(1)
    time.sleep(int(checkSubReleaseInterval))