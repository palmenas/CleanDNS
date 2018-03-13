#!/usr/bin/env python2.7

# update master - 0.0.1 (01/20/2018)

# Import libraries
import argparse
import binascii
import ConfigParser
import glob
import os
import re
import shutil
import socket
import subprocess
import sys
import time

# Local
import clean_environ

# Read configuration file
config = ConfigParser.RawConfigParser()
config.read('/cf/cleandns/etc/setup.cfg')

# Some constants
CLEANDNS_DIR = config.get('cleandns', 'dir')
LOCAL_BL_IPS = config.get('local_settings','blacklist_ips')
SURICATA_INSTALLED_DIR = config.get('suricata','installed_dir')
SURICATA_INSTALLED_RULE = config.get('suricata', 'installed_rule')
SURICATA_BLOCK_RULE = config.get('suricata','block_rule')
SURICATA_ACTION = config.get('suricata', 'action')
SURICATA_BL_1 = config.get('suricata', 'iplist_1')
SURICATA_BL_2 = config.get('suricata', 'iplist_2')
SURICATA_PRE_RULE = config.get('suricata', 'prerule')

# Count the lines on a file
def file_len(f_name):
    with open(f_name) as fh:
        for i, l in enumerate(fh):
            pass
    return(i + 1)

# Update the source files, be it a domain of IPs
def update_ips_mod():

    # Deleting old files
    if os.path.isfile(SURICATA_BLOCK_RULE): os.remove(SURICATA_BLOCK_RULE)
    if os.path.isfile(SURICATA_PRE_RULE): os.remove(SURICATA_PRE_RULE)

    print "Updating IPs BlackLists"
    enabled_sources = config.get('sources','ips').split(' ')
    for i in enabled_sources:
        print '%s/bin/update_ips.py --%s' % (CLEANDNS_DIR, i)
        # os.system(CLEANDNS_DIR + '/bin/update_ips.py --' +i)
    exit(0)

    #
    # EXITING HERE
    #

    # Local Blacklist
    shutil.copyfile(LOCAL_BL_IPS, SURICATA_BL_2)

    # Deduplicating
    s_regs = set()
    for r_file in glob.glob(CLEANDNS_DIR + '/spool/ips-*'):
        with open(r_file) as fh:
            # Organize the file and clean
            for line in fh:
                line = re.sub(' \n','',line)
                if re.search('^[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}$', line):
                    s_regs.add(line)

    # Writing sorted, seded, uniqed
    fh = open(SURICATA_BL_2, 'a')
    fh.writelines(sorted(s_regs))
    fh.close()

    # Cleaning Whitelist
    print 'Cleaning whitelist'
    subprocess.call(CLEANDNS_DIR + '/bin/run_whitelist_ips.sh')

    # IP to Hex -> Suricata
    print 'Updating Suricata Rules'
    r_file = open(SURICATA_BL_1, 'r')
    r_file_lines = r_file.readlines()
    r_file.close()
    counter = 1
    f_regs = set()
    for line in r_file_lines:
        try:
            socket.inet_aton(line)
            hex_ip = binascii.hexlify(socket.inet_aton(line)).upper()
            str_hex_ip = hex_ip[0:2] + ' ' + hex_ip[2:4] + ' ' + hex_ip[4:6] + ' ' + hex_ip[6:8]
            f_regs.add(SURICATA_ACTION + ' udp any 53 -> any any (msg:"CleanDNS_Phase3: dns reponse for a malicious IP ' \
                + re.sub('\n', '', line) + ' "; sid:3210 ' + str(counter) + ' ; rev:001; content:"|' + str_hex_ip + '|";)\n')
            counter += 1
        except socket.error:
            continue

    fhan_suri_block_rule = open(SURICATA_BLOCK_RULE, 'w')
    fhan_suri_block_rule.writelines(sorted(f_regs))
    fhan_suri_block_rule.close()
    # print 'File created' + str(os.path.isfile(SURICATA_BLOCK_RULE))

    # Update Suricata
    if os.path.isfile(SURICATA_BLOCK_RULE):
        os.remove(SURICATA_INSTALLED_DIR + SURICATA_INSTALLED_RULE)
        shutil.copyfile(SURICATA_BLOCK_RULE, SURICATA_INSTALLED_DIR + SURICATA_INSTALLED_RULE)
        subprocess.call(CLEANDNS_DIR + '/sbin/update_suricataconfig.sh')

    # Counting
    print 'CleanDNS is protecting against %s  malware IPs!\nEnjoy!' % file_len(SURICATA_BLOCK_RULE)

def update_sinkhole():
    exit(0)

# Main function
def main():
    # Parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ips_mod', help='Update IP files', action='store_true')
    parser.add_argument('-s', '--sinkhole', help='Update sinkhole files', action='store_true')
    args = parser.parse_args()

    # Check values parsed
    if args.ips_mod:
        update_ips_mod()
    elif args.sinkhole:
        update_sinkhole()
    else:
        subprocess.call([sys.argv[0], '-h'])

# If main :)
if __name__ == '__main__':
    main()
