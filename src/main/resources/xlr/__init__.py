#
# Copyright 2018 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import os
import tempfile
from com.xebialabs.xlr.ssl import LoaderUtil
from java.nio.file import Files, Paths, StandardCopyOption

def set_ca_bundle_path():
    ca_bundle_path = extract_file_from_jar("requests/cacert.pem")
    os.environ['REQUESTS_CA_BUNDLE'] = ca_bundle_path


def extract_file_from_jar(config_file):
    file_url = LoaderUtil.getResourceBySelfClassLoader(config_file)
    if file_url:
        tmp_file, tmp_abs_path = tempfile.mkstemp()
        tmp_file.close()
        Files.copy(file_url.openStream(), Paths.get(tmp_abs_path), StandardCopyOption.REPLACE_EXISTING)
        return tmp_abs_path
    else:
        return None

if 'REQUESTS_CA_BUNDLE' not in os.environ:
    set_ca_bundle_path()
