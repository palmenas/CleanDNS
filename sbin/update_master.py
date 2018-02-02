#!/usr/bin/env python2.7

# update master - 0.0.1 (01/20/2018)

# Import libraries
import argparse
import ConfigParser
import os
import subprocess
import sys

# Local library
import clean_environ

# Set environment variables
os.environ['PATH'] = '/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/sbin:/usr/local/bin:/root/bin'

def read_configs():
    config = ConfigParser.RawConfigParser()
    config.read('/cf/cleandns/etc/setup.cfg')
    # config.read('setup.cfg')
    try:
        # Read configuration file
        clean_dir = config.get('cleandns', 'dir')
        return clean_dir
    except:
        print >> sys.stderr, 'ERROR: Could not open "setup.cfg" configuration file.'

# Update the source files, be it a domain of IPs
def update_files(source):
    clean_dir = read_configs()
    if clean_dir:
        try:
            RETCODE = subprocess.call(clean_dir + '/sbin/update_' + source +'.py', shell=False)
            if RETCODE < 0:
                print >> sys.stderr, 'Process terminated with exit code:', -RETCODE
        except OSError as RETCODE_E:
            print >> sys.stderr, 'ERROR: Failed to start the process:', RETCODE_E
            return False

# Main function
def main():
    # Parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ips_mod', help='Update IP files', action='store_true')
    parser.add_argument('-s', '--sinkhole', help='Update sinkhole files', action='store_true')
    args = parser.parse_args()

    # Check values parsed
    if args.ips_mod:
        update_files('ips_mod')
    elif args.sinkhole:
        update_files('sinkhole')
    else:
        # Print help mesage
        subprocess.call([sys.argv[0], '-h'])

# If main :)
if __name__ == '__main__':
    main()
