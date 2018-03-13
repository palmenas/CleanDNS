#!/usr/bin/env python2.7

# update sinkhole - 0.0.1 (01/15/2018)
# update sinkhole - 0.0.2 (01/17/2018)
# update sinkhole - 0.0.3 (01/19/2018)

# Import libraries
import os
import sys
import ConfigParser
import shutil
import glob
import re
import subprocess
import time

# Think not needed
import clean_environ

# Read configuration file
config = ConfigParser.RawConfigParser()
config.read('/cf/cleandns/etc/setup.cfg')

# Reading the config file
CLEAN_DIR = config.get('cleandns', 'dir')
BIND_DIR = config.get('bind', 'dir')
PRE_SINKHOLE_FILE_1 = config.get('pre_sinkhole', 'file1')
PRE_SINKHOLE_FILE_2 = config.get('pre_sinkhole', 'file2')
SINKHOLE_FILE_1 = config.get('sinkhole', 'file1')
TMP_DIR = config.get('tmp', 'dir')

# The main function
def main():
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

    # Read the information
    for r_file in glob.glob(CLEAN_DIR + '/spool/domains-*'):
        r_file_tmp = open(r_file, 'r')
        r_file_tmp_lines = r_file_tmp.readlines()
        r_file_tmp.close()

        # Organize the file and clean
        for line in r_file_tmp_lines:
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

    r_file = open(PRE_SINKHOLE_FILE_1, 'r')
    r_file_lines = r_file.readlines()
    r_file.close()

    # Step trough lines
    dom_set = set()

    for domain in r_file_lines:
        dom_set.add('zone "' + re.sub(r'\n','',domain) + '" {type master; file "/etc/namedb/sinkhole.target";};\n')

    sinkhole_temp_file = open(SINKHOLE_FILE_1, 'w')
    sinkhole_temp_file.writelines(sorted(dom_set))
    sinkhole_temp_file.close()

    # Change ownership of sinkhole file to bind
    subprocess.call(['chown', 'bind:bind', SINKHOLE_FILE_1])

    # Creating LOG for Suricata
    print '... Creating LOG Syntax ...'

    #START SERVICE
    print '... Restarting Bind: ',
    os.system('pfSsh.php playback svc stop named > /dev/null')
    time.sleep(20)
    os.system('pfSsh.php playback svc start named > /dev/null')
    print 'Done ...'

    # Counting
    r_file = open(SINKHOLE_FILE_1, 'r')
    threats_count = 0
    for line in r_file:
        threats_count += 1
    r_file.close()

    print 'CleanDNS is protecting against %s malware and phishing domains!\nEnjoy!' % threats_count

if __name__ == '__main__':
    main()
