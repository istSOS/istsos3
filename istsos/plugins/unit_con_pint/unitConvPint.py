# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import json
import csv
import istsos
from istsos import setting
from istsos.entity.rest.response import Response
from istsos.actions.action import CompositeAction
from .lookUpTable import LookUpTable
from pint import UnitRegistry, set_application_registry
ureg = UnitRegistry(autoconvert_offset_to_baseunit = True)
set_application_registry(ureg)
Q_ = ureg.Quantity



class UnitConvPint(CompositeAction, LookUpTable):

    @asyncio.coroutine
    def before(self, request):
        """
            Request example:{
                "action": "UNIT_CONVERSION_USING_PINT",
                "data": {
                    "offerings": ["belin"],
                    "observedProperties": [
                        "urn:ogc:def:parameter:x-istsos:1.0:temperature"
                    ],
                    "download_file": {
                        "file_name": "pint1",
                        "location": "istsos/plugins/unit_con_post/download_file/"
                    },
                    "operation": {
                        "type":"add",
                        "qty": "3",
                        "unit": "degK"
                    },
                    "responseFormat": "application/json;subtype='array'",
                    "in_unit":"degK"
                }
            }
        """
        yield from self.add_plugin("unit_con_pint", "UnitConversionPint")

    @asyncio.coroutine
    def after(self, request):
        headers = [{
            "type": "datetime",
            "name": "Phenomenon Time",
            "column": "e"
        }]

        from_unit = request['offerings'][0]['observable_properties'][0]['uom']
        from_unit = yield from self.findLookUp(from_unit)
        converted_data = []
        to_unit = ''
        if request.get_filter("responseFormat") in setting._responseFormat['array']:
            recs = request['observations'].copy()
            if request.get_filter("in_unit") is not None:
                to_unit = request.get_filter("in_unit")
                to_unit = yield from self.findLookUp(to_unit)
                if request.get_filter("operation") is not None:
                    if 'unit' in request.get_filter("operation"):
                        unit = yield from self.findLookUp(request.get_filter("operation")['unit'])
                        if 'qty' in request.get_filter("operation"):
                            qty = request.get_filter("operation")['qty']
                            if 'type' in request.get_filter("operation"):
                                if request.get_filter("operation")['type'] == 'add':
                                    if qty == '':
                                        qty = 0
                                    for rec in recs:
                                        operation = """%s*%sopr%s*%s"""%(rec[1], from_unit, qty, unit)
                                        src, dst = operation.split('opr')
                                        if(from_unit == 'degC' and unit == 'degC'):
                                            conversion = Q_(src)+Q_(dst).to('delta_degC')
                                        elif(from_unit == 'degC'):
                                            conversion = Q_(src)+Q_(dst).to('delta_degC')
                                        elif(unit == 'degC'):
                                            conversion = Q_(src)+Q_(dst).to('delta_degC')
                                        else:
                                            conversion = Q_(src)+Q_(dst)
                                        conversion = Q_(conversion).to(to_unit)
                                        change2 = conversion.magnitude
                                        converted_data.append([rec[0],str(change2)])
                                    conversion_uom = to_unit
                                elif request.get_filter("operation")['type'] == 'sub':
                                    if qty == '':
                                        qty = 0
                                    for rec in recs:
                                        operation = """%s*%sopr%s*%s"""%(rec[1], from_unit, qty, unit)
                                        src, dst = operation.split('opr')
                                        conversion = Q_(src)-Q_(dst)
                                        conversion = Q_(conversion).to(to_unit)
                                        change2 = conversion.magnitude
                                        converted_data.append([rec[0],str(change2)])
                                    conversion_uom = to_unit
                                elif request.get_filter("operation")['type'] == 'mul':
                                    if qty == '':
                                        qty = 1
                                    conversion_uom = """%s*%s"""%(to_unit, unit)
                                    for rec in recs:
                                        operation = """%s*%sopr%s*%s"""%(rec[1], from_unit, qty, unit)
                                        src, dst = operation.split('opr')
                                        conversion = Q_(src)*Q_(dst)
                                        conversion = Q_(conversion).to(conversion_uom)
                                        change2 = conversion.magnitude
                                        converted_data.append([rec[0],str(change2)])
                                elif request.get_filter("operation")['type'] == 'div':
                                    if qty == '':
                                        qty = 1
                                    conversion_uom = """%s/%s"""%(to_unit,unit)
                                    for rec in recs:
                                        operation = """%s*%sopr%s*%s"""%(rec[1], from_unit, qty, unit)
                                        src, dst = operation.split('opr')
                                        conversion = Q_(src)/Q_(dst)
                                        conversion = Q_(conversion).to(conversion_uom)
                                        change2 = conversion.magnitude
                                        converted_data.append([rec[0],str(change2)])
                    else:
                        if 'qty' in request.get_filter("operation"):
                            qty = request.get_filter("operation")['qty']
                            if 'type' in request.get_filter("operation"):
                                if request.get_filter("operation")['type'] == 'add':
                                    if qty == '':
                                        qty = 0
                                    for rec in recs:
                                        operation = """%s*%sopr%s*%s"""%(rec[1], from_unit, qty, from_unit)
                                        src, dst = operation.split('opr')
                                        if(from_unit == 'degC'):
                                            conversion = Q_(src)+Q_(dst).to('delta_degC')
                                        else:
                                            conversion = Q_(src)+Q_(dst)
                                        conversion = Q_(conversion).to(to_unit)
                                        change2 = conversion.magnitude
                                        converted_data.append([rec[0],str(change2)])
                                    conversion_uom = to_unit
                                elif request.get_filter("operation")['type'] == 'sub':
                                    if qty == '':
                                        qty = 0
                                    for rec in recs:
                                        operation = """%s*%sopr%s*%s"""%(rec[1], from_unit, qty, from_unit)
                                        src, dst = operation.split('opr')
                                        conversion = Q_(src)-Q_(dst)
                                        conversion = Q_(conversion).to(to_unit)
                                        change2 = conversion.magnitude
                                        converted_data.append([rec[0],str(change2)])
                                    conversion_uom = to_unit
                                elif request.get_filter("operation")['type'] == 'mul':
                                    if qty == '':
                                        qty = 1
                                    conversion_uom = """%s*%s"""%(to_unit,from_unit)
                                    for rec in recs:
                                        operation = """%s*%sopr%s*%s"""%(rec[1], from_unit, qty, from_unit)
                                        src, dst = operation.split('opr')
                                        conversion = Q_(src)*Q_(dst)
                                        conversion = Q_(conversion).to(conversion_uom)
                                        change2 = conversion.magnitude
                                        converted_data.append([rec[0],str(change2)])
                                elif request.get_filter("operation")['type'] == 'div':
                                    if qty == '':
                                        qty = 1
                                    conversion_uom = """%s/%s"""%(to_unit,from_unit)
                                    for rec in recs:
                                        operation = """%s*%sopr%s*%s"""%(rec[1], from_unit, qty, from_unit)
                                        src, dst = operation.split('opr')
                                        conversion = Q_(src)/Q_(dst)
                                        conversion = Q_(conversion).to(conversion_uom)
                                        change2 = conversion.magnitude
                                        converted_data.append([rec[0],str(change2)])
                else:
                    for rec in recs:
                        operation = """%s*%sopr%s"""%(rec[1], from_unit, to_unit)
                        src, dst = operation.split('opr')
                        conversion = Q_(src).to(dst)
                        change2 = conversion.magnitude
                        converted_data.append([rec[0],str(change2)])
                    conversion_uom = to_unit
            else:
                if request.get_filter("operation") is not None:
                    if 'unit' in request.get_filter("operation"):
                        unit = yield from self.findLookUp(request.get_filter("operation")['unit'])
                        if 'qty' in request.get_filter("operation"):
                            qty = request.get_filter("operation")['qty']
                            if 'type' in request.get_filter("operation"):
                                if request.get_filter("operation")['type'] == 'add':
                                    if qty == '':
                                        qty = 0
                                    for rec in recs:
                                        operation = """%s*%sopr%s*%s"""%(rec[1], from_unit, qty, unit)
                                        src, dst = operation.split('opr')
                                        if(from_unit == 'degC' and unit == 'degC'):
                                            conversion = Q_(src)+Q_(dst).to('delta_degC')
                                        elif(from_unit == 'degC'):
                                            conversion = Q_(src)+Q_(dst).to('delta_degC')
                                        elif(unit == 'degC'):
                                            conversion = Q_(src)+Q_(dst).to('delta_degC')
                                        else:
                                            conversion = Q_(src)+Q_(dst)
                                        change2 = conversion.magnitude
                                        converted_data.append([rec[0],str(change2)])
                                    conversion_uom = from_unit
                                elif request.get_filter("operation")['type'] == 'sub':
                                    if qty == '':
                                        qty = 0
                                    for rec in recs:
                                        operation = """%s*%sopr%s*%s"""%(rec[1], from_unit, qty, unit)
                                        src, dst = operation.split('opr')
                                        conversion = Q_(src)-Q_(dst)
                                        change2 = conversion.magnitude
                                        converted_data.append([rec[0],str(change2)])
                                    conversion_uom = from_unit
                                elif request.get_filter("operation")['type'] == 'mul':
                                    if qty == '':
                                        qty = 1
                                    conversion_uom = """%s*%s"""%(from_unit,unit)
                                    for rec in recs:
                                        operation = """%s*%sopr%s*%s"""%(rec[1], from_unit, qty, unit)
                                        src, dst = operation.split('opr')
                                        conversion = Q_(src)*Q_(dst)
                                        change2 = conversion.magnitude
                                        converted_data.append([rec[0],str(change2)])
                                elif request.get_filter("operation")['type'] == 'div':
                                    if qty == '':
                                        qty = 1
                                    conversion_uom = """%s/%s"""%(from_unit, unit)
                                    for rec in recs:
                                        operation = """%s*%sopr%s*%s"""%(rec[1], from_unit, qty, unit)
                                        src, dst = operation.split('opr')
                                        conversion = Q_(src)/Q_(dst)
                                        change2 = conversion.magnitude
                                        converted_data.append([rec[0], str(change2)])
                    else:
                        if 'qty' in request.get_filter("operation"):
                            qty = request.get_filter("operation")['qty']
                            if 'type' in request.get_filter("operation"):
                                if request.get_filter("operation")['type'] == 'add':
                                    if qty == '':
                                        qty = 0
                                    for rec in recs:
                                        operation = """%s*%sopr%s*%s"""%(rec[1], from_unit, qty, from_unit)
                                        src, dst = operation.split('opr')
                                        if(from_unit == 'degC'):
                                            conversion = Q_(src)+Q_(dst).to('delta_degC')
                                        else:
                                            conversion = Q_(src)+Q_(dst)
                                        change2 = conversion.magnitude
                                        converted_data.append([rec[0], str(change2)])
                                    conversion_uom = from_unit
                                elif request.get_filter("operation")['type'] == 'sub':
                                    if qty == '':
                                        qty = 0
                                    for rec in recs:
                                        operation = """%s*%sopr%s*%s"""%(rec[1], from_unit, qty, from_unit)
                                        src, dst = operation.split('opr')
                                        conversion = Q_(src)-Q_(dst)
                                        change2 = conversion.magnitude
                                        converted_data.append([rec[0], str(change2)])
                                    conversion_uom = from_unit
                                elif request.get_filter("operation")['type'] == 'mul':
                                    if qty == '':
                                        qty = 1
                                    conversion_uom = """%s*%s"""%(from_unit,from_unit)
                                    for rec in recs:
                                        operation = """%s*%sopr%s*%s"""%(rec[1], from_unit, qty, from_unit)
                                        src, dst = operation.split('opr')
                                        conversion = Q_(src)*Q_(dst)
                                        change2 = conversion.magnitude
                                        converted_data.append([rec[0], str(change2)])
                                elif request.get_filter("operation")['type'] == 'div':
                                    if qty == '':
                                        qty = 1
                                    conversion_uom = """%s/%s"""%(from_unit, from_unit)
                                    for rec in recs:
                                        operation = """%s*%sopr%s*%s"""%(rec[1], from_unit, qty, from_unit)
                                        src, dst = operation.split('opr')
                                        conversion = Q_(src)/Q_(dst)
                                        change2 = conversion.magnitude
                                        converted_data.append([rec[0], str(change2)])
                            # for rec in recs:
                            #     # change=rec[1]*ureg.kilometers
                            #     # conversion=change.to(ureg.meter)
                            #     # change2=conversion.magnitude
                            #     change=str(rec[1])+"*"+from_unit+"to"+to_unit
                            #     # change=Q_(str(rec[1]), ureg.degC).to(ureg.kelvin)
                            #     # change=str(rec[1])+"*degC"+"to"+"degF"
                            #     # change=str(rec[1])+"*ureg.degC"+"to"+"ureg.degF"
                            #     # change=rec[1]*ureg.degC
                            #     # change=str(rec[1])+"* kelvin to degF"
                            #     src, dst = change.split('to')
                            #     conversion=Q_(src).to(dst)
                            #     # home = Q_(rec[1], ureg.degC)
                            #     # conversion=home.to('degF')
                            #     # conversion=Q_(rec[1], ureg.degC).to(ureg.kelvin).magnitude
                            #     change2=conversion.magnitude
                            #     # print(change2)
                            #     # print(conversion)
                            #     converted_data.append([rec[0],str(change2)])
                else:
                    converted_data = request['observations']
                    conversion_uom = to_unit
            headers.append({
                "type": request["headers"][1]["type"],
                "name": request["headers"][1]["name"],
                "definition": request["headers"][1]["definition"],
                "offering": request["headers"][1]["offering"],
                "uom": conversion_uom
            })
            request['response'] = Response(
                json_source=Response.get_template({
                    "data": converted_data,
                    "headers": headers
                })
            )
            yield from self.__download_file(request, converted_data, headers)
        else:
            request['response'] = Response(
                json_source=Response.get_template({
                    "message": "In Pint Unit Conversion Valid only for array responseFormat",
                })
            )

    @asyncio.coroutine
    def __download_file(self, request, data, headers=None):
        if request.get_filter("download_file") is not None:
            if 'file_name' in request.get_filter("download_file"):
                file_name=request.get_filter("download_file")['file_name']
            else:
                file_name=request.get_filter("offerings")

            if 'location' in request.get_filter("download_file"):
                download_location=request.get_filter("download_file")['location']
            else:
                download_location='istsos/plugins/unit_con_pint/download_file/'

            file_detail = """%s%s.csv""" % (download_location, file_name)
            f = csv.writer(open(file_detail, "w"))
            if headers is not None:
                f.writerow(headers)
            for x in data:
                f.writerow(x)
            debug_detail = """%s.csv download location is %s""" % (file_name, download_location)
            istsos.debug(debug_detail)