#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
---
module: behave
version_added: "2.3"
short_description: This is a wrapper module around behave
description:
  - short_description: Handle execution of behave tests (http://pythonhosted.org/behave/)
options:
  path:
    description:
      Absolute path of the directory containing the "features" directory.
    required: true
  name:
    description:
      name of the feature files to run. If not provided all feature
      files found in path will be executed.
    required: false
    default: ""
  language:
    description: language of the feature files.
    required: false
  tags:
    description:
        List of tags to select for the execution. The list must be comma
        separated without spaces.
    required: false
    default: None
  output_format:
    description:
        By default the output of the features execution is stored in a file
        with the default formatter. The formatter can be changed by
        specifying the formatter name in output_format.
    default: 'pretty'
    required: false
  output_name:
    description:
        Name of the file where the behave output will be stored.
    default: "{feature}_result"
             where "{feature}" will be replaced by the feature filename
    required: false
  output_dir:
    description:
        Directory where the behave output file will be written.
    default: "/tmp"
    required: false
'''

EXAMPLES = '''
# run all features available under /home/foo/tests
behave:
  path: /home/foo/tests

# run all features and specify the language of the files to french
behave:
  path: /home/foo/tests
  language: fr

# run only base.feature under /home/foo/tests
behave:
  path: /home/foo/tests
  name: "base.feature"

# run base.feature and store output result in "base.feature.output" as json
behave:
  path: /home/foo/tests
  name: "base.feature"
  output_format: json.pretty
  output_name: "base.feature.output"
'''

def main():

    argument_spec = dict(
        path = dict(required=True, type='str'),
        name = dict(required=False, type='str', default=None),
        language = dict(required=False, type='str', default='fr',
                        choices=['fr', 'en']),
        tags = dict(required=False,  type='str', default=None),
        output_format = dict(required=False, type='str', default='pretty',
                             choices=['pretty', 'json.pretty']),
        output_name = dict(required=False, type='str',
                           default="{feature}_result"),
        output_dir = dict(required=False, type='str', default="/tmp"),
    )

    module = AnsibleModule(argument_spec=argument_spec)

    path  = module.params.get('path')
    name = module.params.get('name')
    language = module.params.get('language')
    tags = module.params.get('tags')
    output_format = module.params.get('output_format')
    output_name = module.params.get('output_name')
    output_dir = module.params.get('output_dir')

    if "{feature}" not in output_name:
        module.fail_json(
            msg="The {feature} formatter is required in output_name string")
    else:
        output_name = output_name.format(feature=os.path.basename(name))

    FEAT = ""
    if name:
        FEAT = "--include %s" % name

    LANG = ""
    if language:
        LANG = "--lang %s" % language

    TAGS= ""
    if tags is not None:
        TAGS = "--tags=%s" % tags

    FORMAT = "--format %s" % output_format
    OUTPUT = "--outfile %s" % os.path.join(output_dir, output_name)

    CMD = "behave {lang} {tags} {formatter} {output} {feature}"

    rc, stdout, stderr = module.run_command(
        CMD.format(lang=LANG, tags=TAGS, formatter=FORMAT,
                   output=OUTPUT.format(feature=name), feature=FEAT),
        cwd=path)

    if rc != 0:
        module.fail_json(changed=False, stdout=stdout, stderr=stderr,
                         msg="feature has at least one error",
                         feature=name)
    module.exit_json(changed=False, feature=name, stdout=stdout)

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

if __name__ == "__main__":
    main()
