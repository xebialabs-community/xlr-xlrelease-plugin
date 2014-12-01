# Preface #

This document describes the functionality provided by the xlr-xlr-plugin.

See the **XL Release Reference Manual** for background information on XL Release and release concepts.

# Overview #

The xlr-xlr-plugin is a XL Release plugin that allows to 
  * invoke (create and start) another template from an existing template. So you can call from a parent template a subtemplate.
  * create a template and associate users/groups to teams within that template

## Types ##

+ Create and Start SubRelease 
  * `templateName`: Name of the template to invoke (`string`) 
  * `releaseTitle`: Name of the sub release instance (`string`)
  * `releaseDescription`: Description of the sub release (`string`)
  * `variables`: Comma separated key value pairs, e.g. key1=value1,key2=value2 (`string`)

+ Create Template
  * `templateName`: Name of the template to create (`string`)
  * `tags`: Comma separated list of tags to associate with this template e.g. tag1,tag2 (`string`)
