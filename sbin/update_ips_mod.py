#!/usr/bin/env python2.7

# update ips mod - 0.0.1 (01/19/18)

# Import libraries
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

# Some vars
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
    with open(f_name) as f:
        for i, l in enumerate(f):
            pass
    return(i + 1)

# Main function
def main():
    # Deleting old files
    if os.path.isfile(SURICATA_BLOCK_RULE):
        os.remove(SURICATA_BLOCK_RULE)

    if os.path.isfile(SURICATA_PRE_RULE):
        os.remove(SURICATA_PRE_RULE)

    print "Updating IPs BlackLists"
    for source in sorted(glob.glob(CLEANDNS_DIR + '/etc/sources/enabled/ips*sh')):
        subprocess.call(source)
        time.sleep(1)

    # Local Blacklist
    shutil.copyfile(LOCAL_BL_IPS, SURICATA_BL_2)

    # Deduplicating
    s_regs = set()
    for r_file in glob.glob(CLEANDNS_DIR + '/spool/ips-*'):
        r_file_tmp = open(r_file, 'r')
        r_file_tmp_lines = r_file_tmp.readlines()
        r_file_tmp.close()

        # Organize the file and clean
        for line in r_file_tmp_lines:
            line = re.sub(' \n','',line)
            if re.search('^[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}$', line):
                s_regs.add(line)

    # Writing sorted, seded, uniqed
    all_regs_file = open(SURICATA_BL_2, 'a')
    all_regs_file.writelines(sorted(s_regs))
    all_regs_file.close()

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
            f_regs.add(SURICATA_ACTION + ' udp any 53 -> any any (msg:"CleanDNS_Phase3: dns reponse for a malicious IP ' + re.sub('\n', '', line) + ' "; sid:3210 ' + str(counter) + ' ; rev:001; content:"|' + str_hex_ip + '|";)\n')
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
    print 'CleanDNS is protecting against ' + str(file_len(SURICATA_BLOCK_RULE)) + ' malware IPs!\nEnjoy!'

if __name__ == '__main__':
    main()
