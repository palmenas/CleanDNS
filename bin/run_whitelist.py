#!/usr/bin/env python2.7

# run whitelists 0.0.1 (03/10/2018)

__description__ = 'Run IOCs'
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

# Libraries
import argparse
import ConfigParser
import os
import socket
import sys

# Constants
CLEANDS_DIR = config.get('cleandns','dir')
PRESINKHOLE_FILE = CLEANDNS_DIR+'/spool/suricata_blacklist1.txt'
PRESINKHOLE_FILE2 = CLEANDNS_DIR+'/spool/suricata_blacklist.txt'
RUN_PRESINKHOLE_FILE = CLEANDNS_DIR+'/spool/clean_suricata_blacklist.txt'

# Whitelist Domains
def whitelist_domains():
    print 'domains'

# Whitelist IPs
def whitelist_ips():
    print 'ips'
    # cp $_PRESINKHOLE_FILE $_RUN_PRESINKHOLE_FILE
    shutil.copyfile(PRESINKHOLE_FILE, RUN_PRESINKHOLE_FILE)

    with open(CLEANDNS_DIR+'/etc/local_whitelist-ips.conf') as fh:
        for line in fh:
            shutil.copyfile(RUN_PRESINKHOLE_FILE, PRESINKHOLE_FILE)
            with open(PRESINKHOLE_FILE) as fh2:
                for line2 in fh2:
                    re.sub(line,'',line2)

    for i in glob.glob('')
    #MAIN
    foreach name ( `cat $_CLEANDNS_DIR/etc/local_whitelist-ips.conf` )

    cat $_PRESINKHOLE_FILE | sed '/'$name'$/d' > $_RUN_PRESINKHOLE_FILE
    end
    cp $_RUN_PRESINKHOLE_FILE $_PRESINKHOLE_FILE2

# Main function
def main():
    # Parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domains', dest='dom', help='Run whitelist for domains', action='store_true')
    parser.add_argument('-i', '--ips', dest='ips', help='Run shitelist for IPs', action='store_true')
    args = parser.parse_args()

    # Check values parsed
    if (args.dom):
        whitelist_domains()
    elif (args.ips):
        whitelist_ips()
    else:
        os.system(sys.argv[0] + ' -h')

# If main :)
if __name__ == '__main__':
    main()
