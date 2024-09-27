import asyncio
from istsos import setting
from istsos.entity.rest.response import Response
from istsos.actions.action import CompositeAction


class UnitConvPost(CompositeAction):

    @asyncio.coroutine
    def before(self, request):
        """
            Request example: {
            "action": "UNIT_CONVERSION_USING_POSTGRESQL_UNIT",
                "data": {
                    "offerings": ["belin"],
                    "observedProperties": [
                        "urn:ogc:def:parameter:x-istsos:1.0:temperature"
                    ],
                    "download_file": {
                        "file_name": "testing3",
                        "location": "istsos/plugins/unit_con_post/download_file/"
                    },
                    "in_unit":"degC",
                    "operation": {
                        "type":"add",
                        "qty": "3",
                        "unit": "degF"
                    },
                    "responseFormat": "application/json;subtype='array'"
                }
            }
        """
        yield from self.add_plugin("unit_con_post", "UnitConversionPo_sql_unit")

    @asyncio.coroutine
    def after(self, request):
        request['response'] = Response(
            json_source=Response.get_template({
                "data": request['observations'],
                "headers": request['headers']
            })
        )