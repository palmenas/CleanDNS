#!/usr/bin/env python2.7

# update ips files - 0.0.1 (01/20/18)
# update ips files - 0.1.0 (01/27/18)
# update ips files - 0.1.1 (01/28/18)

# Import libraries
import os
import sys
import ConfigParser
import shutil
import glob
import re
import subprocess
import time
import binascii
import socket

# Local files
import clean_environ

# Read configuration file
config = ConfigParser.RawConfigParser()
config.read('/cf/cleandns/etc/setup.cfg')

# Some vars
BIND_DIR = config.get('bind', 'dir')
CLEAN_DIR = config.get('cleandns', 'dir')
LOCAL_BL_IPS = config.get('local_settings','blacklist_ips')
PRE_SINKHOLE_FILE_1 = config.get('pre_sinkhole', 'file1')
PRE_SINKHOLE_FILE_2 = config.get('pre_sinkhole', 'file2')
SURICATA_INSTALLED_DIR = config.get('suricata','installed_dir')
SURICATA_INSTALLED_RULE = config.get('suricata', 'installed_rule')
SINKHOLE_BLOCK_RULE = config.get('suricata','block_rule')
SURICATA_ACTION = config.get('suricata', 'action')
SURICATA_BL_1 = config.get('suricata', 'iplist_1')
SURICATA_BL_2 = config.get('suricata', 'iplist_2')
SURICATA_PRE_RULE = config.get('suricata', 'prerule')
SINKHOLE_FILE_1 = config.get('sinkhole', 'file1')
TMP_DIR = config.get('tmp', 'dir')

# Count the threats
def file_len(f_name):
    with open(f_name) as f:
        for i, l in enumerate(f):
            pass
    return(i + 1)

# Update IPS
def ips_mod():
    # Deleting old files
    if os.path.isfile(SINKHOLE_BLOCK_RULE): os.remove(SINKHOLE_BLOCK_RULE)
    if os.path.isfile(SURICATA_PRE_RULE): os.remove(SURICATA_PRE_RULE)

    print "Updating IPs BlackLists"
    for source in sorted(glob.glob(CLEAN_DIR + '/etc/sources/enabled/ips*sh')):
        subprocess.call(source)
        time.sleep(1)

    # Local Blacklist
    shutil.copyfile(LOCAL_BL_IPS, SURICATA_BL_2)

    # Deduplicating
    s_regs = set()
    for r_file in glob.glob(CLEAN_DIR + '/spool/ips-*'):
        with open(r_file) as f:
            for line in f:
                if socket.inet_aton(line): s_regs.add(line)

    # Writing sorted, seded, uniqed
    all_regs_file = open(SURICATA_BL_2, 'a')
    all_regs_file.writelines(sorted(s_regs))
    all_regs_file.close()

    # Cleaning Whitelist
    print 'Cleaning whitelist'
    subprocess.call(CLEAN_DIR + '/bin/run_whitelist_ips.sh')

    # IP to Hex -> Suricata
    print 'Updating Suricata Rules'
    counter = 1
    with open(SURICATA_BL_1) as f:
        for line in f:
            try:
                socket.inet_aton(line)
                hex_ip = binascii.hexlify(socket.inet_aton(line)).upper()
                str_hex_ip = hex_ip[0:2] + ' ' + hex_ip[2:4] + ' ' + hex_ip[4:6] + ' ' + hex_ip[6:8]
                f_regs.add(SURICATA_ACTION + ' udp any 53 -> any any (msg:"CleanDNS_Phase3: dns reponse for a malicious IP ' + re.sub('\n', '', line) + ' "; sid:3210 ' + str(counter) + ' ; rev:001; content:"|' + str_hex_ip + '|";)\n')
                counter += 1
            except socket.error:
                continue

    # Write the lines to suricata file
    with open(SINKHOLE_BLOCK_RULE, 'w') as f:
        for s in sorted(f_regs):
            f.write(s)

    # Update Suricata
    if os.path.isfile(SINKHOLE_BLOCK_RULE):
        os.remove(SURICATA_INSTALLED_DIR + SURICATA_INSTALLED_RULE)
        shutil.copyfile(SINKHOLE_BLOCK_RULE, SURICATA_INSTALLED_DIR + SURICATA_INSTALLED_RULE)
        subprocess.call(CLEAN_DIR + '/sbin/update_suricataconfig.sh')

    # Counting
    print 'CleanDNS is protecting against %s malware IPs!\nEnjoy!' % file_len(SINKHOLE_BLOCK_RULE)

# Update sinkhole
def sinkhole():
    os.chdir(TMP_DIR)
    # Getting sources
    print '... Updating malware blacklists ...'
    for source in sorted(glob.glob(CLEAN_DIR + '/etc/sources/enabled/domains-*')):
        subprocess.call(source)
        time.sleep(1)

    # Creating local blacklist
    shutil.copyfile(CLEAN_DIR + '/etc/local_blacklist-domains.conf', PRE_SINKHOLE_FILE_2)

    # Deduplicating
    s_regs = set()
    for r_file in glob.glob(CLEAN_DIR + '/spool/domains-*'):
        with open(r_file) as f:
            for line in f:
                line = re.sub(' ','',line)
                if re.search('[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}', line):
                    continue
                elif re.search('\.$', line):
                    continue
                elif re.search('^$', line):
                    continue
                else:
                    s_regs.add(line.lower())

    # Writing sorted, seded, uniqed
    all_regs_file = open(PRE_SINKHOLE_FILE_2, 'a')
    all_regs_file.writelines(sorted(s_regs))
    all_regs_file.close()

    # Cleaning whitelist
    subprocess.call(CLEAN_DIR + '/bin/run_whitelist_domains.sh')

    # Creating new sinkhole file
    os.remove(SINKHOLE_FILE_1)

    # Step trough lines
    dom_set = set()

    with open(PRE_SINKHOLE_FILE_1) as f:
        for domain in f:
            dom_set.add('zone "' + re.sub(r'\n','',domain) + '" {type master; file "/etc/namedb/sinkhole.target";};\n')

    sinkhole_temp_file = open(SINKHOLE_FILE_1, 'w')
    sinkhole_temp_file.writelines(sorted(dom_set))
    sinkhole_temp_file.close()

    # Change ownership of sinkhole file to bind
    subprocess.call(['chown', 'bind:bind', SINKHOLE_FILE_1])

    # Creating LOG for Suricata
    print '... Creating LOG Syntax ...'

    #START SERVICE
    print '... Restarting Bind: '
    subprocess.call(['pfSsh.php', 'playback', 'svc', 'stop', 'named'], shell=False)
    time.sleep(20)
    subprocess.call(['pfSsh.php', 'playback', 'svc', 'start', 'named'], shell=False)
    print 'Done ...'

    # Counting
    print 'CleanDNS is protecting against %s malware and phishing domains!\nEnjoy!' % file_len(SINKHOLE_FILE_1)

# Main function
def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-i', '--ips', dest='ips', help='Protect against IPs', action='store_true')
    argparser.add_argument('-d', '--domains', dest='domains', help='Protect against Domains', action='store_true')
    args = argparser.parse_args()

    if (args.ips):
        update_malwaredomainlist()
    elif (args.domains):
        update_otx()
    else:
        os.system(sys.argv[0] + ' -h')

# If main ;-)
if __name__ == '__main__':
    main()
