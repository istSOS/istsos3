# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import istsos
import json
import csv
from istsos import setting
from istsos.actions.retrievers.observations import Observations
from istsos.entity.observation import Observation
from istsos.entity.observedProperty import (
    ObservedProperty, ObservedPropertyComplex)
from istsos.plugins.unit_con_post.lookUpTable import LookUpTable


class Observations(Observations, LookUpTable):
    """Query an SOS to retrieve observation data structured according to the
O&M specification.

istSOS supports this filters:

temporalFilter:
- during: om:phenomenonTime,
          2012-11-19T14:00:00+01:00/2012-11-19T14:15:00+01:00
- equals: om:phenomenonTime,
          2012-11-19T14:00:00.000+01:00
    """

    @asyncio.coroutine
    def process(self, request):
        """Depending on the selected procedures call its specific retriever to
        query the relatives observed data.

        :param dict state: must contain an object with the queried procedures
        """

        if 'offerings' not in request:
            # A request can also lead to an empty response
            return

        # @todo check if this helps
        if False:  # len(request['offerings']) > 1:
            istsos.debug("Running retrieval in parallel")
            funcs = [
                self.__get_data(
                    offering, request
                ) for offering in request['offerings']
            ]
            yield from asyncio.gather(*funcs)

        else:
            istsos.debug("Running retrieval sequentially")
            if request.get_filter(
                    "responseFormat") in setting._responseFormat['vega']:
                yield from self.__get_kvp(
                    request['offerings'], request)
            elif request.get_filter(
                    "responseFormat") in setting._responseFormat['array']:
                yield from self.__get_array(
                    request['offerings'], request)
            elif request.get_filter(
                    "responseFormat") in setting._responseFormat['array2']:
                yield from self.__get_array_2(
                    request['offerings'], request)
            else:
                for offering in request['offerings']:
                    yield from self.__get_data(offering, request)
        # istsos.debug(request['observations'])

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
                download_location='istsos/plugins/unit_con_post/download_file/'

            file_detail = """%s%s.csv""" % (download_location, file_name)
            f = csv.writer(open(file_detail, "w"))
            if headers is not None:
                f.writerow(headers)
            for x in data:
                f.writerow(x)
            debug_detail = """%s.csv download location is %s""" % (file_name, download_location)
            istsos.debug(debug_detail)

    @asyncio.coroutine
    def __download_csv_from_json(self, request, data, headers=None):
        if request.get_filter("download_file") is not None:
            if 'file_name' in request.get_filter("download_file"):
                file_name=request.get_filter("download_file")['file_name']
            else:
                file_name=request.get_filter("offerings")

            if 'location' in request.get_filter("download_file"):
                download_location=request.get_filter("download_file")['location']
            else:
                download_location='istsos/plugins/unit_con_post/download_file/'

            file_detail = """%s%s.csv""" % (download_location, file_name)
            csvwriter = csv.writer(open(file_detail, "w"))
            if headers is not None:
                csvwriter.writerow(headers)
            count = 0
            for obj in data:
                if count == 0:
                    header = obj.keys()
                    csvwriter.writerow(header)
                    count += 1
                csvwriter.writerow(obj.values())

            debug_detail = """%s.csv download location is %s""" % (file_name, download_location)
            istsos.debug(debug_detail)

    @asyncio.coroutine
    def __download_json(self, request, data):
        if request.get_filter("download_file") is not None:
            if 'file_name' in request.get_filter("download_file"):
                file_name=request.get_filter("download_file")['file_name']
            else:
                file_name=request.get_filter("offerings")

            if 'location' in request.get_filter("download_file"):
                download_location=request.get_filter("download_file")['location']
            else:
                download_location='istsos/plugins/unit_con_post/download_file/'

            file_detail = """%s%s.json""" % (download_location, file_name)
            with open(file_detail, 'w') as outfile:
                json.dump(data, outfile)
            debug_detail = """%s.json download location is %s""" % (file_name, download_location)
            istsos.debug(debug_detail)


    @asyncio.coroutine
    def __get_array_2(self, offerings, request):

        dbmanager = yield from self.init_connection()
        cur = dbmanager.cur
        op_filter = request.get_filter('observedProperties')
        tables = {}
        columns = []
        from_uom=''
        conversion_uom=''
        headers = [{
            "type": "datetime",
            "name": "Phenomenon Time",
            "column": "e"
        }]

        for offering in request['offerings']:
            tName = "_%s" % offering['name'].lower()
            if offering.is_complex():
                tables[tName] = []
                for op in offering['observable_properties']:
                    if op['type'] == setting._COMPLEX_OBSERVATION:
                        continue
                    else:
                        # observedProperty filters are applied here excluding
                        # the observed properties columns from the query
                        if op_filter is not None and (
                                op['definition'] not in op_filter):
                            continue
                        columns.append(op['column'])
                        # columns_qi.append('%s_qi' % op['column'])
                        tables[tName].append(op['column'])
                        from_uom=op['uom']
                        headers.append({
                            "type": "number",
                            "name": op['name'],
                            "definition": op['definition'],
                            "offering": offering['name'],
                            "initial_uom": op['uom'],
                            "column": op['column']
                        })
            elif offering.is_array():
                raise Exception("Not implemented yet")
            else:
                tables[tName] = []
                for op in offering['observable_properties']:
                    # observedProperty filters are applied here excluding
                    # the observed properties columns from the query
                    if op_filter is not None and (
                            op['definition'] not in op_filter):
                        continue
                    columns.append(op['column'])
                    # columns_qi.append('%s_qi' % op['column'])
                    tables[tName].append(op['column'])
                    from_uom=yield from self.findLookUp(op['uom'])
                    headers.append({
                        "type": "number",
                        "name": op['name'],
                        "definition": op['definition'],
                        "offering": offering['name'],
                        "initial_uom": op['uom'],
                        "column": op['column']
                    })

        unions = []
        unionSelect = []
        jsonKeys = [
            "array_agg(to_char(end_time, 'YYYY-MM-DD\"T\"HH24:MI:SSZ'))"
        ]
        unionColumns = []
        for idx in range(0, len(columns)):
            unionSelect.append(
                "SUM(c%s) as c%s" % (idx, idx)
            )
            unionColumns.append(
                "NULL::double precision as c%s" % (idx)
            )
            jsonKeys.append(
                "array_agg(c%s)" % (idx))

        unionSelect = ", ".join(unionSelect)

        temporal = []
        where = []
        params = []
        if request.get_filters() is not None:
            keys = list(request.get_filters())
            for key in keys:
                fltr = request.get_filters()[key]
                if key == 'temporal':
                    if fltr['fes'] == 'during':
                        temporal.append("""
                            begin_time >= %s::timestamp with time zone
                        AND
                            end_time <= %s::timestamp with time zone
                        """)
                        params.extend(fltr['period'])

                    elif fltr['fes'] == 'equals':
                        temporal.append("""
                            begin_time = end_time
                        AND
                            begin_time = %s::timestamp with time zone
                        """)
                        params.append(fltr['instant'])

                    where.append(
                        "(%s)" % (' OR '.join(temporal))
                    )

        for table in tables.keys():
            off_cols = tables[table]
            cols = unionColumns.copy()
            for col in off_cols:
                conversion_query = ''
                if request.get_filter("in_unit") is not None:
                    to_unit = yield from self.findLookUp(request.get_filter("in_unit"))
                    if request.get_filter("operation") is not None:
                        if 'unit' in request.get_filter("operation"):
                            unit = yield from self.findLookUp(request.get_filter("operation")['unit'])
                            if 'qty' in request.get_filter("operation"):
                                qty = request.get_filter("operation")['qty']
                                if 'type' in request.get_filter("operation"):
                                    if request.get_filter("operation")['type'] == 'add':
                                        if qty == '':
                                            qty = 0
                                        conversion_query = """(%s::text||'%s')::unit + ('%s'::text||'%s')::unit@@'%s' """%(col, from_uom, qty, unit, to_unit)
                                        conversion_uom = to_unit
                                    elif request.get_filter("operation")['type'] == 'sub':
                                        if qty == '':
                                            qty = 0
                                        conversion_query = """(%s::text||'%s')::unit - ('%s'::text||'%s')::unit@@'%s' """%(col, from_uom, qty, unit, to_unit)
                                        conversion_uom = to_unit
                                    elif request.get_filter("operation")['type'] == 'mul':
                                        if qty == '':
                                            qty = 1
                                        conversion_query = """(%s::text||'%s')::unit * '%s %s' ::unit@@'%s*%s' """%(col, from_uom, qty, unit, to_unit, unit)
                                        conversion_uom = """ %s*%s """%(to_unit,unit)
                                    elif request.get_filter("operation")['type'] == 'div':
                                        if qty == '':
                                            qty = 1
                                        conversion_query = """(%s::text||'%s')::unit / '%s %s' ::unit@@'%s/%s' """%(col, from_uom, qty, unit, to_unit, unit)
                                        conversion_uom = """ %s/%s """%(to_unit,unit)
                        else:
                            if 'qty' in request.get_filter("operation"):
                                qty = request.get_filter("operation")['qty']
                                if 'type' in request.get_filter("operation"):
                                    if request.get_filter("operation")['type'] == 'add':
                                        if qty == '':
                                            qty = 0
                                        conversion_query = """(%s::text||'%s')::unit + ('%s'::text||'%s')::unit@@'%s' """%(col, from_uom, qty, from_uom, to_unit)
                                        conversion_uom = to_unit
                                    elif request.get_filter("operation")['type'] == 'sub':
                                        if qty == '':
                                            qty = 0
                                        conversion_query = """(%s::text||'%s')::unit - ('%s'::text||'%s')::unit@@'%s' """%(col, from_uom, qty, from_uom, to_unit)
                                        conversion_uom = to_unit
                                    elif request.get_filter("operation")['type'] == 'mul':
                                        if qty == '':
                                            qty = 1
                                        conversion_query = """(%s::text||'%s')::unit * '%s %s' ::unit@@'%s*%s' """%(col, from_uom, qty, from_uom, to_unit, to_unit)
                                        conversion_uom = """ %s*%s """%(to_unit,to_unit)
                                    elif request.get_filter("operation")['type'] == 'div':
                                        if qty == '':
                                            qty = 1
                                        conversion_query = """(%s::text||'%s')::unit / '%s %s' ::unit@@'%s/%s' """%(col, from_uom, qty, from_uom, to_unit, to_unit)
                                        conversion_uom = """ %s/%s """%(to_unit,to_unit)
                    else:
                        conversion_query = """(%s::text||'%s')::unit@@'%s' """%(col, from_uom, to_unit)
                        conversion_uom = to_unit
                    cols[
                        columns.index(col)
                    ] = unionColumns[columns.index(col)].replace(
                        "NULL::double precision",
                        conversion_query
                    )
                elif request.get_filter("operation") is not None:
                    if 'unit' in request.get_filter("operation"):
                        unit = yield from self.findLookUp(request.get_filter("operation")['unit'])
                        if 'qty' in request.get_filter("operation"):
                            qty = request.get_filter("operation")['qty']
                            if 'type' in request.get_filter("operation"):
                                if request.get_filter("operation")['type'] == 'add':
                                    if qty == '':
                                        qty = 0
                                    conversion_query = """(%s::text||'%s')::unit + ('%s'::text||'%s')::unit@@'%s' """%(col, from_uom, qty, unit, from_uom)
                                    conversion_uom = from_uom
                                elif request.get_filter("operation")['type'] == 'sub':
                                    if qty == '':
                                        qty = 0
                                    conversion_query = """(%s::text||'%s')::unit - ('%s'::text||'%s')::unit@@'%s' """%(col, from_uom, qty, unit, from_uom)
                                    conversion_uom = from_uom
                                elif request.get_filter("operation")['type'] == 'mul':
                                    if qty == '':
                                        qty = 1
                                    conversion_query = """(%s::text||'%s')::unit * '%s %s' ::unit@@'%s*%s' """%(col, from_uom, qty, unit, from_uom, unit)
                                    conversion_uom = """ %s*%s """%(from_uom,unit)
                                elif request.get_filter("operation")['type'] == 'div':
                                    if qty == '':
                                        qty = 1
                                    conversion_query = """(%s::text||'%s')::unit / '%s %s' ::unit@@'%s/%s' """%(col, from_uom, qty, unit, from_uom, unit)
                                    conversion_uom = """ %s/%s """%(from_uom,unit)
                    else:
                        if 'qty' in request.get_filter("operation"):
                            qty = request.get_filter("operation")['qty']
                            if 'type' in request.get_filter("operation"):
                                if request.get_filter("operation")['type'] == 'add':
                                    if qty == '':
                                        qty = 0
                                    conversion_query = """(%s::text||'%s')::unit + ('%s'::text||'%s')::unit@@'%s' """%(col, from_uom, qty, from_uom, from_uom)
                                    conversion_uom = from_uom
                                elif request.get_filter("operation")['type'] == 'sub':
                                    if qty == '':
                                        qty = 0
                                    conversion_query = """(%s::text||'%s')::unit - ('%s'::text||'%s')::unit@@'%s' """%(col, from_uom, qty, from_uom, from_uom)
                                    conversion_uom = from_uom
                                elif request.get_filter("operation")['type'] == 'mul':
                                    if qty == '':
                                        qty = 1
                                    conversion_query = """(%s::text||'%s')::unit * '%s %s' ::unit@@'%s*%s' """%(col, from_uom, qty, from_uom, from_uom, from_uom)
                                    conversion_uom = """ %s*%s """%(from_uom,from_uom)
                                elif request.get_filter("operation")['type'] == 'div':
                                    if qty == '':
                                        qty = 1
                                    conversion_query = """(%s::text||'%s')::unit / '%s %s' ::unit@@'%s/%s' """%(col, from_uom, qty, from_uom, from_uom, from_uom)
                                    conversion_uom = """ %s/%s """%(from_uom,from_uom)

                    cols[
                        columns.index(col)
                    ] = unionColumns[columns.index(col)].replace(
                        "NULL::double precision",
                        conversion_query
                    )
                else:
                    cols[
                        columns.index(col)
                    ] = unionColumns[columns.index(col)].replace(
                        "NULL::double precision",
                        col
                    )

            uSql = """
                SELECT
                    end_time, %s
                FROM
                    data.%s
            """ % (
                ", ".join(cols), table
            )

            if len(where) > 0:
                uSql += "WHERE %s" % (
                    'AND'.join(where)
                )
            unions.append("(%s)" % uSql)

        jsonSql = """
            SELECT %s
            FROM
        """ % (
            ", ".join(jsonKeys),
        )

        sql = """
            SET enable_seqscan=false;
            SET SESSION TIME ZONE '+00:00';
            %s
            (
                SELECT end_time, %s
                FROM (
                    %s
                ) a
                GROUP BY end_time
                ORDER BY end_time
            ) b
        """ % (
            jsonSql,
            unionSelect,
            " UNION ".join(unions)
        )

        istsos.debug(
            (
                yield from cur.mogrify(sql, tuple(params*len(unions)))
            ).decode("utf-8")
        )

        sqlExtensionUnit="""CREATE EXTENSION IF NOT EXISTS unit;"""
        yield from cur.execute(sqlExtensionUnit)

        yield from cur.execute(sql, tuple(params*len(unions)))
        rec = yield from cur.fetchone()

        request['observations'] = {}
        for idx in range(0, len(headers)):
            header = headers[idx]
            request['observations'][header['column']] = rec[idx]

        headers.append({
            "type": "number",
            "name": op['name'],
            "definition": op['definition'],
            "offering": offering['name'],
            "final_uom": conversion_uom,
            "column": op['column']
        })

        yield from self.__download_file(request, rec, headers)

        request['headers'] = headers
        istsos.debug("Data is fetched!")

    @asyncio.coroutine
    def __get_array(self, offerings, request):
        conversion_uom=''
        from_uom=''
        dbmanager = yield from self.init_connection()
        cur = dbmanager.cur
        op_filter = request.get_filter('observedProperties')
        tables = {}
        columns = []
        headers = [{
            "type": "time",
            "name": "Phenomenon Time",
            "column": "datetime"
        }]

        for offering in request['offerings']:
            tName = "_%s" % offering['name'].lower()
            if offering.is_complex():
                tables[tName] = []
                for op in offering['observable_properties']:
                    if op['type'] == setting._COMPLEX_OBSERVATION:
                        continue
                    else:
                        # observedProperty filters are applied here excluding
                        # the observed properties columns from the query
                        if op_filter is not None and (
                                op['definition'] not in op_filter):
                            continue
                        columns.append(op['column'])
                        # columns_qi.append('%s_qi' % op['column'])
                        tables[tName].append(op['column'])
                        from_uom=yield from self.findLookUp(op['uom'])
                        headers.append({
                            "type": "number",
                            "name": op['name'],
                            "definition": op['definition'],
                            "offering": offering['name'],
                            "uom": op['uom']
                        })

            elif offering.is_array():
                raise Exception("Not implemented yet")
            else:
                tables[tName] = []
                for op in offering['observable_properties']:
                    # observedProperty filters are applied here excluding
                    # the observed properties columns from the query
                    if op_filter is not None and (
                            op['definition'] not in op_filter):
                        continue
                    columns.append(op['column'])
                    # columns_qi.append('%s_qi' % op['column'])
                    tables[tName].append(op['column'])
                    from_uom=op['uom']
                    headers.append({
                        "type": "number",
                        "name": op['name'],
                        "definition": op['definition'],
                        "offering": offering['name'],
                        "uom": op['uom']
                    })
        unions = []
        unionSelect = []
        jsonKeys = []
        unionColumns = []
        for idx in range(0, len(columns)):
            unionSelect.append(
                "SUM(c%s)::text as c%s" % (idx, idx)
            )
            unionColumns.append(
                "NULL::double precision as c%s" % (idx)
            )
            jsonKeys.append("COALESCE(c%s, 'null')" % (idx))

        unionSelect = ", ".join(unionSelect)

        temporal = []
        where = []
        params = []
        if request.get_filters() is not None:
            keys = list(request.get_filters())
            for key in keys:
                fltr = request.get_filters()[key]
                if key == 'temporal':
                    if fltr['fes'] == 'during':
                        temporal.append("""
                            begin_time >= %s::timestamp with time zone
                        AND
                            end_time <= %s::timestamp with time zone
                        """)
                        params.extend(fltr['period'])

                    elif fltr['fes'] == 'equals':
                        temporal.append("""
                            begin_time = end_time
                        AND
                            begin_time = %s::timestamp with time zone
                        """)
                        params.append(fltr['instant'])

                    where.append(
                        "(%s)" % (' OR '.join(temporal))
                    )

        for table in tables.keys():
            off_cols = tables[table]
            cols = unionColumns.copy()
            for col in off_cols:
                conversion_query = ''
                if request.get_filter("in_unit") is not None:
                    to_unit = yield from self.findLookUp(request.get_filter("in_unit"))
                    if request.get_filter("operation") is not None:
                        if 'unit' in request.get_filter("operation"):
                            unit = yield from self.findLookUp(request.get_filter("operation")['unit'])
                            if 'qty' in request.get_filter("operation"):
                                qty = request.get_filter("operation")['qty']
                                if 'type' in request.get_filter("operation"):
                                    if request.get_filter("operation")['type'] == 'add':
                                        if qty == '':
                                            qty = 0
                                        conversion_query = """(%s::text||'%s')::unit + ('%s'::text||'%s')::unit@@'%s' """%(col, from_uom, qty, unit, to_unit)
                                        conversion_uom = to_unit
                                    elif request.get_filter("operation")['type'] == 'sub':
                                        if qty == '':
                                            qty = 0
                                        conversion_query = """(%s::text||'%s')::unit - ('%s'::text||'%s')::unit@@'%s' """%(col, from_uom, qty, unit, to_unit)
                                        conversion_uom = to_unit
                                    elif request.get_filter("operation")['type'] == 'mul':
                                        if qty == '':
                                            qty = 1
                                        conversion_query = """(%s::text||'%s')::unit * '%s %s' ::unit@@'%s*%s' """%(col, from_uom, qty, unit, to_unit, unit)
                                        conversion_uom = """ %s*%s """%(to_unit,unit)
                                    elif request.get_filter("operation")['type'] == 'div':
                                        if qty == '':
                                            qty = 1
                                        conversion_query = """(%s::text||'%s')::unit / '%s %s' ::unit@@'%s/%s' """%(col, from_uom, qty, unit, to_unit, unit)
                                        conversion_uom = """ %s/%s """%(to_unit,unit)
                        else:
                            if 'qty' in request.get_filter("operation"):
                                qty = request.get_filter("operation")['qty']
                                if 'type' in request.get_filter("operation"):
                                    if request.get_filter("operation")['type'] == 'add':
                                        if qty == '':
                                            qty = 0
                                        conversion_query = """(%s::text||'%s')::unit + ('%s'::text||'%s')::unit@@'%s' """%(col, from_uom, qty, from_uom, to_unit)
                                        conversion_uom = to_unit
                                    elif request.get_filter("operation")['type'] == 'sub':
                                        if qty == '':
                                            qty = 0
                                        conversion_query = """(%s::text||'%s')::unit - ('%s'::text||'%s')::unit@@'%s' """%(col, from_uom, qty, from_uom, to_unit)
                                        conversion_uom = to_unit
                                    elif request.get_filter("operation")['type'] == 'mul':
                                        if qty == '':
                                            qty = 1
                                        conversion_query = """(%s::text||'%s')::unit * '%s %s' ::unit@@'%s*%s' """%(col, from_uom, qty, from_uom, to_unit, to_unit)
                                        conversion_uom = """ %s*%s """%(to_unit,to_unit)
                                    elif request.get_filter("operation")['type'] == 'div':
                                        if qty == '':
                                            qty = 1
                                        conversion_query = """(%s::text||'%s')::unit / '%s %s' ::unit@@'%s/%s' """%(col, from_uom, qty, from_uom, to_unit, to_unit)
                                        conversion_uom = """ %s/%s """%(to_unit,to_unit)
                    else:
                        conversion_query = """(%s::text||'%s')::unit@@'%s' """%(col, from_uom, to_unit)
                        conversion_uom = to_unit
                    cols[
                        columns.index(col)
                    ] = unionColumns[columns.index(col)].replace(
                        "NULL::double precision",
                        conversion_query
                    )
                elif request.get_filter("operation") is not None:
                    if 'unit' in request.get_filter("operation"):
                        unit = yield from self.findLookUp(request.get_filter("operation")['unit'])
                        if 'qty' in request.get_filter("operation"):
                            qty = request.get_filter("operation")['qty']
                            if 'type' in request.get_filter("operation"):
                                if request.get_filter("operation")['type'] == 'add':
                                    if qty == '':
                                        qty = 0
                                    conversion_query = """(%s::text||'%s')::unit + ('%s'::text||'%s')::unit@@'%s' """%(col, from_uom, qty, unit, from_uom)
                                    conversion_uom = from_uom
                                elif request.get_filter("operation")['type'] == 'sub':
                                    if qty == '':
                                        qty = 0
                                    conversion_query = """(%s::text||'%s')::unit - ('%s'::text||'%s')::unit@@'%s' """%(col, from_uom, qty, unit, from_uom)
                                    conversion_uom = from_uom
                                elif request.get_filter("operation")['type'] == 'mul':
                                    if qty == '':
                                        qty = 1
                                    conversion_query = """(%s::text||'%s')::unit * '%s %s' ::unit@@'%s*%s' """%(col, from_uom, qty, unit, from_uom, unit)
                                    conversion_uom = """ %s*%s """%(from_uom,unit)
                                elif request.get_filter("operation")['type'] == 'div':
                                    if qty == '':
                                        qty = 1
                                    conversion_query = """(%s::text||'%s')::unit / '%s %s' ::unit@@'%s/%s' """%(col, from_uom, qty, unit, from_uom, unit)
                                    conversion_uom = """ %s/%s """%(from_uom,unit)
                    else:
                        if 'qty' in request.get_filter("operation"):
                            qty = request.get_filter("operation")['qty']
                            if 'type' in request.get_filter("operation"):
                                if request.get_filter("operation")['type'] == 'add':
                                    if qty == '':
                                        qty = 0
                                    conversion_query = """(%s::text||'%s')::unit + ('%s'::text||'%s')::unit@@'%s' """%(col, from_uom, qty, from_uom, from_uom)
                                    conversion_uom = from_uom
                                elif request.get_filter("operation")['type'] == 'sub':
                                    if qty == '':
                                        qty = 0
                                    conversion_query = """(%s::text||'%s')::unit - ('%s'::text||'%s')::unit@@'%s' """%(col, from_uom, qty, from_uom, from_uom)
                                    conversion_uom = from_uom
                                elif request.get_filter("operation")['type'] == 'mul':
                                    if qty == '':
                                        qty = 1
                                    conversion_query = """(%s::text||'%s')::unit * '%s %s' ::unit@@'%s*%s' """%(col, from_uom, qty, from_uom, from_uom, from_uom)
                                    conversion_uom = """ %s*%s """%(from_uom,from_uom)
                                elif request.get_filter("operation")['type'] == 'div':
                                    if qty == '':
                                        qty = 1
                                    conversion_query = """(%s::text||'%s')::unit / '%s %s' ::unit@@'%s/%s' """%(col, from_uom, qty, from_uom, from_uom, from_uom)
                                    conversion_uom = """ %s/%s """%(from_uom,from_uom)

                    cols[
                        columns.index(col)
                    ] = unionColumns[columns.index(col)].replace(
                        "NULL::double precision",
                        conversion_query
                    )
                else:
                    cols[
                        columns.index(col)
                    ] = unionColumns[columns.index(col)].replace(
                        "NULL::double precision",
                        col
                    )

            uSql = """
                SELECT
                    end_time, %s
                FROM
                    data.%s
            """ % (
                ", ".join(cols), table
            )

            if len(where) > 0:
                uSql += "WHERE %s" % (
                    'AND'.join(where)
                )
            unions.append("(%s)" % uSql)

        jsonSql = """
            SELECT array_agg(
                ARRAY[
                    to_char(end_time, 'YYYY-MM-DD"T"HH24:MI:SSZ'),
                    %s
                ]
            )
            FROM
        """ % (
            ", ".join(jsonKeys),
        )

        sql = """
            SET enable_seqscan=false;
            SET SESSION TIME ZONE '+00:00';
            %s
            (
                SELECT end_time, %s
                FROM (
                    %s
                ) a
                GROUP BY end_time
                ORDER BY end_time
            ) b
        """ % (
            jsonSql,
            unionSelect,
            " UNION ".join(unions)
        )

        istsos.debug(
            (
                yield from cur.mogrify(sql, tuple(params*len(unions)))
            ).decode("utf-8")
        )        
        sqlExtensionUnit="""CREATE EXTENSION IF NOT EXISTS unit;"""
        yield from cur.execute(sqlExtensionUnit)
        yield from cur.execute(sql, tuple(params*len(unions)))
        rec = yield from cur.fetchone()

        headers.append({
            "type": "number",
            "name": op['name'],
            "definition": op['definition'],
            "offering": offering['name'],
            "final_uom": conversion_uom,
            "column": op['column']
        })

        yield from self.__download_file(request, rec[0], headers)

        request['observations'] = rec[0]
        request['headers'] = headers
        # recs = yield from cur.fetchall()
        istsos.debug("Data is fetched!")

    @asyncio.coroutine
    def __get_kvp(self, offerings, request):

        dbmanager = yield from self.init_connection()
        cur = dbmanager.cur
        op_filter = request.get_filter('observedProperties')
        tables = {}
        columns = []
        from_uom=''
        conversion_uom=''
        headers = [{
            "type": "time",
            "name": "Phenomenon Time",
            "column": "datetime"
        }]
        for offering in request['offerings']:
            tName = "_%s" % offering['name'].lower()
            if offering.is_complex():
                tables[tName] = []
                for op in offering['observable_properties']:
                    if op['type'] == setting._COMPLEX_OBSERVATION:
                        continue
                    else:
                        # observedProperty filters are applied here excluding
                        # the observed properties columns from the query
                        if op_filter is not None and (
                                op['definition'] not in op_filter):
                            continue
                        columns.append(op['column'])
                        # columns_qi.append('%s_qi' % op['column'])
                        tables[tName].append(op['column'])
                        from_uom=op['uom']

            elif offering.is_array():
                raise Exception("Not implemented yet")
            else:
                tables[tName] = []
                for op in offering['observable_properties']:
                    # observedProperty filters are applied here excluding
                    # the observed properties columns from the query
                    if op_filter is not None and (
                            op['definition'] not in op_filter):
                        continue
                    columns.append(op['column'])
                    # columns_qi.append('%s_qi' % op['column'])
                    tables[tName].append(op['column'])
                    from_uom=op['uom']

        unions = []
        unionSelect = []
        jsonKeys = []
        unionColumns = []
        for idx in range(0, len(columns)):
            unionSelect.append(
                "SUM(c%s)::text as c%s" % (idx, idx)
            )
            unionColumns.append(
                "NULL::double precision as c%s" % (idx)
            )
            jsonKeys.append("""
                "%s": ' || COALESCE(c%s, 'null') || '
            """ % (
                columns[idx],
                idx
            ))

        unionSelect = ", ".join(unionSelect)

        temporal = []
        where = []
        params = []
        if request.get_filters() is not None:
            keys = list(request.get_filters())
            for key in keys:
                fltr = request.get_filters()[key]
                if key == 'temporal':
                    if fltr['fes'] == 'during':
                        temporal.append("""
                            begin_time >= %s::timestamp with time zone
                        AND
                            end_time <= %s::timestamp with time zone
                        """)
                        params.extend(fltr['period'])

                    elif fltr['fes'] == 'equals':
                        temporal.append("""
                            begin_time = end_time
                        AND
                            begin_time = %s::timestamp with time zone
                        """)
                        params.append(fltr['instant'])

                    where.append(
                        "(%s)" % (' OR '.join(temporal))
                    )

        for table in tables.keys():
            off_cols = tables[table]
            cols = unionColumns.copy()
            for col in off_cols:
                conversion_query = ''
                if request.get_filter("in_unit") is not None:
                    to_unit = yield from self.findLookUp(request.get_filter("in_unit"))
                    if request.get_filter("operation") is not None:
                        if 'unit' in request.get_filter("operation"):
                            unit = yield from self.findLookUp(request.get_filter("operation")['unit'])
                            if 'qty' in request.get_filter("operation"):
                                qty = request.get_filter("operation")['qty']
                                if 'type' in request.get_filter("operation"):
                                    if request.get_filter("operation")['type'] == 'add':
                                        if qty == '':
                                            qty = 0
                                        conversion_query = """(%s::text||'%s')::unit + ('%s'::text||'%s')::unit@@'%s' """%(col, from_uom, qty, unit, to_unit)
                                        conversion_uom = to_unit
                                    elif request.get_filter("operation")['type'] == 'sub':
                                        if qty == '':
                                            qty = 0
                                        conversion_query = """(%s::text||'%s')::unit - ('%s'::text||'%s')::unit@@'%s' """%(col, from_uom, qty, unit, to_unit)
                                        conversion_uom = to_unit
                                    elif request.get_filter("operation")['type'] == 'mul':
                                        if qty == '':
                                            qty = 1
                                        conversion_query = """(%s::text||'%s')::unit * '%s %s' ::unit@@'%s*%s' """%(col, from_uom, qty, unit, to_unit, unit)
                                        conversion_uom = """ %s*%s """%(to_unit,unit)
                                    elif request.get_filter("operation")['type'] == 'div':
                                        if qty == '':
                                            qty = 1
                                        conversion_query = """(%s::text||'%s')::unit / '%s %s' ::unit@@'%s/%s' """%(col, from_uom, qty, unit, to_unit, unit)
                                        conversion_uom = """ %s/%s """%(to_unit,unit)
                        else:
                            if 'qty' in request.get_filter("operation"):
                                qty = request.get_filter("operation")['qty']
                                if 'type' in request.get_filter("operation"):
                                    if request.get_filter("operation")['type'] == 'add':
                                        if qty == '':
                                            qty = 0
                                        conversion_query = """(%s::text||'%s')::unit + ('%s'::text||'%s')::unit@@'%s' """%(col, from_uom, qty, from_uom, to_unit)
                                        conversion_uom = to_unit
                                    elif request.get_filter("operation")['type'] == 'sub':
                                        if qty == '':
                                            qty = 0
                                        conversion_query = """(%s::text||'%s')::unit - ('%s'::text||'%s')::unit@@'%s' """%(col, from_uom, qty, from_uom, to_unit)
                                        conversion_uom = to_unit
                                    elif request.get_filter("operation")['type'] == 'mul':
                                        if qty == '':
                                            qty = 1
                                        conversion_query = """(%s::text||'%s')::unit * '%s %s' ::unit@@'%s*%s' """%(col, from_uom, qty, from_uom, to_unit, to_unit)
                                        conversion_uom = """ %s*%s """%(to_unit,to_unit)
                                    elif request.get_filter("operation")['type'] == 'div':
                                        if qty == '':
                                            qty = 1
                                        conversion_query = """(%s::text||'%s')::unit / '%s %s' ::unit@@'%s/%s' """%(col, from_uom, qty, from_uom, to_unit, to_unit)
                                        conversion_uom = """ %s/%s """%(to_unit,to_unit)
                    else:
                        conversion_query = """(%s::text||'%s')::unit@@'%s' """%(col, from_uom, to_unit)
                        conversion_uom = to_unit
                    cols[
                        columns.index(col)
                    ] = unionColumns[columns.index(col)].replace(
                        "NULL::double precision",
                        conversion_query
                    )
                elif request.get_filter("operation") is not None:
                    if 'unit' in request.get_filter("operation"):
                        unit = yield from self.findLookUp(request.get_filter("operation")['unit'])
                        if 'qty' in request.get_filter("operation"):
                            qty = request.get_filter("operation")['qty']
                            if 'type' in request.get_filter("operation"):
                                if request.get_filter("operation")['type'] == 'add':
                                    if qty == '':
                                        qty = 0
                                    conversion_query = """(%s::text||'%s')::unit + ('%s'::text||'%s')::unit@@'%s' """%(col, from_uom, qty, unit, from_uom)
                                    conversion_uom = from_uom
                                elif request.get_filter("operation")['type'] == 'sub':
                                    if qty == '':
                                        qty = 0
                                    conversion_query = """(%s::text||'%s')::unit - ('%s'::text||'%s')::unit@@'%s' """%(col, from_uom, qty, unit, from_uom)
                                    conversion_uom = from_uom
                                elif request.get_filter("operation")['type'] == 'mul':
                                    if qty == '':
                                        qty = 1
                                    conversion_query = """(%s::text||'%s')::unit * '%s %s' ::unit@@'%s*%s' """%(col, from_uom, qty, unit, from_uom, unit)
                                    conversion_uom = """ %s*%s """%(from_uom,unit)
                                elif request.get_filter("operation")['type'] == 'div':
                                    if qty == '':
                                        qty = 1
                                    conversion_query = """(%s::text||'%s')::unit / '%s %s' ::unit@@'%s/%s' """%(col, from_uom, qty, unit, from_uom, unit)
                                    conversion_uom = """ %s/%s """%(from_uom,unit)
                    else:
                        if 'qty' in request.get_filter("operation"):
                            qty = request.get_filter("operation")['qty']
                            if 'type' in request.get_filter("operation"):
                                if request.get_filter("operation")['type'] == 'add':
                                    if qty == '':
                                        qty = 0
                                    conversion_query = """(%s::text||'%s')::unit + ('%s'::text||'%s')::unit@@'%s' """%(col, from_uom, qty, from_uom, from_uom)
                                    conversion_uom = from_uom
                                elif request.get_filter("operation")['type'] == 'sub':
                                    if qty == '':
                                        qty = 0
                                    conversion_query = """(%s::text||'%s')::unit - ('%s'::text||'%s')::unit@@'%s' """%(col, from_uom, qty, from_uom, from_uom)
                                    conversion_uom = from_uom
                                elif request.get_filter("operation")['type'] == 'mul':
                                    if qty == '':
                                        qty = 1
                                    conversion_query = """(%s::text||'%s')::unit * '%s %s' ::unit@@'%s*%s' """%(col, from_uom, qty, from_uom, from_uom, from_uom)
                                    conversion_uom = """ %s*%s """%(from_uom,from_uom)
                                elif request.get_filter("operation")['type'] == 'div':
                                    if qty == '':
                                        qty = 1
                                    conversion_query = """(%s::text||'%s')::unit / '%s %s' ::unit@@'%s/%s' """%(col, from_uom, qty, from_uom, from_uom, from_uom)
                                    conversion_uom = """ %s/%s """%(from_uom,from_uom)

                    cols[
                        columns.index(col)
                    ] = unionColumns[columns.index(col)].replace(
                        "NULL::double precision",
                        conversion_query
                    )
                else:
                    cols[
                        columns.index(col)
                    ] = unionColumns[columns.index(col)].replace(
                        "NULL::double precision",
                        col
                    )

            uSql = """
                SELECT
                    end_time, %s
                FROM
                    data.%s
            """ % (
                ", ".join(cols), table
            )

            if len(where) > 0:
                uSql += "WHERE %s" % (
                    'AND'.join(where)
                )
            unions.append("(%s)" % uSql)

        jsonSql = """
            SELECT array_to_json(
                array_agg(('{
                    "e": "' || to_char(
                        end_time, 'YYYY-MM-DD"T"HH24:MI:SSZ')
                        || '",
                    %s
                }')::json)
            )
            FROM
        """ % (
            ", ".join(jsonKeys),
        )

        sql = """
            SET enable_seqscan=false;
            SET SESSION TIME ZONE '+00:00';
            %s
            (
                SELECT end_time, %s
                FROM (
                    %s
                ) a
                GROUP BY end_time
                ORDER BY end_time
            ) b
        """ % (
            jsonSql,
            unionSelect,
            " UNION ".join(unions)
        )
        istsos.debug(
            (
                yield from cur.mogrify(sql, tuple(params*len(unions)))
            ).decode("utf-8")
        )
        sqlExtensionUnit="""CREATE EXTENSION IF NOT EXISTS unit;"""
        yield from cur.execute(sqlExtensionUnit)
        yield from cur.execute(sql, tuple(params*len(unions)))
        rec = yield from cur.fetchone()
        headers.append({
            "type": "number",
            "name": op['name'],
            "definition": op['definition'],
            "offering": offering['name'],
            "final_uom": conversion_uom,
            "column": op['column']
        })

        request['observations'] = rec[0]
        request['headers'] = headers

        yield from self.__download_csv_from_json(request, rec[0], headers)

        # recs = yield from cur.fetchall()
        istsos.debug("Data is fetched!")

    @asyncio.coroutine
    def __get_data(self, offering, request):

        dbmanager = yield from self.init_connection()
        cur = dbmanager.cur

        table_name = "data._%s" % offering['name'].lower()

        columns = []
        from_uom=''
        conversion_query=''
        to_unit=''
        if request.get_filter("in_unit") is not None:
            to_unit=yield from self.findLookUp(request.get_filter("in_unit"))
        # columns_qi = []
        op_filter = request.get_filter('observedProperties')

        observation = Observation.get_template({
            "offering": offering['name'],
            "procedure": offering['procedure']
        })

        if offering.is_complex():
            observation["type"] = setting._COMPLEX_OBSERVATION
            op = offering.get_complex_observable_property()
            observation["observedProperty"] = \
                ObservedPropertyComplex.get_template({
                    "def": op['definition'],
                    "name": op['name'],
                    "type": op['type'],
                    "uom": to_unit
                })
            for op in offering['observable_properties']:
                if op['type'] == setting._COMPLEX_OBSERVATION:
                    continue
                else:
                    # observedProperty filters are applied here excluding
                    # the observed properties columns from the query
                    if op_filter is not None and (
                            op['definition'] not in op_filter):
                        continue

                    observation["observedProperty"]['fields'].append(
                        ObservedProperty.get_template({
                            "def": op['definition'],
                            "name": op['name'],
                            "type": op['type'],
                            "uom": to_unit
                        })
                    )
                    columns.append(op['column'])
                    from_uom=op['uom']
                    # columns_qi.append('%s_qi' % op['column'])

        elif offering.is_array():
            raise Exception("Not implemented yet")

        else:
            for op in offering['observable_properties']:
                observation["type"] = op['type']
                # observedProperty filters are applied here excluding
                # the observed properties columns from the query
                if op_filter is not None and (
                        op['definition'] not in op_filter):
                    continue

                observation["observedProperty"] = \
                    ObservedProperty.get_template({
                        "def": op['definition'],
                        "name": op['name'],
                        "type": op['type'],
                        "uom": to_unit
                    })
                columns.append(op['column'])
                from_uom=op['uom']
                # columns_qi.append('%s_qi' % op['column'])
        # if request.get_filter("in_unit") is not None:
            # conversion_query="(%s::text||'%s')::unit@@'%s' as %s "%(", ".join(columns), from_uom, to_unit, ", ".join(columns))
        conversion_query = ''
        if request.get_filter("in_unit") is not None:
            to_unit = yield from self.findLookUp(request.get_filter("in_unit"))
            if request.get_filter("operation") is not None:
                if 'unit' in request.get_filter("operation"):
                    unit = yield from self.findLookUp(request.get_filter("operation")['unit'])
                    if 'qty' in request.get_filter("operation"):
                        qty = request.get_filter("operation")['qty']
                        if 'type' in request.get_filter("operation"):
                            if request.get_filter("operation")['type'] == 'add':
                                if qty == '':
                                    qty = 0
                                conversion_query = """(%s::text||'%s')::unit + ('%s'::text||'%s')::unit@@'%s' as %s """%(", ".join(columns), from_uom, qty, unit, to_unit, ", ".join(columns))
                                conversion_uom = to_unit
                            elif request.get_filter("operation")['type'] == 'sub':
                                if qty == '':
                                    qty = 0
                                conversion_query = """(%s::text||'%s')::unit - ('%s'::text||'%s')::unit@@'%s' as %s """%(", ".join(columns), from_uom, qty, unit, to_unit, ", ".join(columns))
                                conversion_uom = to_unit
                            elif request.get_filter("operation")['type'] == 'mul':
                                if qty == '':
                                    qty = 1
                                conversion_query = """(%s::text||'%s')::unit * '%s %s' ::unit@@'%s*%s' as %s """%(", ".join(columns), from_uom, qty, unit, to_unit, unit, ", ".join(columns))
                                conversion_uom = """ %s*%s """%(to_unit,unit)
                            elif request.get_filter("operation")['type'] == 'div':
                                if qty == '':
                                    qty = 1
                                conversion_query = """(%s::text||'%s')::unit / '%s %s' ::unit@@'%s/%s' as %s """%(", ".join(columns), from_uom, qty, unit, to_unit, unit, ", ".join(columns))
                                conversion_uom = """ %s/%s """%(to_unit,unit)
                else:
                    if 'qty' in request.get_filter("operation"):
                        qty = request.get_filter("operation")['qty']
                        if 'type' in request.get_filter("operation"):
                            if request.get_filter("operation")['type'] == 'add':
                                if qty == '':
                                    qty = 0
                                conversion_query = """(%s::text||'%s')::unit + ('%s'::text||'%s')::unit@@'%s' as %s """%(", ".join(columns), from_uom, qty, from_uom, to_unit, ", ".join(columns))
                                conversion_uom = to_unit
                            elif request.get_filter("operation")['type'] == 'sub':
                                if qty == '':
                                    qty = 0
                                conversion_query = """(%s::text||'%s')::unit - ('%s'::text||'%s')::unit@@'%s' as %s """%(", ".join(columns), from_uom, qty, from_uom, to_unit, ", ".join(columns))
                                conversion_uom = to_unit
                            elif request.get_filter("operation")['type'] == 'mul':
                                if qty == '':
                                    qty = 1
                                conversion_query = """(%s::text||'%s')::unit * '%s %s' ::unit@@'%s*%s' as %s """%(", ".join(columns), from_uom, qty, from_uom, to_unit, to_unit, ", ".join(columns))
                                conversion_uom = """ %s*%s """%(to_unit,to_unit)
                            elif request.get_filter("operation")['type'] == 'div':
                                if qty == '':
                                    qty = 1
                                conversion_query = """(%s::text||'%s')::unit / '%s %s' ::unit@@'%s/%s' as %s """%(", ".join(columns), from_uom, qty, from_uom, to_unit, to_unit, ", ".join(columns))
                                conversion_uom = """ %s/%s """%(to_unit,to_unit)
            else:
                conversion_query = """(%s::text||'%s')::unit@@'%s' as %s """%(", ".join(columns), from_uom, to_unit, ", ".join(columns))
                conversion_uom = to_unit
        elif request.get_filter("operation") is not None:
            if 'unit' in request.get_filter("operation"):
                unit = yield from self.findLookUp(request.get_filter("operation")['unit'])
                if 'qty' in request.get_filter("operation"):
                    qty = request.get_filter("operation")['qty']
                    if 'type' in request.get_filter("operation"):
                        if request.get_filter("operation")['type'] == 'add':
                            if qty == '':
                                qty = 0
                            conversion_query = """(%s::text||'%s')::unit + ('%s'::text||'%s')::unit@@'%s' as %s """%(", ".join(columns), from_uom, qty, unit, from_uom, ", ".join(columns))
                            conversion_uom = from_uom
                        elif request.get_filter("operation")['type'] == 'sub':
                            if qty == '':
                                qty = 0
                            conversion_query = """(%s::text||'%s')::unit - ('%s'::text||'%s')::unit@@'%s' as %s """%(", ".join(columns), from_uom, qty, unit, from_uom, ", ".join(columns))
                            conversion_uom = from_uom
                        elif request.get_filter("operation")['type'] == 'mul':
                            if qty == '':
                                qty = 1
                            conversion_query = """(%s::text||'%s')::unit - ('%s'::text||'%s')::unit@@'%s' as %s """%(", ".join(columns), from_uom, qty, unit, from_uom, ", ".join(columns))
                            conversion_uom = """ %s*%s """%(from_uom,unit)
                        elif request.get_filter("operation")['type'] == 'div':
                            if qty == '':
                                qty = 1
                            conversion_query = """(%s::text||'%s')::unit / '%s %s' ::unit@@'%s/%s' as %s """%(", ".join(columns), from_uom, qty, unit, from_uom, unit, ", ".join(columns))
                            conversion_uom = """ %s/%s """%(from_uom,unit)
            else:
                if 'qty' in request.get_filter("operation"):
                    qty = request.get_filter("operation")['qty']
                    if 'type' in request.get_filter("operation"):
                        if request.get_filter("operation")['type'] == 'add':
                            if qty == '':
                                qty = 0
                            conversion_query = """(%s::text||'%s')::unit + ('%s'::text||'%s')::unit@@'%s' as %s """%(", ".join(columns), from_uom, qty, from_uom, from_uom, ", ".join(columns))
                            conversion_uom = from_uom
                        elif request.get_filter("operation")['type'] == 'sub':
                            if qty == '':
                                qty = 0
                            conversion_query = """(%s::text||'%s')::unit - ('%s'::text||'%s')::unit@@'%s' as %s """%(", ".join(columns), from_uom, qty, from_uom, from_uom, ", ".join(columns))
                            conversion_uom = from_uom
                        elif request.get_filter("operation")['type'] == 'mul':
                            if qty == '':
                                qty = 1
                            conversion_query = """(%s::text||'%s')::unit * '%s %s' ::unit@@'%s*%s' as %s """%(", ".join(columns), from_uom, qty, from_uom, from_uom, from_uom, ", ".join(columns))
                            conversion_uom = """ %s*%s """%(from_uom,from_uom)
                        elif request.get_filter("operation")['type'] == 'div':
                            if qty == '':
                                qty = 1
                            conversion_query = """(%s::text||'%s')::unit / '%s %s' ::unit@@'%s/%s' as %s """%(", ".join(columns), from_uom, qty, from_uom, from_uom, from_uom, ", ".join(columns))
                            conversion_uom = """ %s/%s """%(from_uom,from_uom)
        else:
            conversion_query="%s"%(", ".join(columns))

        observation["phenomenonTime"] = {
            "timePeriod": {
                "begin": "",
                "end": ""
            }
        }

        if request.get_filter(
                "responseFormat") in setting._responseFormat['vega']:
            fastSql = """
                SELECT array_to_json(
                    array_agg(('{
                        "o": "%s",
                        "b": "' || to_char(
                            begin_time, 'YYYY-MM-DD"T"HH24:MI:SS+02:00')
                            || '",
                        "e": "' || to_char(
                            end_time, 'YYYY-MM-DD"T"HH24:MI:SS+02:00')
                            || '",
                        "r": "' || to_char(
                            result_time, 'YYYY-MM-DD"T"HH24:MI:SS+02:00')
                            || '",
                        "a": "' || %s || '"
                    }')::json)
                )
                FROM (
            """ % (
                offering['name'],
                columns[0],
            )

        else:
            fastSql = """
                SELECT
                    array_to_json(
                        array_agg(('{
                            "offering": "%s",
                            "procedure": "%s",
                            "type": %s,
                            "featureOfInterest": "ciao",
                            "phenomenonTime": {
                                "timePeriod": {
                                    "begin": "' || begin_time || '",
                                    "end": "' || end_time || '"
                                }
                            },
                            "resultTime": {
                                "timeInstant": {
                                    "instant": "' || result_time || '"
                                }
                            },
                            "result": "' || %s || '",
                            "observedProperty": %s
                        }')::json)
                )
                FROM (
                """ % (
                offering['name'],
                offering['procedure'],
                json.dumps(observation["type"]),
                columns[0],
                json.dumps(observation["observedProperty"])
            )

        sql = """
            SELECT
                begin_time,
                end_time,
                result_time,
                %s""" % (
                             conversion_query
                ) + """
            FROM %s
            """ % table_name
        temporal = []
        where = []
        params = []
        if request.get_filters() is not None:
            keys = list(request.get_filters())
            for key in keys:
                fltr = request.get_filters()[key]
                if key == 'temporal':
                    if fltr['fes'] == 'during':
                        temporal.append("""
                            begin_time >= %s::timestamp with time zone
                        AND
                            end_time <= %s::timestamp with time zone
                        """)
                        params.extend(fltr['period'])

                    elif fltr['fes'] == 'equals':
                        temporal.append("""
                            begin_time = end_time
                        AND
                            begin_time = %s::timestamp with time zone
                        """)
                        params.append(fltr['instant'])

                    where.append(
                        "(%s)" % (' OR '.join(temporal))
                    )

        if len(where) > 0:
            sql += "WHERE %s" % (
                'AND'.join(where)
            )

        sql = """
            SET enable_seqscan=false;
            SET SESSION TIME ZONE '+02:00';
            %s
            %s
             ORDER BY begin_time ) t
        """ % (
            fastSql,
            sql
        )

        istsos.debug(
            (
                yield from cur.mogrify(sql, tuple(params))
            ).decode("utf-8")
        )

        sqlExtensionUnit="""CREATE EXTENSION IF NOT EXISTS unit;"""
        yield from cur.execute(sqlExtensionUnit)

        yield from cur.execute(sql, tuple(params))
        rec = yield from cur.fetchone()

        request['observations'] += rec[0]

        yield from self.__download_csv_from_json(request, rec[0])

        # recs = yield from cur.fetchall()
        istsos.debug("Data is fetched!")
