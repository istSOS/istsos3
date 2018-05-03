# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.entity.baseEntity import BaseEntity
import collections


class Term(BaseEntity):
    """
    /req/base/vocab-term
    A controlled term used in a data instance shall be encoded as a JSON
    object containing the text value in a property “term”, and an optional
    source vocabulary in a property “vocabulary”. If present, the value of
    “vocabulary” shall be a URI denoting a controlled vocabulary.
    """

    json_schema = {
        "type": "object",
        "properties": {
            "aterm": {"type": "string"},
            "vocabulary": {"type": "string"}
        },
        "required": ["term"]
    }
