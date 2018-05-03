# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.entity.baseEntity import BaseEntity
from istsos.entity.om_base_entity.eventTime import (
    EventTime,
    EventTimeInstant
)
from istsos.entity.om_base_entity.measure import Measure
# from istsos.entity.om_base_entity.geoJson import Point
from istsos.entity.om_base_entity.link import Link
from istsos import setting


class Specimen(BaseEntity):
    """
    An object on which measurements may be made, often ex-situ. Note that if
    this specimen is a "processed" version of another (e.g. by grinding,
    sieving, etc) then the predecessor (if known) may be recorded as a
    relatedSamplingFeature.

     "description": If present, the textual description of the sample

     "identifier": The identifier of the specimen

     "name": The name f the specimen, used as reference name for observations

     "type": The specimen type: "Specimen"

     "sampledFeature": The feature that is sampled.
        EXAMPLE: Lugano Lake, Mount Everest, Highway 24.

     "materialClass": The attribute materialClass:GenericName shall provide a
        basic classification of the material type of the specimen.
        EXAMPLE: soil, water, rock, aqueous, liquid, tissue,
        vegetableMatter, food, gas, solid.

     "samplingTime": The attribute samplingTime:TM_Object shall record when
        the specimen was retrieved from the sampled feature.

     "samplingMethod": If present, the attribute
        shall describe the method used to obtain the specimen from its
        sampledFeature.

     "samplingLocation": If present, the attribute
        shall describe the location from where the specimen was obtained.
        NOTE: Where a specimen has a relatedSamplingFeature whose location
        provides an unambiguous location then this attribute is not
        required. However, if the specific sampling location within the
        sampledFeature is important, then this attribute supports its
        description.

     "processingDetails": In many applications specimen preparation
        procedures are applied to the material prior to its use in
        an observation. The class PreparationStep (Figure 13) shall link
        a SF_Specimen to a OM_Process that describes a phase of the
        specimen preparation. It shall support one attribute.

     "size": If present, the attribute size:Measure shall describe a
        physical extent of the specimen. This may be length, mass, volume,
        etc as appropriate for the specimen instance and its material class.

     "currentLocation": If present, the attribute shall
        describe the location of a physical specimen. This may be a storage
        location, such as a shelf in a warehouse or a drawer in a museum.
        NOTE: If a specimen no longer exists, for example it was destroyed in
        connection with an observation act, then the currentLocation should
        be omitted or carry a suitable null indicator.

     "specimenType": If present, the attribute specimenType:GenericName
        shall describe the basic form of the specimen.
        EXAMPLE:	polished section; core; pulp; solution

    """
    json_schema = {
        "type": "object",
        "properties": {
            "id": {
                "type": "integer"
            },
            "offering": {
                "type": "string"
            },
            "prefix": {
                "type": "string"
            },
            "name": {
                "type": "string"
            },
            "description": {
                "type": "string"
            },
            "identifier": {
                "type": "string",
                "minLength": 1
            },
            "type": {
                "type": "string",
                "enum": [
                    setting._SAMPLING_SPECIMEN
                ]
            },
            "sampledFeature": Link.json_schema,
            "materialClass": Link.json_schema,
            "samplingTime": EventTime.json_schema,
            "samplingMethod": {
                "oneOf": [
                    Link.json_schema,
                    {"type": "null"}
                ]
            },
            #  "samplingLocation": Point.json_schema,
            "processingDetails": {
                "type": "array",
                "items": {
                    "type": ["object", "null"],
                    "properties": {
                        "processOperator": Link.json_schema,
                        "processingDetails": Link.json_schema,
                        "time": EventTimeInstant.json_schema
                    },
                    "additionalProperties": False
                }
            },
            "size": Measure.json_schema,
            "currentLocation": Link.json_schema,
            "specimenType": {
                "oneOf": [
                    {"type": "null"},
                    Link.json_schema
                ]
            }
        },
        "required": [
            "description",
            "identifier",
            "name",
            "type",
            "sampledFeature",
            "materialClass",
            "samplingTime",
            "samplingMethod",
            # "samplingLocation",
            "size",
            "currentLocation",
            "specimenType"
        ],
        "additionalProperties": False
    }

    @staticmethod
    def get_template(specimen=None):
        ret = {
            "description": "",
            "identifier": "",
            "name": "",
            "type": setting._SAMPLING_SPECIMEN,
            "sampledFeature": "",
            "materialClass": "",
            "samplingTime": "",
            "samplingMethod": "",
            # "samplingLocation": "",
            "size": Measure.get_template(),
            "currentLocation": "",
            "specimenType": ""
        }
        if specimen is not None:
            ret.update(specimen)
        return ret
