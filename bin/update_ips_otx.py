#!/usr/bin/env python2.7

# update ips otx - 0.0.1 (2018)

# Libraries
import argparse
import ConfigParser
import os
import socket
import sys

# Constants
config = ConfigParser.RawConfigParser()
config.read('/cf/cleandns/etc/setup.cfg')

# Some vars
CLEANDNS_DIR = config.get('cleandns', 'dir')
TMP_DIR = config.get('tmp', 'dir')
IP_FILE = CLEANDNS_DIR  + '/spool/ips-otx.txt'

#MAIN
subsystem.call('update_ips.py --otx')