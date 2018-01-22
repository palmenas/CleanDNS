#!/usr/bin/env python2.7

# update sinkhole - 0.0.1 (01/15/2018)
# update sinkhole - 0.0.2 (01/17/2018)
# update sinkhole - 0.0.3 (01/19/2018)

# Import libraries
import os, sys, ConfigParser, shutil, glob, re, subprocess, time
import clean_environ

# Read configuration file
config = ConfigParser.RawConfigParser()
config.read('/cf/cleandns/etc/setup.cfg')

# Some vars
clean_dir = config.get('cleandns', 'dir')
pre_sinkhole1_file = config.get('pre_sinkhole', 'file1')
pre_sinkhole2_file = config.get('pre_sinkhole', 'file2')
sinkhole1_file = config.get('sinkhole', 'file1')
bind_dir = config.get('bind', 'dir')
tmp_dir = config.get('tmp', 'dir')

# Goes to /tmp
os.chdir(tmp_dir)

# The main function
def main():
    # Getting sources
    print '... Updating malware blacklists ...'
    for source in sorted(glob.glob(clean_dir + '/etc/sources/enabled/domains-*')):
        subprocess.call(source)
        time.sleep(1)

    # Creating local blacklist
    shutil.copyfile(clean_dir + '/etc/local_blacklist-domains.conf', pre_sinkhole2_file)

    # Deduplicating
    s_regs = set()

    # Read the information
    for r_file in glob.glob(clean_dir + '/spool/domains-*'):
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
    all_regs_file = open(pre_sinkhole2_file, 'a')
    all_regs_file.writelines(sorted(s_regs))
    all_regs_file.close()

    # Cleaning whitelist
    subprocess.call(clean_dir + '/bin/run_whitelist_domains.sh')

    # Creating new sinkhole file
    os.remove(sinkhole1_file)

    r_file = open(pre_sinkhole1_file, 'r')
    r_file_lines = r_file.readlines()
    r_file.close()

    # Step trough lines
    dom_set = set()

    for domain in r_file_lines:
        dom_set.add('zone "' + re.sub(r'\n','',domain) + '" {type master; file "/etc/namedb/sinkhole.target";};\n')

    sinkhole_temp_file = open(sinkhole1_file, 'w')
    sinkhole_temp_file.writelines(sorted(dom_set))
    sinkhole_temp_file.close()

    # Change ownership of sinkhole file to bind
    subprocess.call(['chown', 'bind:bind', sinkhole1_file])

    # Creating LOG for Suricata
    print '... Creating LOG Syntax ...'

    #START SERVICE
    print '... Restarting Bind: '
    subprocess.call(['pfSsh.php', 'playback', 'svc', 'stop', 'named', '>/dev/null'])
    time.sleep(20)
    subprocess.call(['pfSsh.php', 'playback', 'svc', 'start', 'named', '>/dev/null'])
    print 'Done ...'

    # Counting
    r_file = open(sinkhole1_file, 'r')
    threats_count = 0
    for line in r_file:
        threats_count = threats_count + 1

    r_file.close()
    print 'CleanDNS is protecting against ' + str(threats_count) + ' malware and phishing domains!\nEnjoy!'

if __name__ == '__main__':
    main()
