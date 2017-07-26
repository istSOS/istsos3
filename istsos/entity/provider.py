# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.entity.baseEntity import BaseEntity


class Provider(BaseEntity):
    json_schema = {
        "type": "object",
        "properties": {
            "providerName": {
                "type": "string"
            },
            "providerSite": {
                "type": "string"
            },
            "serviceContact": {
                "type": "object",
                "properties": {
                    "individualName": {
                        "type": "string"
                    },
                    "positionName": {
                        "type": "string"
                    },
                    "serviceContact": {
                        "type": "object",
                        "properties": {
                            "phone": {
                                "type": "string"
                            },
                            "fax": {
                                "type": "string"
                            },
                        }
                    },
                    "address": {
                        "type": "object",
                        "properties": {
                            "deliveryPoint": {
                                "type": "string"
                            },
                            "city": {
                                "type": "string"
                            },
                            "administrativeArea": {
                                "type": "string"
                            },
                            "postalCode": {
                                "type": "string"
                            },
                            "country": {
                                "type": "string"
                            },
                            "email": {
                                "type": "string"
                            }
                        }
                    }
                }
            }
        }
    }

    @staticmethod
    def get_template():
        return {
            "providerName": "",
            "providerSite": "",
            "serviceContact": {
                "individualName": "",
                "positionName": "",
                "contactInfo": {
                    "phone": "",
                    "fax": ""
                },
                "address": {
                    "deliveryPoint": "",
                    "city": "",
                    "administrativeArea": "",
                    "postalCode": "",
                    "country": "",
                    "email": ""
                }
            }
        }
