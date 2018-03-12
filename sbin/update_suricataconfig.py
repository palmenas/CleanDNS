#!/usr/bin/env python2.7

# update suricata config - 0.0.1 (03/10/2018)

__description__ = 'Update suricata rules'
__author__ = 'Palmenas Diniz'
__version__ = '0.0.1'
__date__ = '2018/03/10'


"""
Source code in bitbucket.org/cleandnscode
No Copyright

Use at your own risk

Developed with Python 2.7

History:
  2018/03/10: 0.0.1 when the Python expression returns None (in stead of a byte value), no byte is written to output.

Todo:
  - Logs
"""

# Import libraries
import argparse
import binascii
import ConfigParser
import glob
import os
import re
import shutil
import socket
import sys

# Read configuration file
config = ConfigParser.RawConfigParser()
config.read('/cf/cleandns/etc/setup.cfg')

# Some constants
CLEANDNS_DIR = config.get('cleandns', 'dir')
CLEANDNSMOD = config.get('suricata', 'cleandnsmod')
LOCAL_BL_IPS = config.get('local_settings','blacklist_ips')
IPREPLIST = config.get('cleandns','ip_rep_list')
SURICATA_INSTALLED_DIR = config.get('suricata','installed_dir') + '/rules'
SURICATA_INSTALLED_RULE = config.get('suricata', 'installed_rule')
SURICATA_INTERFACE = config.get('suricata','interface')
SURICATA_ACTION = config.get('suricata', 'action')
SURICATA_RULES = config.get('suricata', 'rules')

def main():
    os.chdir(SURICATA_INSTALLED_DIR)
    with open(SURICATA_RULES) as f:
        s_regs = []
        for line in f:
            if re.search(r'^drop (http|smtp|tls)', line):
                continue
            elif re.search('$DNS_SERVERS', line):
                line = re.sub('!$DNS_SERVERS', 'any', line)
                line = re.sub('$DNS_SERVERS', 'any', line)
                s_regs.append(line)
            elif re.search('![$SMTP_SERVERS,any]', line):
                line = re.sub('![$SMTP_SERVERS,any]', 'any', line)
                s_regs.append(line)
            else:
                s_regs.append(line)

    # Writing
    f = open(CLEANDNSMOD, 'w')
    f.writelines(s_regs)
    f.close()

    with open('../suricata.yaml') as f:
        s_regs = []
        for line in f:
            if re.search('suricata.rules', line):
                line = re.sub('suricata.rules', 'cleandns.rules', line)
            s_regs.append(line)

    f = open('../suricata2.yaml', 'w')
    f.writelines(s_regs)
    f.close

    # Move temp to production
    os.rename('../suricata2.yaml', '../suricata.yaml')

    # Restart service
    print '... Restarting Suricata: '
    os.system('pfSsh.php playback svc stop suricata ' + SURICATA_INTERFACE + ' > /dev/null')
    os.system('pfSsh.php playback svc start suricata ' + SURICATA_INTERFACE + ' > /dev/null')
    print 'Done ...'

# If main :x
if __name__ == '__main__':
    main()
