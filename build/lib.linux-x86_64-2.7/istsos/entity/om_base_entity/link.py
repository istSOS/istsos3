# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.entity.baseEntity import BaseEntity

url = (
    "^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+"
    "[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"
)


class Link(BaseEntity):
    """
    /req/base/link
    A hyperlink used in a data instance shall be encoded as a JSON object,
    with a property “href” carrying the URI of the external resource, an
    optional “rel” property providing the semantics of the reference, and an
    optional “title” property providing a human readable label for the
    reference.
    """

    json_schema = {
        "type": "object",
        "properties": {
            "href": {
                "type": "string"
                # "pattern": url
            },
            "rel": {"type": "string"},
            "title": {"type": "string"}
        },
        "required": ["href"],
        "additionalProperties": False
    }
