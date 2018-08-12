# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import istsos
from istsos.entity.rest.response import Response
from istsos.actions.action import CompositeAction


class UnitConversionPo_sql_unit(CompositeAction):

    @asyncio.coroutine
    def process(self, request):
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
        # Add filters
        request.set_filter(request.get_rest_data())
        # Adding action Offering retriever
        yield from self.add_retriever_unit_conversion('Offerings')
        # yield from self.add_retriever('Offerings')
        yield from self.add_retriever_unit_conversion('Observations')

    @asyncio.coroutine
    def after(self, request):
        pass

    @asyncio.coroutine
    def add_retriever_unit_conversion(self, action, filter=None):
        self.add((yield from get_retrievers_unit_conversion(action, filter=filter)))



@asyncio.coroutine
def get_retrievers_unit_conversion(name, **kwargs):
    action = yield from __get_plugin_proxy(
        'plugins.unit_con_post.retrievers', name, **kwargs)
    return action


@asyncio.coroutine
def __get_plugin_proxy(istsos_package, action_module, **kwargs):
    from istsos import setting
    import importlib
    state = yield from setting.get_state()
    fileName = action_module[0].lower() + action_module[1:]
    module = 'istsos.%s.%s.%s' % (
        istsos_package,
        state.config["loader"]["type"],
        fileName
    )

    istsos.debug("Importing %s.%s" % (module, action_module))
    try:
        m = importlib.import_module(module)
    except Exception:
        module = 'istsos.%s.%s' % (
            istsos_package,
            fileName
        )
        m = importlib.import_module(module)

    m = getattr(m, action_module)
    if kwargs is not None:
        return m(**kwargs)
    return m()