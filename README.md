# Preface #

This document describes the functionality provided by the xlr-xlr-plugin.

See the **[XL Release Documentation](https://docs.xebialabs.com/xl-release/index.html)** for background information on XL Release and release concepts.

# Overview #

The xlr-xlr-plugin is an XL Release plugin that allows you to:
  * programmatically create a template and assign tags to it
  * invoke (create and start) another release from an existing release. So you can call a subrelease from a parent release.

## Tasks ##

+ Create and Start SubRelease 
  * `templateName`: Name of the template to invoke (`string`) 
  * `releaseTitle`: Name of the sub release instance (`string`)
  * `releaseDescription`: Description of the sub release (`string`)
  * `variables`: Comma separated key-value pairs, e.g. var1=value1,var2=value2 (`string`)

+ Create Template
  * `templateName`: Name of the template to create (`string`)
  * `tags`: Comma separated list of tags to associate with this template e.g. tag1,tag2 (`string`)
