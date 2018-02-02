#!/usr/bin/env python2.7

# update otx - 0.0.1 (01/24/2018)
# 0.0.2 (02/01/2018)

# Import libraries
import argparse
import ConfigParser
import json
import sys

from OTXv2 import OTXv2
from OTXv2 import IndicatorTypes

# Read configuration file
def download_partial():
    print 'Downloading partial indicators.'
    config = ConfigParser.RawConfigParser()
    try:
        # Read configuration file
        config.read('/cf/cleandns/etc/setup.cfg')
        API_KEY = config.get('otx', 'key')
        OTX_SERVER = config.get('otx', 'server')
        otx = OTXv2(API_KEY, server=OTX_SERVER)

        # Download partial indicators (test) (1 page with limit of 10 records)
        pulses = otx.getall_iter(max_page=1, limit=10)
        f = open('pulses.txt', 'w')
        for p in pulses:
            for i in p['indicators']:
                if i['type'] == 'IPv4' or i['type'] == 'URL':
                    f.write(str(i['indicator']) + '\n')
        f.close()

    except:
        print 'ERROR: Could not parse config'
        return False
    print 'Done downloading indicators.'

"""
    Download the full list of indicators
    note that it will take a long time
    Aprox 1gb of information will be downloaded
"""
def download_full():
    print 'Downloading FULL indicators... sit and wait ! :)'
    config = ConfigParser.RawConfigParser()
    try:
        # Read configuration file
        config.read('/cf/cleandns/etc/setup.cfg')
        API_KEY = config.get('otx', 'key')
        OTX_SERVER = config.get('otx', 'server')
        otx = OTXv2(API_KEY, server=OTX_SERVER)

        # Download ALL indicators (about 1GB)
        pulses = otx.getall_iter()
        f = open('pulses.txt', 'w')
        for p in pulses:
            for i in p['indicators']:
                if i['type'] == 'IPv4' or i['type'] == 'URL':
                    f.write(str(i['indicator']) + '\n')
        f.close()

    except:
        print 'ERROR: Could not parse config'
        return False

# Main functino
def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-F', '--FULL', dest='full', help='Download ALL IOCs (aprox 1GB)', action='store_true')
    argparser.add_argument('-i', dest='ips', default=None, help='Download 3 pages of IOCs type IPv4 and URL', action='store_true')
    args = argparser.parse_args()

    if (args.ips):
        download_partial()
    elif (args.full):
        download_full()

# If main then main
if __name__ == '__main__':
    main()
