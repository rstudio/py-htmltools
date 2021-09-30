#!/usr/bin/env python3

import os
from typing import List
import urllib
import urllib.request
import json

# Change known-tags to master once this gets merged
# https://github.com/rstudio/htmltools/pull/286
url = "https://raw.githubusercontent.com/rstudio/htmltools/known-tags/scripts/known_tags.json"
with urllib.request.urlopen(url) as u:
    tags = json.loads(u.read().decode())

tags_code: List[str] = []
for nm in tags:
    # We don't have any immediate need for tags.head() since you can achieve
    # the same effect with an 'anonymous' dependency (i.e.,
    # htmlDependency(head = ....))
    if nm == "head":
        continue
    # TODO: still provide this, but with underscores?
    if nm == "del":
        continue
    # TODO: this probably should be removed from the R pkg??
    if nm == "color-profile":
        continue
    code = f"def {nm}(*args: TagChild, children: Optional[List[TagChild]] = None, **kwargs: AttrType) -> tag:\n" + \
           f"    return tag('{nm}', *args, children=children, **kwargs)\n"
    tags_code.append(code)

header = """\
# Do not edit by hand; this file is generated by ./scripts/generate_tags.py
from typing import Optional, List

from .core import tag, TagChild, AttrType

"""

src_file = os.path.join(os.path.dirname(__file__), '../htmltools/tags.py')
with open(src_file, 'w') as f:
    src = header + '\n'.join(tags_code)
    f.write(src)
