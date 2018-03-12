#!/usr/bin/env python2.7

# CleanDNS environment - 0.1

import os

# Creating environment variables
os.environ['PATH'] = '/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/sbin:/usr/local/bin:/root/bin'
os.environ['_TMP_DIR'] = '/tmp'
os.environ['_BIND_DIR'] = '/cf/named/etc/namedb'
os.environ['_CLEANDNS_DIR'] = '/cf/cleandns'
os.environ['_PRESINKHOLE_FILE'] = os.environ['_CLEANDNS_DIR'] + '/spool/presinkhole.txt'
os.environ['_PRESINKHOLE2_FILE'] = os.environ['_CLEANDNS_DIR'] + '/spool/presinkhole1.txt'
os.environ['_SINKHOLE_FILE'] =  os.environ['_BIND_DIR'] + '/sinkhole.zones'
os.environ['_SINKHOLE_TARGET'] = '/etc/namedb/sinkhole.target'
os.environ['_SINKHOLE_EXPORT'] = os.environ['_CLEANDNS_DIR'] + '/spool/sinkhole_export.txt'
os.environ['_DOMAIN_FILE'] = os.environ['_CLEANDNS_DIR'] + '/spool/ips-otx.txt'
# tested jan/16
# print os.environ['_PRESINKHOLE_FILE']
