#!/usr/bin/env python2.7

# update ips mod - 0.0.1 (01/19/18)

# Import libraries
import os, sys, ConfigParser, shutil, glob, re, subprocess, time, binascii, socket
import clean_environ

# Read configuration file
config = ConfigParser.RawConfigParser()
config.read('/cf/cleandns/etc/setup.cfg')

# Some vars
clean_dir = config.get('cleandns', 'dir')
local_bl_ips = config.get('local_settings','blacklist_ips')
suricata_installed_dir = config.get('suricata','installed_dir')
suricata_installed_rule = config.get('suricata', 'installed_rule')
suricata_block_rule = config.get('suricata','block_rule')
suricata_action = config.get('suricata', 'action')
suricata_bl_1 = config.get('suricata', 'iplist_1')
suricata_bl_2 = config.get('suricata', 'iplist_2')
suricata_pre_rule = config.get('suricata', 'prerule')

# Main function
def main():
    # Deleting old files
    if os.path.isfile(suricata_block_rule):
        os.remove(suricata_block_rule)

    if os.path.isfile(suricata_pre_rule):
        os.remove(suricata_pre_rule)

    print "Updating IPs BlackLists"
    for source in sorted(glob.glob(clean_dir + '/etc/sources/enabled/ips*sh')):
        subprocess.call(source)
        time.sleep(1)

    # Local Blacklist
    shutil.copyfile(local_bl_ips, suricata_bl_2)

    # Deduplicating
    s_regs = set()

    # Read the information
    for r_file in glob.glob(clean_dir + '/spool/ips-*'):
        r_file_tmp = open(r_file, 'r')
        r_file_tmp_lines = r_file_tmp.readlines()
        r_file_tmp.close()

        # Organize the file and clean
        for line in r_file_tmp_lines:
            line = re.sub(' \n','',line)
            if re.search('^[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}$', line):
                s_regs.add(line)

    # Writing sorted, seded, uniqed
    all_regs_file = open(suricata_bl_2, 'a')
    all_regs_file.writelines(sorted(s_regs))
    all_regs_file.close()

    # Cleaning Whitelist
    print 'Cleaning whitelist'
    subprocess.call(clean_dir + '/bin/run_whitelist_ips.sh')

    # IP to Hex -> Suricata
    print 'Updating Suricata Rules'
    r_file = open(suricata_bl_1, 'r')
    r_file_lines = r_file.readlines()
    r_file.close()
    counter = 1
    f_regs = set()
    for line in r_file_lines:
        try:
            socket.inet_aton(line)
            hex_ip = binascii.hexlify(socket.inet_aton(line)).upper()
            str_hex_ip = hex_ip[0:2] + ' ' + hex_ip[2:4] + ' ' + hex_ip[4:6] + ' ' + hex_ip[6:8]
            f_regs.add(suricata_action + ' udp any 53 -> any any (msg:"CleanDNS_Phase3: dns reponse for a malicious IP ' + re.sub('\n', '', line) + ' "; sid:3210 ' + str(counter) + ' ; rev:001; content:"|' + str_hex_ip + '|";)\n')
            counter = counter + 1
        except socket.error:
            continue

    fhan_suri_block_rule = open(suricata_block_rule, 'w')
    fhan_suri_block_rule.writelines(sorted(f_regs))
    fhan_suri_block_rule.close()
    # print 'File created' + str(os.path.isfile(suricata_block_rule))

    # Update Suricata
    if os.path.isfile(suricata_block_rule):
        os.remove(suricata_installed_dir + suricata_installed_rule)
        shutil.copyfile(suricata_block_rule, suricata_installed_dir + suricata_installed_rule)
        subprocess.call(clean_dir + '/sbin/update_suricataconfig.sh')

    # Counting
    print 'CleanDNS is protecting against ' + str(protect_count(suricata_block_rule)) + ' malware IPs!\nEnjoy!'

# Count the threats
def protect_count(f_name):
    counter = 0
    r_file = open(f_name, 'r')
    for line in r_file:
        counter = counter + 1
    r_file.close()
    return(counter)

if __name__ == '__main__':
    main()
