# -*- coding: utf-8 -*-
# Inspired by Ken Weiner
# https://goo.gl/GkVRlg


import sys
import subprocess
from decimal import Decimal

url = sys.argv[1]

if len(sys.argv) == 1:
    print("Web address not given")
    exit()


getCapabilities = (
    'service=SOS&request=GetCapabilities&service=SOS'
    '&version=2.0.0&AcceptVersions=2.0.0'
)

describeSensor = (
    'service=SOS&request=DescribeSensor&service=SOS'
    '&version=2.0.0&procedure=urn:ogc:def:procedure:x-istsos:1.0:LUGANO'
    '&procedureDescriptionFormat=http://www.opengis.net/sensorML/1.0.1'
)


def execute(url):
    print("\nAddress: %s\n" % (url))

    process = subprocess.Popen([
            'curl',
            '-s',
            '-w',
            (
                '%{time_namelookup},%{time_pretransfer},'
                '%{time_starttransfer},%{time_total}'
            ),
            '-o',
            '/dev/null',
            "%s" % (url)
        ],
        stdout=subprocess.PIPE
    )
    out, err = process.communicate()

    data = [Decimal(x) for x in out.split(",")]

    result = """Time (in sec):
--------------
DNS Lookup:     %s
TCP Connection: %s
Generation:     %s
Download:       %s
=====================
Total:          %s
    """ % (
        data[0],
        data[1] - data[0],
        data[2] - data[1],
        data[3] - data[2],
        data[3]
    )

    print(result)


execute("%s?%s" % (url, getCapabilities))
