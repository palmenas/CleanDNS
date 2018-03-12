#!/usr/bin/env python

# get iocs 0.0.2 (03/10/2018)

__description__ = 'Get IOCs'
__author__ = 'Palmenas Diniz'
__version__ = '0.0.2'
__date__ = '2018/03/10'

"""
Source code in bitbucket.org/cleandnscode
No Copyright

Use at your own risk

Developed and tested with Python 2.7

History:
  2018/03/10: 0.0.1 ????

Todo:
"""

# Import libraries
import os
import subprocess
import sys

# Set environment variables
os.environ['PATH'] = '/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/sbin:/usr/local/bin:/root/bin'
os.environ['_TMP_DIR'] = '/tmp'
os.environ['_BIND_DIR'] = '/cf/named/etc/namedb'
os.environ['_CLEANDNS_DIR'] = '/cf/cleandns'
os.environ['_PRESINKHOLE_DIR'] = os.environ['_CLEANDNS_DIR']+'/spool/presinkhole.txt'

os.environ['_CURL'] = '/usr/local/bin/curl'
os.environ['_PHP'] = '/usr/local/bin/php'

# Vars

# Get the first argument
_type = sys.argv[1]
_types = ['SHA1', 'IPv4', 'URL', 'domain', 'IPV6', 'hostname']

def main():
    print _type
    print os.environ['_PRESINKHOLE_DIR']
    if _type in _types:
        print "Found"

 #   try:
  #      RETCODE = subprocess.call('/cf/cleandns/sbin/update_ips_mod.sh', shell=False)
   #     if RETCODE < 0:
    #        print >> sys.stderr, 'Process terminated with exit code:', -RETCODE
    #    else:
    #        print >> sys.stderr, 'Process returned:', RETCODE
#    except OSError as RETCODE_E:
    #    print >> sys.stderr, 'Failed to start the process:', RETCODE_E

if __name__ == '__main__':
    main()
